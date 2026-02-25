from pathlib import Path

import numpy as np
import pandas as pd


SOURCE_PATH = Path("data/raw/mercedes_benz_sales_2020_2025.csv")
RAW_SAMPLE_PATH = Path("data/raw/mb_sales_sample_stratified.csv")
PROCESSED_DIR = Path("data/processed")
RANDOM_SEED = 551
TARGET_N = 120_000


def count_strata(path: Path, chunksize: int = 200_000) -> pd.DataFrame:
    counts = {}
    for chunk in pd.read_csv(path, usecols=["Year", "Fuel Type"], chunksize=chunksize):
        key_counts = chunk.value_counts(["Year", "Fuel Type"])
        for key, value in key_counts.items():
            counts[key] = counts.get(key, 0) + int(value)

    rows = [
        {"Year": key[0], "Fuel Type": key[1], "count": value}
        for key, value in counts.items()
    ]
    out = pd.DataFrame(rows)
    return out.sort_values(["Year", "Fuel Type"]).reset_index(drop=True)


def build_sampling_plan(strata_counts: pd.DataFrame) -> pd.DataFrame:
    total = int(strata_counts["count"].sum())
    strata_counts = strata_counts.copy()

    # proportional allocation with lower bound per stratum
    strata_counts["target"] = np.maximum(
        500, np.round(strata_counts["count"] / total * TARGET_N).astype(int)
    )
    strata_counts["target"] = np.minimum(strata_counts["target"], strata_counts["count"])
    strata_counts["prob"] = strata_counts["target"] / strata_counts["count"]
    return strata_counts


def draw_stratified_sample(path: Path, plan: pd.DataFrame, chunksize: int = 200_000) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)
    prob_map = {
        (int(row["Year"]), row["Fuel Type"]): float(row["prob"])
        for _, row in plan.iterrows()
    }
    target_map = {
        (int(row["Year"]), row["Fuel Type"]): int(row["target"])
        for _, row in plan.iterrows()
    }
    picked_map = {k: 0 for k in target_map}

    samples = []
    for chunk in pd.read_csv(path, chunksize=chunksize):
        probs = chunk.apply(
            lambda r: prob_map.get((int(r["Year"]), r["Fuel Type"]), 0.0),
            axis=1,
        ).to_numpy()
        keep = rng.random(len(chunk)) < probs
        sampled = chunk.loc[keep].copy()
        if sampled.empty:
            continue

        sampled["key"] = list(zip(sampled["Year"].astype(int), sampled["Fuel Type"]))
        kept_rows = []
        for key, group in sampled.groupby("key"):
            need = target_map[key] - picked_map[key]
            if need <= 0:
                continue
            take = group.head(need)
            picked_map[key] += len(take)
            kept_rows.append(take.drop(columns=["key"]))
        if kept_rows:
            samples.append(pd.concat(kept_rows, ignore_index=True))

    if not samples:
        raise RuntimeError("no rows sampled; check source data and sampling plan")

    sample_df = pd.concat(samples, ignore_index=True)
    return sample_df


def build_processed_tables(df: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    by_year_fuel = (
        df.groupby(["Year", "Fuel Type"], as_index=False)["Sales Volume"].sum()
        .sort_values(["Year", "Fuel Type"])
        .reset_index(drop=True)
    )
    by_year_fuel.to_csv(out_dir / "sample_sales_by_year_fuel.csv", index=False)

    top_models = (
        df.groupby("Model", as_index=False)["Sales Volume"].sum()
        .sort_values("Sales Volume", ascending=False)
        .head(25)
        .reset_index(drop=True)
    )
    top_models.to_csv(out_dir / "sample_top_models.csv", index=False)

    color_year = (
        df.groupby(["Year", "Color"], as_index=False)["Sales Volume"].sum()
        .sort_values(["Year", "Sales Volume"], ascending=[True, False])
        .reset_index(drop=True)
    )
    color_year.to_csv(out_dir / "sample_color_by_year.csv", index=False)

    # simple bins for speed in dashboards
    binned = df.copy()
    binned["price_bin"] = pd.cut(
        binned["Base Price (USD)"], bins=10, include_lowest=True
    ).astype(str)
    binned["hp_bin"] = pd.cut(binned["Horsepower"], bins=10, include_lowest=True).astype(str)
    price_hp_grid = (
        binned.groupby(["price_bin", "hp_bin"], as_index=False)["Sales Volume"].sum()
        .sort_values("Sales Volume", ascending=False)
        .reset_index(drop=True)
    )
    price_hp_grid.to_csv(out_dir / "sample_price_hp_grid.csv", index=False)


def main() -> None:
    if not SOURCE_PATH.exists():
        raise FileNotFoundError(f"source data not found: {SOURCE_PATH}")

    strata_counts = count_strata(SOURCE_PATH)
    plan = build_sampling_plan(strata_counts)
    sampled = draw_stratified_sample(SOURCE_PATH, plan)
    sampled = sampled.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

    RAW_SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    sampled.to_csv(RAW_SAMPLE_PATH, index=False)
    build_processed_tables(sampled, PROCESSED_DIR)

    summary = sampled.groupby(["Year", "Fuel Type"], as_index=False).size()
    summary.rename(columns={"size": "rows"}, inplace=True)
    summary.to_csv(PROCESSED_DIR / "sample_strata_summary.csv", index=False)

    print(f"saved raw sample: {RAW_SAMPLE_PATH} ({len(sampled)} rows)")
    print(f"saved processed tables in: {PROCESSED_DIR}")


if __name__ == "__main__":
    main()

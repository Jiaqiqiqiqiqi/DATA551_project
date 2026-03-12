from pathlib import Path

import altair as alt
import pandas as pd
from dash import Dash, Input, Output, callback_context, dcc, html


def find_data_file() -> Path:
    candidates = [
        Path("data/raw/mb_sales_sample_stratified.csv"),
        Path("data/raw/mercedes_benz_sales_2020_2025.csv"),
        Path("mercedes_benz_sales_2020_2025.csv"),
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("data file not found")


def load_data() -> pd.DataFrame:
    df = pd.read_csv(find_data_file())
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Base Price (USD)"] = pd.to_numeric(df["Base Price (USD)"], errors="coerce")
    df["Horsepower"] = pd.to_numeric(df["Horsepower"], errors="coerce")
    df["Sales Volume"] = pd.to_numeric(df["Sales Volume"], errors="coerce").fillna(0)
    return df.dropna(
        subset=["Year", "Model", "Fuel Type", "Base Price (USD)", "Horsepower", "Turbo"]
    )


df_all = load_data()

year_min = int(df_all["Year"].min())
year_max = int(df_all["Year"].max())
price_min = int(df_all["Base Price (USD)"].min())
price_max = int(df_all["Base Price (USD)"].max())
hp_min = int(df_all["Horsepower"].min())
hp_max = int(df_all["Horsepower"].max())

model_options = sorted(df_all["Model"].dropna().unique().tolist())
fuel_options = sorted(df_all["Fuel Type"].dropna().unique().tolist())
turbo_options = sorted(df_all["Turbo"].dropna().unique().tolist())

app = Dash(__name__)
server = app.server


def chart_to_html(chart: alt.Chart) -> str:
    return chart.to_html(embed_options={"actions": False})


def make_empty_chart(title: str, message: str) -> alt.Chart:
    source = pd.DataFrame({"text": [message]})
    return (
        alt.Chart(source)
        .mark_text(size=18)
        .encode(text="text:N")
        .properties(width="container", height=320, title=title)
    )


def build_fuel_trend_chart(df: pd.DataFrame) -> alt.Chart:
    if df.empty:
        return make_empty_chart("Fuel Type Sales Trend", "No data for this filter")

    grouped = (
        df.groupby(["Year", "Fuel Type"], as_index=False)["Sales Volume"]
        .sum()
        .sort_values("Year")
    )

    return (
        alt.Chart(grouped)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Year:O",
                title="Year",
                axis=alt.Axis(labelAngle=0, labelOverlap="greedy"),
            ),
            y=alt.Y("Sales Volume:Q", title="Sales Volume"),
            color=alt.Color("Fuel Type:N", title="Fuel Type"),
            tooltip=["Year:O", "Fuel Type:N", "Sales Volume:Q"],
        )
        .properties(width="container", height=320, title="Fuel Type Sales Trend")
    )


def build_model_rank_chart(df: pd.DataFrame) -> alt.Chart:
    if df.empty:
        return make_empty_chart("Top Models by Sales", "No data for this filter")

    if df["Model"].nunique() == 1:
        grouped = df.groupby("Model", as_index=False)["Sales Volume"].sum()
        chart_title = "Selected Model Sales"
    else:
        grouped = (
            df.groupby("Model", as_index=False)["Sales Volume"]
            .sum()
            .nlargest(12, "Sales Volume")
        )
        chart_title = "Top Models by Sales"

    return (
        alt.Chart(grouped)
        .mark_bar()
        .encode(
            x=alt.X("Sales Volume:Q", title="Sales Volume"),
            y=alt.Y("Model:N", sort="-x", title="Model"),
            color=alt.value("#4c78a8"),
            tooltip=["Model:N", "Sales Volume:Q"],
        )
        .properties(width="container", height=320, title=chart_title)
    )


def build_price_hp_chart(df: pd.DataFrame) -> alt.Chart:
    if df.empty:
        return make_empty_chart("Horsepower vs Price", "No data for this filter")

    if len(df) == 1:
        return make_empty_chart(
            "Horsepower vs Price",
            "Only 1 vehicle record matches the current filters",
        )

    sample = df.sample(min(3000, len(df)), random_state=42)

    return (
        alt.Chart(sample)
        .mark_circle(size=40, opacity=0.45)
        .encode(
            x=alt.X("Horsepower:Q", title="Horsepower"),
            y=alt.Y("Base Price (USD):Q", title="Base Price (USD)"),
            color=alt.Color("Fuel Type:N", title="Fuel Type"),
            tooltip=[
                "Model:N",
                "Fuel Type:N",
                "Base Price (USD):Q",
                "Horsepower:Q",
                "Turbo:N",
            ],
        )
        .properties(width="container", height=320, title="Horsepower vs Price")
    )


def build_color_chart(df: pd.DataFrame) -> alt.Chart:
    if df.empty:
        return make_empty_chart("Top Colors", "No data for this filter")

    grouped = (
        df.groupby("Color", as_index=False)["Sales Volume"]
        .sum()
        .nlargest(10, "Sales Volume")
    )

    chart_title = "Selected Color Sales" if grouped["Color"].nunique() == 1 else "Top Colors"

    color_scale = alt.Scale(
        domain=[
            "Black",
            "White",
            "Silver",
            "Gray",
            "Grey",
            "Blue",
            "Red",
            "Green",
            "Yellow",
            "Brown",
            "Beige",
            "Orange",
        ],
        range=[
            "black",
            "white",
            "silver",
            "gray",
            "gray",
            "steelblue",
            "firebrick",
            "forestgreen",
            "gold",
            "saddlebrown",
            "beige",
            "orange",
        ],
    )

    return (
        alt.Chart(grouped)
        .mark_bar()
        .encode(
            x=alt.X("Sales Volume:Q", title="Sales Volume"),
            y=alt.Y("Color:N", sort="-x", title="Color"),
            color=alt.Color("Color:N", scale=color_scale, legend=None),
            tooltip=["Color:N", "Sales Volume:Q"],
        )
        .properties(width="container", height=320, title=chart_title)
    )


def filter_data(
    year_range, models, fuel_types, turbo_types, price_range, horsepower_range
) -> pd.DataFrame:
    df = df_all.copy()
    df = df[df["Year"].between(year_range[0], year_range[1])]
    df = df[df["Base Price (USD)"].between(price_range[0], price_range[1])]
    df = df[df["Horsepower"].between(horsepower_range[0], horsepower_range[1])]

    if models:
        df = df[df["Model"].isin(models)]
    if fuel_types:
        df = df[df["Fuel Type"].isin(fuel_types)]
    if turbo_types:
        df = df[df["Turbo"].isin(turbo_types)]

    return df


app.layout = html.Div(
    [
        html.H1("Mercedes-Benz Sales Insights Dashboard"),
        html.P(
            "Interactive app for exploring trends in models, fuel types, pricing, horsepower, and colors."
        ),
        html.Div(
            [
                html.Label("Year Range"),
                dcc.RangeSlider(
                    id="year-range",
                    min=year_min,
                    max=year_max,
                    value=[year_min, year_max],
                    step=1,
                    marks={y: str(y) for y in range(year_min, year_max + 1)},
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Model"),
                        dcc.Dropdown(
                            id="model-filter",
                            options=[{"label": m, "value": m} for m in model_options],
                            value=[],
                            multi=True,
                            placeholder="All models",
                        ),
                    ],
                    style={"width": "32%"},
                ),
                html.Div(
                    [
                        html.Label("Fuel Type"),
                        dcc.Dropdown(
                            id="fuel-filter",
                            options=[{"label": f, "value": f} for f in fuel_options],
                            value=[],
                            multi=True,
                            placeholder="All fuel types",
                        ),
                    ],
                    style={"width": "32%"},
                ),
                html.Div(
                    [
                        html.Label("Turbo"),
                        dcc.Dropdown(
                            id="turbo-filter",
                            options=[{"label": t, "value": t} for t in turbo_options],
                            value=[],
                            multi=True,
                            placeholder="All turbo settings",
                        ),
                    ],
                    style={"width": "32%"},
                ),
            ],
            style={"display": "flex", "justifyContent": "space-between", "gap": "12px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Price Range (USD)"),
                        dcc.RangeSlider(
                            id="price-range",
                            min=price_min,
                            max=price_max,
                            value=[price_min, price_max],
                            step=500,
                            marks={
                                price_min: f"{price_min:,}",
                                (price_min + price_max) // 2: f"{(price_min + price_max) // 2:,}",
                                price_max: f"{price_max:,}",
                            },
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ],
                    style={"width": "49%"},
                ),
                html.Div(
                    [
                        html.Label("Horsepower Range"),
                        dcc.RangeSlider(
                            id="hp-range",
                            min=hp_min,
                            max=hp_max,
                            value=[hp_min, hp_max],
                            step=5,
                            marks={
                                hp_min: str(hp_min),
                                (hp_min + hp_max) // 2: str((hp_min + hp_max) // 2),
                                hp_max: str(hp_max),
                            },
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ],
                    style={"width": "49%"},
                ),
            ],
            style={"display": "flex", "justifyContent": "space-between", "marginTop": "16px"},
        ),
        html.Button(
            "Reset All Filters",
            id="reset-btn",
            n_clicks=0,
            style={"marginTop": "18px"},
        ),
        html.P(id="status-line", style={"marginTop": "10px", "fontWeight": "bold"}),
        html.Div(
            [
                html.Iframe(
                    id="chart-fuel",
                    style={"width": "100%", "height": "460px", "border": "0", "overflow": "hidden"},
                ),
                html.Iframe(
                    id="chart-model",
                    style={"width": "100%", "height": "460px", "border": "0", "overflow": "hidden"},
                ),
                html.Iframe(
                    id="chart-price-hp",
                    style={"width": "100%", "height": "440px", "border": "0", "overflow": "hidden"},
                ),
                html.Iframe(
                    id="chart-color",
                    style={"width": "100%", "height": "460px", "border": "0", "overflow": "hidden"},
                ),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(600px, 1fr))",
                "gap": "16px",
                "marginTop": "20px",
            },
        ),
    ],
    style={"width": "100%", "maxWidth": "1800px", "margin": "0 auto", "padding": "24px 32px"},
)


@app.callback(
    Output("year-range", "value"),
    Output("model-filter", "value"),
    Output("fuel-filter", "value"),
    Output("turbo-filter", "value"),
    Output("price-range", "value"),
    Output("hp-range", "value"),
    Output("status-line", "children"),
    Output("chart-fuel", "srcDoc"),
    Output("chart-model", "srcDoc"),
    Output("chart-price-hp", "srcDoc"),
    Output("chart-color", "srcDoc"),
    Input("year-range", "value"),
    Input("model-filter", "value"),
    Input("fuel-filter", "value"),
    Input("turbo-filter", "value"),
    Input("price-range", "value"),
    Input("hp-range", "value"),
    Input("reset-btn", "n_clicks"),
)
def update_dashboard(
    year_range, models, fuel_types, turbo_types, price_range, horsepower_range, reset_clicks
):
    trigger = (
        callback_context.triggered[0]["prop_id"].split(".")[0]
        if callback_context.triggered
        else ""
    )

    if trigger == "reset-btn" and reset_clicks:
        year_range = [year_min, year_max]
        models = []
        fuel_types = []
        turbo_types = []
        price_range = [price_min, price_max]
        horsepower_range = [hp_min, hp_max]

    filtered = filter_data(
        year_range=year_range,
        models=models,
        fuel_types=fuel_types,
        turbo_types=turbo_types,
        price_range=price_range,
        horsepower_range=horsepower_range,
    )

    status = (
        f"Vehicles matching current filters: {len(filtered):,} "
        f"| Models: {filtered['Model'].nunique():,}"
    )

    return (
        year_range,
        models,
        fuel_types,
        turbo_types,
        price_range,
        horsepower_range,
        status,
        chart_to_html(build_fuel_trend_chart(filtered)),
        chart_to_html(build_model_rank_chart(filtered)),
        chart_to_html(build_price_hp_chart(filtered)),
        chart_to_html(build_color_chart(filtered)),
    )


if __name__ == "__main__":
    app.run(debug=True)

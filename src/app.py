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

app = Dash(__name__, title="Mercedes-Benz Sales Insights Dashboard")
server = app.server
CHART_HEIGHT = 250


def chart_to_html(chart: alt.Chart) -> str:
    return chart.to_html(embed_options={"actions": False, "renderer": "svg"})


def make_empty_chart(title: str, message: str) -> alt.Chart:
    source = pd.DataFrame({"text": [message]})
    return (
        alt.Chart(source)
        .mark_text(size=18)
        .encode(text="text:N")
        .properties(width="container", height=CHART_HEIGHT, title=title)
    )


def build_fuel_trend_chart(df: pd.DataFrame) -> alt.Chart:
    if df.empty:
        return make_empty_chart("Fuel Type Sales Trend", "No data for this filter")

    grouped = (
        df.groupby(["Year", "Fuel Type"], as_index=False)["Sales Volume"]
        .sum()
        .sort_values("Year")
    )

    year_ticks = max(2, min(6, grouped["Year"].nunique()))

    return (
        alt.Chart(grouped)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Year:Q",
                title="Year",
                axis=alt.Axis(format="d", tickCount=year_ticks, labelAngle=0),
            ),
            y=alt.Y("Sales Volume:Q", title="Sales Volume"),
            color=alt.Color("Fuel Type:N", title="Fuel Type"),
            tooltip=["Year:Q", "Fuel Type:N", "Sales Volume:Q"],
        )
        .properties(width="container", height=CHART_HEIGHT, title="Fuel Type Sales Trend")
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
            color=alt.Color("Model:N", legend=None),
            tooltip=["Model:N", "Sales Volume:Q"],
        )
        .properties(width="container", height=CHART_HEIGHT, title=chart_title)
    )


def build_price_hp_chart(df: pd.DataFrame) -> alt.Chart:
    if df.empty:
        return make_empty_chart("Horsepower vs Price", "No data for this filter")

    if len(df) < 2:
        return make_empty_chart(
            "Horsepower vs Price",
            "Not enough records for regression",
        )

    color_scale = alt.Scale(domain=fuel_options)
    regression_df = df.sample(min(4500, len(df)), random_state=42)

    lines = (
        alt.Chart(regression_df)
        .transform_loess(
            "Horsepower",
            "Base Price (USD)",
            groupby=["Fuel Type"],
            bandwidth=0.6,
        )
        .mark_line(size=3.5)
        .encode(
            x=alt.X("Horsepower:Q", title="Horsepower"),
            y=alt.Y("Base Price (USD):Q", title="Base Price (USD)"),
            color=alt.Color("Fuel Type:N", title="Fuel Type", scale=color_scale),
            tooltip=["Fuel Type:N"],
        )
    )

    return lines.properties(
        width="container", height=CHART_HEIGHT, title="Horsepower vs Price"
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

    return (
        alt.Chart(grouped)
        .mark_bar()
        .encode(
            x=alt.X("Sales Volume:Q", title="Sales Volume"),
            y=alt.Y("Color:N", sort="-x", title="Color"),
            color=alt.value("#4c78a8"),
            tooltip=["Color:N", "Sales Volume:Q"],
        )
        .properties(width="container", height=CHART_HEIGHT, title=chart_title)
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
        html.Div(
            [
                html.Div(
                    [
                        html.Label("YEAR RANGE"),
                        dcc.RangeSlider(
                            id="year-range",
                            min=year_min,
                            max=year_max,
                            value=[year_min, year_max],
                            step=1,
                            marks={y: str(y) for y in range(year_min, year_max + 1)},
                        ),
                        html.Div(style={"height": "4px"}),
                        html.Label("MODEL"),
                        dcc.Dropdown(
                            id="model-filter",
                            options=[{"label": m, "value": m} for m in model_options],
                            value=[],
                            multi=True,
                            placeholder="ALL MODELS",
                        ),
                        html.Div(style={"height": "4px"}),
                        html.Label("FUEL TYPE"),
                        dcc.Dropdown(
                            id="fuel-filter",
                            options=[{"label": f, "value": f} for f in fuel_options],
                            value=[],
                            multi=True,
                            placeholder="ALL FUEL TYPES",
                        ),
                        html.Div(style={"height": "4px"}),
                        html.Label("TURBO"),
                        dcc.Dropdown(
                            id="turbo-filter",
                            options=[{"label": t, "value": t} for t in turbo_options],
                            value=[],
                            multi=True,
                            placeholder="ALL TURBO SETTINGS",
                        ),
                        html.Div(style={"height": "4px"}),
                        html.Label(id="price-range-label"),
                        dcc.RangeSlider(
                            id="price-range",
                            min=price_min,
                            max=price_max,
                            value=[price_min, price_max],
                            step=500,
                            marks={
                                price_min: f"{price_min // 1000}K",
                                (price_min + price_max) // 2: f"{((price_min + price_max) // 2) // 1000}K",
                                price_max: f"{price_max // 1000}K",
                            },
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                        html.Div(style={"height": "4px"}),
                        html.Label(id="hp-range-label"),
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
                        html.Button(
                            "RESET ALL FILTERS",
                            id="reset-btn",
                            n_clicks=0,
                            style={"marginTop": "4px"},
                        ),
                    ],
                    style={
                        "width": "280px",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "4px",
                        "padding": "10px",
                        "border": "1px solid #e5e7eb",
                        "borderRadius": "10px",
                        "backgroundColor": "white",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    "MERCEDES-BENZ SALES INSIGHTS DASHBOARD",
                                    style={"margin": "0", "fontSize": "24px", "lineHeight": "1.1"},
                                ),
                            ],
                            style={"display": "flex", "flexDirection": "column", "gap": "2px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [html.Div("TOTAL RECORDS", style={"fontSize": "11px", "color": "#666"}), html.Div(id="metric-total", style={"fontWeight": "700", "fontSize": "16px"})],
                                    style={"padding": "8px 10px", "border": "1px solid #e5e7eb", "borderRadius": "8px", "backgroundColor": "white"},
                                ),
                                html.Div(
                                    [html.Div("MODEL COUNT", style={"fontSize": "11px", "color": "#666"}), html.Div(id="metric-models", style={"fontWeight": "700", "fontSize": "16px"})],
                                    style={"padding": "8px 10px", "border": "1px solid #e5e7eb", "borderRadius": "8px", "backgroundColor": "white"},
                                ),
                                html.Div(
                                    [html.Div("AVG PRICE (USD)", style={"fontSize": "11px", "color": "#666"}), html.Div(id="metric-price", style={"fontWeight": "700", "fontSize": "16px"})],
                                    style={"padding": "8px 10px", "border": "1px solid #e5e7eb", "borderRadius": "8px", "backgroundColor": "white"},
                                ),
                                html.Div(
                                    [html.Div("AVG HORSEPOWER", style={"fontSize": "11px", "color": "#666"}), html.Div(id="metric-hp", style={"fontWeight": "700", "fontSize": "16px"})],
                                    style={"padding": "8px 10px", "border": "1px solid #e5e7eb", "borderRadius": "8px", "backgroundColor": "white"},
                                ),
                            ],
                            style={"display": "grid", "gridTemplateColumns": "repeat(4, minmax(0, 1fr))", "gap": "8px"},
                        ),
                        html.Div(
                            [
                                html.Iframe(
                                    id="chart-fuel",
                                    style={"width": "100%", "height": "100%", "border": "0"},
                                ),
                                html.Iframe(
                                    id="chart-model",
                                    style={"width": "100%", "height": "100%", "border": "0"},
                                ),
                                html.Iframe(
                                    id="chart-price-hp",
                                    style={"width": "100%", "height": "100%", "border": "0"},
                                ),
                                html.Iframe(
                                    id="chart-color",
                                    style={"width": "100%", "height": "100%", "border": "0"},
                                ),
                            ],
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
                                "gridTemplateRows": "repeat(2, minmax(0, 1fr))",
                                "gap": "6px",
                                "height": "calc(100vh - 170px)",
                                "minHeight": "0",
                            },
                        ),
                    ],
                    style={"flex": "1", "display": "flex", "flexDirection": "column", "gap": "8px"},
                ),
            ],
            style={
                "display": "flex",
                "gap": "8px",
                "height": "calc(100vh - 20px)",
            },
        ),
    ],
    style={
        "width": "100%",
        "maxWidth": "1800px",
        "margin": "0 auto",
        "padding": "8px",
        "boxSizing": "border-box",
        "overflow": "hidden",
        "height": "calc(100vh - 16px)",
    },
)


@app.callback(
    Output("year-range", "value"),
    Output("model-filter", "value"),
    Output("fuel-filter", "value"),
    Output("turbo-filter", "value"),
    Output("price-range", "value"),
    Output("hp-range", "value"),
    Output("price-range-label", "children"),
    Output("hp-range-label", "children"),
    Output("metric-total", "children"),
    Output("metric-models", "children"),
    Output("metric-price", "children"),
    Output("metric-hp", "children"),
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
    filtered_for_regression = filter_data(
        year_range=year_range,
        models=models,
        fuel_types=[],
        turbo_types=turbo_types,
        price_range=price_range,
        horsepower_range=horsepower_range,
    )

    price_label = f"PRICE RANGE (USD): {price_range[0]:,} - {price_range[1]:,}"
    hp_label = f"HORSEPOWER RANGE: {horsepower_range[0]} - {horsepower_range[1]}"
    metric_total = f"{len(filtered):,}"
    metric_models = f"{filtered['Model'].nunique():,}"
    metric_price = (
        f"{int(filtered['Base Price (USD)'].mean()):,}" if not filtered.empty else "0"
    )
    metric_hp = f"{int(filtered['Horsepower'].mean()):,}" if not filtered.empty else "0"

    return (
        year_range,
        models,
        fuel_types,
        turbo_types,
        price_range,
        horsepower_range,
        price_label,
        hp_label,
        metric_total,
        metric_models,
        metric_price,
        metric_hp,
        chart_to_html(build_fuel_trend_chart(filtered)),
        chart_to_html(build_model_rank_chart(filtered)),
        chart_to_html(build_price_hp_chart(filtered_for_regression)),
        chart_to_html(build_color_chart(filtered)),
    )


if __name__ == "__main__":
    app.run(debug=False)

# Milestone 4 Feedback Resolution Log

This document records how TA and peer feedback was addressed for the final dashboard version.

## TA feedback and actions

| Feedback item | Action taken | Status | Evidence |
|---|---|---|---|
| App was not optimized for full-screen use | Reworked layout into a fixed-height single-screen dashboard with left filter panel and right content panel | Implemented | `src/app.py` layout section (`app.layout`) |
| Use more capital letters in UI labels | Updated filter labels and key controls to uppercase style | Implemented | `src/app.py` (`YEAR RANGE`, `MODEL`, `FUEL TYPE`, `RESET ALL FILTERS`) |
| Avoid internal scrolling in chart widgets | Reduced chart heights and tightened spacing in a 2x2 grid to keep views within one screen | Implemented | `CHART_HEIGHT` and chart iframe grid styles in `src/app.py` |
| Price range / horsepower range labels were hard to read | Added dynamic labels that show exact selected ranges above sliders | Implemented | `price-range-label`, `hp-range-label` callback outputs in `src/app.py` |
| Plot looked poor when only one model remained | Added explicit handling for low-data cases (empty and too-few-record conditions) | Implemented | `build_model_rank_chart`, `build_price_hp_chart` in `src/app.py` |
| Clarify wording and chart naming (`price vs horsepower` vs `horsepower vs price`) | Standardized chart title to `Horsepower vs Price` | Implemented | `build_price_hp_chart` title in `src/app.py` |
| Top color chart should have clearer style | Finalized top-color chart with one consistent bar color for readability | Implemented | `build_color_chart` in `src/app.py` |
| Last x-axis labels were crowded | Tuned year-axis tick count/format to improve spacing | Implemented | `build_fuel_trend_chart` in `src/app.py` |

## Peer feedback and actions

| Feedback item | Action taken | Status | Evidence |
|---|---|---|---|
| Horsepower-price panel looked visually noisy | Replaced scatter-heavy view with LOESS regression lines by fuel type | Implemented | `build_price_hp_chart` in `src/app.py` |
| Need all fuel types shown in regression panel | Regression chart uses data filtered by non-fuel controls, then groups by all fuel types | Implemented | `filtered_for_regression` in callback (`src/app.py`) |
| Header area had too much text | Removed subtitle paragraph under main title for cleaner header | Implemented | `app.layout` title block in `src/app.py` |

## Deferred items

- Full chart-to-chart click cross-filtering remains deferred due scope and stability concerns for the final release.
- Reason for defer: milestone goal prioritized usability, performance, and polishing existing global-filter workflow.

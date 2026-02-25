# Reflection for Milestone 2

## What we finished
We built a working dashboard prototype with Dash and Altair.
The app uses one Mercedes-Benz sales dataset from 2020 to 2025.
Users can filter by year, model, fuel type, turbo, price range, and horsepower range.
We added a reset button to clear all filters.

We implemented four charts:
- fuel type sales trend by year
- top models by sales
- price vs horsepower scatter plot
- top colors by sales

These charts help users move from a big picture to details.
The app is readable in full-screen mode.

## What is not finished yet
Some advanced interactions are not finished.
Right now, filters are controlled by dropdowns and sliders.
Direct click selection on charts is not fully linked across all panels yet.

The deployed link is still pending.
We will add the final public URL in README after deployment.

## Known issues
The dataset is large, so loading can take time on first run.
The scatter chart uses sampling for speed.
This means users see pattern shape, not every single point.

## What works well
The layout is simple and clear.
The controls are easy to understand.
The current views already support basic inventory planning questions.

## Next improvements
We plan to add stronger chart-to-chart click interactions.
We also plan to improve style and labels.
After TA feedback, we will update features and complexity for the next milestone.

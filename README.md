# Mercedes-Benz Sales Insights Dashboard (2020-2025)

Deployed app link: **https://data551-project.onrender.com/**

This project is an interactive dashboard for Mercedes-Benz sales data from 2020 to 2025.

## Why this project
We are a student data consulting team.
Our main users are regional dealership managers.
They need simple evidence for inventory and display decisions.

## What users can do
- Check fuel type trend by year
- Check top-selling models
- Compare price and horsepower patterns
- Check top color choices
- Filter data by year, model, fuel type, turbo, price, and horsepower
- Use one reset button to clear all filters

## Interaction design / Dashboard layout
- Global filters: Year range, Model, Fuel type, Turbo, Price range, and Horsepower range update all charts simultaneously.
- Cross-filtering: clicking a category (e.g., a fuel type or a model bar) highlights and filters related records across the other panels for quick segment comparison.
- Hover tooltips: hovering on marks reveals exact counts/percentages and key attributes to support precise reading.
- Reset: a single reset button clears all filters/selections to return to the default overview state.

## Dashboard layout
Main panels in the app:
- Fuel type sales trend
- Top models by sales
- Horsepower vs Price
- Top colors

## Sketch
This is our early layout sketch for dashboard design and interaction flow.

![Dashboard sketch](./Sketch.png)

## Local setup
### 1) create environment (optional)
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) install packages
```bash
pip install -r requirements.txt
```

### 3) run app
```bash
python src/app.py
```

The app will use this file by default:
`data/raw/mb_sales_sample_stratified.csv`

If you have the full raw dataset, you can rebuild samples with:
```bash
python src/build_samples.py
```

Then open the local link in your browser.

## Project structure
```text
DATA551_Project_G11_SUN_YAO_ZHAO/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── reports/
├── doc/
├── requirements.txt
├── Procfile
└── README.md
```

## Future Improvements

In future iterations, we plan to:

- Conduct structured user testing and incorporate feedback
- Improve performance optimization for large datasets
- Introduce additional KPIs such as sales growth rate
- Enhance visual consistency and accessibility

## For contributors
Please read `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` first.
You can open an issue for bugs, ideas, or feature requests.
If you want to help, open a pull request to `main`.

## Team files
- Proposal: `proposal.md`
- Team contract: `team-contract.md`
- Milestone submission link: `canvas-submission.md`

## Milestone 4 Highlights
- Final full-screen layout with a dedicated filter panel and KPI cards
- Improved label readability for range filters
- Refined chart titles and spacing for clearer interpretation
- Feedback-driven redesign of the horsepower-price panel to grouped regression trends
- Final reflection and feedback resolution documentation in `doc/`
- Milestone 4 release and submission materials are prepared


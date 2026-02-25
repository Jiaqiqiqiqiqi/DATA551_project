# Mercedes-Benz Sales Insights Dashboard (2020-2025)

## 1. Motivation and Purpose
Our role is a student data consulting team for car retail planning.  
Our target audience is regional dealership managers.  
These managers need to decide what models and configurations to stock each quarter.  
They also need to track how fast hybrid and electric demand is changing.

We build this dashboard to support these decisions with clear visual evidence.  
Users can compare trends by year, model, fuel type, color, and performance features.  
The goal is to reduce guesswork in inventory planning and product positioning.

## 2. Description of the Data
We use a Mercedes-Benz sales dataset from Kaggle for years 2020 to 2025.  
Each row represents one sold vehicle.

### Dataset Size and Structure
- About 1.8 million rows
- 9 columns
- Missing values are close to none in the current version

### Variables Overview
| Feature | Data type | Description |
|---|---|---|
| Model | Categorical | Vehicle model name, such as A-Class, GLC, AMG S 63 |
| Year | Numeric (discrete) | Year of sale, 2020 to 2025 |
| Region | Categorical | Market region (currently Global) |
| Color | Categorical | Exterior color |
| Fuel Type | Categorical | Petrol, Diesel, Hybrid, Electric |
| Base Price (USD) | Numeric (continuous) | Vehicle base price |
| Horsepower | Numeric (continuous) | Engine power |
| Turbo | Binary categorical | Whether turbo is used (Yes/No) |
| Sales Volume | Numeric | One sale record per row (value is 1) |

### Why this data is useful
- It contains both market trend variables and product feature variables.
- It supports time analysis from 2020 to 2025.
- It supports segmentation by model and fuel type.
- It supports practical business questions about stocking and pricing.

## 3. Research Questions
We focus on three questions.

**RQ1: How do fuel-type sales shares change over time?**  
We will compare yearly sales shares of petrol, diesel, hybrid, and electric vehicles.

**RQ2: How do price, horsepower, and turbo settings relate to sales patterns?**  
We will inspect distribution differences across models and fuel types.

**RQ3: How do color preferences change by model and year?**  
We will compare top colors by year and by model group.

## 4. Usage Scenarios
### Persona
Liam is a regional dealership manager. He prepares quarterly inventory plans.  
He needs simple evidence before he sends order recommendations to headquarters.

### Scenario A: Quarterly inventory planning
Liam opens the dashboard and first selects the last two years.  
He checks the fuel-type trend chart to see if hybrid and electric are growing.  
Next, he clicks one fuel type to filter all other charts.  
He then checks model ranking and price-horsepower distribution for that segment.  
Finally, he exports a short note: increase orders for top models in the selected segment.

### Scenario B: Marketing and display planning
Liam selects one model family and one price range.  
He checks the color chart to find the top colors for that segment.  
Then he switches between years to see if color preferences changed.  
He uses this result to suggest showroom color mix and ad focus for next month.

### Scenario C: Performance package decision
Liam filters by model and compares turbo vs non-turbo sales distribution.  
He looks at horsepower bands and their sales concentration.  
If high-horsepower turbo trims have stable demand, he keeps those trims in stock.  
If not, he reduces low-demand trims and shifts budget to higher-demand configurations.

# Mercedes-Benz Sales Insights Dashboard (2020-2025)

## 1. Motivation and Purpose
Our role: A student data consulting team working for a Mercedes-Benz retail analytics unit.

Target audience: Regional dealership managers who make quarterly inventory and showroom display decisions.

Dealership managers must decide which models and configurations to stock (fuel type, turbo, horsepower bands, and color mix) under a limited budget and floor space. At the same time, they need to monitor whether hybrid/electric demand is accelerating and which segments are shifting.

We built this dashboard to provide evidence-based support for these decisions by enabling fast comparison of sales patterns across years, models, fuel types, prices, and performance features. The goal is to reduce guesswork in inventory planning and improve product positioning using interactive visual exploration.

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
He requires simple evidence before sending order recommendations to headquarters.

### Scenario A: Quarterly inventory planning
Liam opens the dashboard before submitting next-quarter order recommendations.  
1) He sets the Year range filter to the most recent 8 quarters (e.g., 2023–2025) to focus on current demand.  
2) In the Fuel Type trend chart, he compares the sales share trajectories of Petrol vs Hybrid vs Electric.  
3) He clicks “Electric” in the legend (or bar/line) to cross-filter the entire dashboard to only electric records.  
4) The Top Models panel updates; Liam identifies the top 5 electric-selling models and checks whether their trend is stable or growing.  
5) He uses the Price and Horsepower sliders to narrow to the dealership’s budget-friendly range, then checks whether demand concentrates in specific horsepower bands.  
Decision: He increases orders for the best-performing electric models in the selected price band and reduces low-selling trims.


### Scenario B: Marketing and display planning
Liam needs to decide what colors/configurations to feature in next month’s showroom and marketing materials.  
1) He selects a target model family (e.g., GLC) and a mid-to-high price range using filters.  
2) In the Color Preference chart, he ranks colors by sales count and notes the top 3 colors for the chosen segment.  
3) He toggles between years (2024 vs 2025) to check if preferences are shifting (e.g., White decreasing, Grey increasing).  
4) He optionally filters Turbo = Yes to see whether performance-oriented buyers prefer different colors.  
Decision: He recommends a showroom color mix. 

### Scenario C: Performance package decision
Liam wants to know whether performance-oriented configurations are worth stocking.  
1) He filters to one model (or a small set of comparable models).  
2) He compares Turbo = Yes vs No, checking the relative sales volume and how it changes over time.  
3) In the Price vs Horsepower view, he looks for clusters where sales concentrate (e.g., 250–350 hp turbo trims).  
4) He checks whether higher-horsepower trims sell consistently or only in specific years.  
Decision: If turbo high-hp trims exhibit stable demand, he keeps them in the inventory mix; otherwise, he shifts budget toward configurations with stronger, more consistent sales.


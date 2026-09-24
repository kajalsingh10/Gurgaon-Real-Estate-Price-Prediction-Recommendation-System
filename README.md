# Gurgaon Real Estate Price Prediction & Recommendation System

An end-to-end data science project on Gurgaon (Gurugram) property listings. It predicts property prices, surfaces sector-level market insights, and recommends similar apartments.
---

## Table of Contents
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Dataset](#dataset)
- [Project Workflow](#project-workflow)
- [Model Results](#model-results)
- [Recommender System](#recommender-system)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Problem Statement

Property listings in Gurgaon are messy and inconsistent, which makes it hard for buyers, sellers, and analysts to judge whether a price is fair or to find comparable options. This project turns raw listing data into a clean, model-ready dataset and builds three things on top of it:

1. **Price prediction:** estimate a property's price from its attributes.
2. **Market insights:** compare prices and trends across sectors.
3. **Apartment recommender:** suggest similar apartments.

## Features

- Data cleaning and merging of flat and independent house listings
- Feature engineering (luxury score, floor category, property age, furnishing type, and more)
- Outlier treatment and missing-value imputation
- Feature selection using multiple methods (Random Forest importance, Lasso, RFE, SHAP)
- Comparison of 11 regression models with a tuned final pipeline
- Sector-level analytics and map-based visualisations
- Content-based apartment recommender using cosine similarity

## Dataset

Property listings for flats, independent houses, and apartment projects in Gurgaon, collected from 99acres.

| File | Description |
|---|---|
| `flats.csv`, `houses.csv` | Raw listings for flats and independent houses |
| `appartments.csv` | Apartment projects with nearby places, distances, and BHK-wise details |
| `latlong.csv` | Sector coordinates used for map visualisations |
| `gurgaon_properties_*.csv` | Intermediate datasets saved at each stage of the pipeline |

> Predictions are based on listing (asking) prices, not final transaction prices.

## Project Workflow

```
Raw listings (flats, houses, apartments)
        │
   Clean each ─► Merge ─► Level-2 cleaning
        │
   EDA ─► Feature engineering ─► Outlier treatment ─► Missing-value imputation
        │
   Feature selection ─► Baseline models ─► Model selection & tuning
        │
   ┌────┴───────────────┬───────────────────┐
 Price predictor   Analytics / insights   Recommender (cosine similarity)
```

1. **Data preprocessing:** clean flats and houses separately, then merge them into one dataset.
2. **EDA:** univariate and multivariate analysis, plus an automated profiling report.
3. **Feature engineering:** split area types, flag extra rooms, and create age, furnishing, luxury, and floor categories.
4. **Outlier treatment:** remove unrealistic listings (for example, implausible area per room).
5. **Missing-value imputation:** fill gaps using related columns rather than a blanket mean.
6. **Feature selection:** rank features using several methods and drop weak ones.
7. **Modeling:** baseline models, then model selection with a target transformation and hyperparameter tuning.
8. **Extra modules:** analytics, insights, and the recommender system.

Price is modelled on a log scale to reduce right-skew, so very expensive properties do not dominate the loss.

## Model Results

Eleven regression models were compared:

| Model | R² | MAE |
|---|---|---|
| Extra Trees | 0.9023 | 0.4572 |
| XGBoost | 0.9006 | 0.4834 |
| Random Forest | 0.9005 | 0.4536 |
| Gradient Boosting | 0.8891 | 0.5094 |
| MLP | 0.8529 | 0.6297 |
| Decision Tree | 0.8307 | 0.5438 |
| Ridge | 0.8295 | 0.7135 |
| Linear Regression | 0.8295 | 0.7130 |
| AdaBoost | 0.8200 | 0.6815 |
| SVR | 0.7829 | 0.8189 |
| Lasso | 0.0594 | 1.5289 |

**Key takeaways**
- Tree-based ensembles (Extra Trees, XGBoost, Random Forest) all reach R² ≈ 0.90.
- Random Forest has the lowest error (MAE 0.4536), about 36% lower than Linear Regression (0.7130).
- Lasso performs poorly here, most likely because of regularization strength.


## Recommender System

A content-based recommender that finds similar apartments by combining three signals:

- **Facilities:** text-based similarity of amenities (TF-IDF)
- **Attributes:** encoded property attributes
- **Location:** normalized distances to nearby landmarks

Each signal produces a cosine-similarity matrix, and the matrices are combined into one score to rank the most similar apartments.

## Project Structure

```
├── data/
│   ├── flats.csv
│   ├── houses.csv
│   ├── appartments.csv
│   ├── latlong.csv
│   └── gurgaon_properties_*.csv
├── notebooks/
│   ├── data-preprocessing-flats.ipynb
│   ├── data-preprocessing-houses.ipynb
│   ├── merge-flats-and-house.ipynb
│   ├── data-preprocessing-level-2.ipynb
│   ├── eda-univariate-analysis.ipynb
│   ├── eda-multivariate-analysis.ipynb
│   ├── eda-pandas-profiling.ipynb
│   ├── feature-engineering.ipynb
│   ├── outlier-treatment.ipynb
│   ├── missing-value-imputation.ipynb
│   ├── feature-selection.ipynb
│   ├── baseline model.ipynb
│   ├── model-selection.ipynb
│   ├── data-visualization.ipynb
│   ├── insights-module.ipynb
│   └── recommender-system.ipynb
├── requirements.txt
└── README.md
```

> Adjust the folders above to match how your repository is actually organised.

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter and run the notebooks in the order listed above
jupyter notebook
```




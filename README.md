# Data Analysis of Airbnb Datasets (Boston vs. Seattle)
This repository contains the code, and technical details of my Medium article at this [link](https://medium.com/@hedeya1980/data-analysis-of-airbnb-datasets-boston-vs-seattle-dd7410a27e3f).

## Introduction:
In this work I used the following datasets:
* [Bsont Airbnb Open Data | Kaggle.](https://www.kaggle.com/datasets/airbnb/boston)
* [Seattle Airbnb Open Data | Kaggle.](https://www.kaggle.com/datasets/airbnb/seattle)

to answer the following questions:
1. Which neighborhoods have the highest average prices? Are they the same neighborhoods having the highest average price per guest?
2. How prices in the two cities compare based on the property types?
3. What are the most and the least important amenities in each city?
4. Where are the top-rated listings, in each city/neighborhood, located on the map?
5. Do prices vary by month? Which months have the highest prices?
6. How are prices related to availability?

## Files in the Repository:
### [Data Understanding and ETL Preparation](https://github.com/hedeya1980/Airbnb_Boston_vs_Seattle/blob/main/Data%20Understanding%20and%20ETL%20Preparation.ipynb)
This file includes is meant for the following:
* Exploratory Data Analysis to understand the data.
* Basic Data Cleaning.
* Preparing the ETL pipeline.
* Producing the combined database file 'BostonSeattle.db'

### [process_data.py (the ETL execution file)](https://github.com/hedeya1980/Airbnb_Boston_vs_Seattle/blob/main/process_data.py)
This file can be executed to produce the cleaned data (cleandedListings & cleanedCalendars) that will be used for the analysis.

```Example1 (cleanedListings): python process_data.py Boston/listings.csv Seattle/listings.csv BostonSeattle.db cleanedListings```

```Example2 (cleanedCalendars): python process_data.py Boston/calendar.csv Seattle/calendar.csv BostonSeattle.db cleanedCalendars```

### [Data Analysis - Research Questions (Boston vs. Seattle)](https://github.com/hedeya1980/Airbnb_Boston_vs_Seattle/blob/main/Data%20Analysis%20-%20Research%20Questions%20(Boston%20vs.%20Seattle).ipynb)
This file is where data analysis was performed to answer the above questions.


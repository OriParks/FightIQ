FightIQ: Machine Learning-Driven UFC Analytics

Author: Lance (Ori) Parks
Repository: https://github.com/OriParks/FightIQ

Overview

FightIQ is a data analytics and machine learning project focused on predicting outcomes of UFC fights using historical data and real-time statistics collected from UFCStats.com

    . The project integrates automated web scraping, data processing, and predictive modeling to uncover insights into fighter performance and match dynamics.

Features

Automated Data Scraper
Collects live fight and fighter statistics from UFCStats.com using Selenium and Brave Browser.

Data Cleaning and Feature Engineering (in development)
Transforms unstructured fight statistics (e.g., "10 of 30 strikes landed") into structured, numeric features suitable for model training.

Baseline Machine Learning Models (upcoming)
Implements classifiers such as Logistic Regression, Random Forest, and XGBoost to predict fight outcomes.

Analytics Dashboard (planned)
Interactive visualization of fighter statistics and predictive insights using Streamlit.

Technical Stack:
Category	Tools and Libraries
Programming Language	Python 3.11
Data Processing	Pandas, NumPy
Machine Learning	Scikit-learn, XGBoost
Automation	Selenium, BeautifulSoup, chromedriver-autoinstaller
Visualization	Matplotlib, Seaborn
Environment	venv with requirements.txt

Setup Instructions

Clone the Repository

git clone https://github.com/OriParks/FightIQ.git
cd FightIQ

Create and Activate a Virtual Environment

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

Install Dependencies

pip install -r requirements.txt

Run the Data Scraper

python fightiq/data_loader.py

Note: Ensure Brave Browser is installed and accessible at /Applications/Brave Browser.app/Contents/MacOS/Brave Browser.

Output

Generates a CSV file at: data/ufc_fights_raw.csv

Each record represents one fight with fighter names, statistics, and outcomes.

Example Output
fighter_red	fighter_blue	winner	KD_red	KD_blue	SigStr_red	SigStr_blue
Conor McGregor	Dustin Poirier	Blue	0	1	29 of 75	36 of 71
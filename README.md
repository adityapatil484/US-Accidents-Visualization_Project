# US Accidents Data Visualization Project

## Overview
This repository contains a project focused on analyzing US accident data using visualization techniques. The analysis includes data preprocessing, trend analysis, and interactive visualizations.

## Project: US Accidents Data Analysis
- 🚗 **Traffic Accident Data**: The dataset contains records of road accidents across the United States, including details such as location, time, weather conditions, and severity.
- 📊 **Datasets**: `US_Accidents_March23.csv` is the raw file, must be downloaded from kaggle and moved to path `scripts/data/raw/`, processed datasets stored in `scripts/data/processed/`
- 🎯 **Objective**: Explore accident trends and patterns across states, cities, and time periods using analytical and visualization techniques.
- 🛠 **Tech Stack**: Python, Pandas, Matplotlib, Tableau.

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Jupyter Notebook
- Tableau (for visualizations)
- Required dependencies (listed below)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/US-Accidents-Visualization_Project.git
   ```
2. Navigate to the project directory:
   ```sh
   cd US-Accidents-Visualization_Project
   ```
3. **Download the dataset manually** from Kaggle:  
   - Go to [US Accidents Dataset](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents).
   - Download the file `US_Accidents_March23.csv`.
   - Move it into the `scripts/data/raw/` directory.

5. Run the preprocess_data.py script to populate the `scripts/data/processed/` folder
   ```sh
      python3 scripts/preprocess_data.py
   ```

4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Open Jupyter Notebook and run it:
   ```sh
   jupyter notebook notebooks/data_visualization.ipynb
   ```

## Directory Structure
```
US-Accidents-Visualization_Project/
│-- notebooks/
│   │-- data_visualization.ipynb        # Jupyter Notebook for data exploration
│
│-- scripts/
│   │-- preprocess_data.py               # Python script for preprocessing data
│   │-- data/
│   │   ├── raw/
│   │   │   ├── US_Accidents_March23.csv # Raw dataset (must be downloaded manually)
│   │   ├── processed/
│   │   │   ├── accidents_sample.csv    # Sample processed data
│   │   │   ├── city_data.csv           # Processed city-level data
│   │   │   ├── hour_data.csv           # Processed hourly trends
│   │   │   ├── state_data.csv          # Processed state-level data
│   │   │   ├── time_data.csv           # Processed time-based trends
│   │   │   ├── weather_data.csv        # Processed weather conditions data
│   │   │   ├── weekday_data.csv        # Processed weekday trends
│
│-- visualisations/
│   │-- US_Accidents_Data_Visualised.twb # Tableau visualization file
│
│-- requirements.txt                      # Dependencies list
│-- README.md                             # Project documentation
```

## Data Source
This dataset must be downloaded from Kaggle:  
🔗 [US Accidents Dataset](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

## Contribution
Contributions are welcome! Follow these steps to contribute:
1. **Fork** the repository.
2. **Create a new branch** (`feature-branch`).
3. **Commit your changes**.
4. **Open a pull request**.

## Contact
For questions or suggestions, reach out:
- **Author**:  Aditya Patil
- **GitHub**: [adityapatil484](https://github.com/adityapatil484)

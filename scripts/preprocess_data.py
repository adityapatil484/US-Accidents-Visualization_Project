import os
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# User-defined path where manually downloaded dataset is stored
USER_PROVIDED_PATH = Path("/Users/adityapatil/Desktop/US-Accidents-Visualization_Project/scripts/data/raw/US_Accidents_March23.csv") 

# Data directories
PROCESSED_DIR = Path("data/processed")

def ensure_directories():
    """Create necessary directories if they don't exist."""
    PROCESSED_DIR.mkdir(exist_ok=True, parents=True)
    logger.info("Directory structure verified.")

def load_raw_data():
    """Load the manually downloaded US Accidents dataset."""
    if not USER_PROVIDED_PATH.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {USER_PROVIDED_PATH}. "
            "Please manually download the dataset from Kaggle and place it in the specified path."
        )
    
    logger.info(f"Loading data from {USER_PROVIDED_PATH}...")
    
    # Read the first few rows to determine data size
    df_sample = pd.read_csv(USER_PROVIDED_PATH, nrows=5)
    columns = df_sample.columns
    
    # For large datasets, sample to make it more manageable
    if USER_PROVIDED_PATH.stat().st_size > 1e9:  # If file > 1GB
        logger.info("Large dataset detected, using random sampling...")
        df = pd.read_csv(USER_PROVIDED_PATH, usecols=[
            'ID', 'Severity', 'Start_Time', 'End_Time', 'Start_Lat', 'Start_Lng',
            'City', 'County', 'State', 'Temperature(F)', 'Visibility(mi)',
            'Weather_Condition', 'Sunrise_Sunset'
        ])
        # Take a 10% random sample for manageability
        df = df.sample(frac=0.1, random_state=42)
    else:
        df = pd.read_csv(USER_PROVIDED_PATH)
    
    logger.info(f"Loaded dataset with shape: {df.shape}")
    return df

def preprocess_data(df):
    """Preprocess the dataset for visualization."""
    logger.info("Starting data preprocessing...")
    
    # Convert timestamps
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    if 'End_Time' in df.columns:
        df['End_Time'] = pd.to_datetime(df['End_Time'])
        # Calculate accident duration in minutes
        df['Duration_Minutes'] = ((df['End_Time'] - df['Start_Time']).dt.total_seconds() / 60)
    
    # Extract time-based features
    df['Year'] = df['Start_Time'].dt.year
    df['Month'] = df['Start_Time'].dt.month
    df['Day'] = df['Start_Time'].dt.day
    df['Hour'] = df['Start_Time'].dt.hour
    df['DayOfWeek'] = df['Start_Time'].dt.dayofweek
    df['Weekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Handle missing values in key columns
    numerical_cols = ['Severity', 'Start_Lat', 'Start_Lng']
    if 'Temperature(F)' in df.columns:
        numerical_cols.extend(['Temperature(F)', 'Visibility(mi)'])
    
    for col in numerical_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    
    # Simplify weather conditions (if present)
    if 'Weather_Condition' in df.columns:
        # Group similar weather conditions
        weather_mapping = {
            'clear': ['clear', 'fair', 'sunny'],
            'cloudy': ['cloudy', 'overcast', 'partly cloudy'],
            'rain': ['rain', 'drizzle', 'shower'],
            'snow': ['snow', 'sleet', 'ice', 'freezing'],
            'fog': ['fog', 'haze', 'smoke'],
            'thunderstorm': ['thunderstorm', 'storm'],
            'windy': ['windy', 'breezy']
        }
        
        def map_weather(condition):
            if pd.isna(condition):
                return 'unknown'
            condition = condition.lower()
            for category, terms in weather_mapping.items():
                if any(term in condition for term in terms):
                    return category
            return 'other'
        
        df['Weather_Category'] = df['Weather_Condition'].apply(map_weather)
    
    # Create aggregated datasets for different visualization needs
    logger.info("Creating aggregated datasets...")
    
    # 1. Accidents by state
    state_counts = df.groupby('State').size().reset_index(name='Accident_Count')
    state_severity = df.groupby('State')['Severity'].mean().reset_index(name='Avg_Severity')
    state_data = pd.merge(state_counts, state_severity, on='State')
    
    # 2. Accidents by time patterns
    time_data = df.groupby(['Year', 'Month']).size().reset_index(name='Accident_Count')
    hour_data = df.groupby('Hour').size().reset_index(name='Accident_Count')
    weekday_data = df.groupby(['DayOfWeek', 'Weekend']).size().reset_index(name='Accident_Count')
    weekday_data['DayName'] = weekday_data['DayOfWeek'].map({
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
        4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    })
    
    # 3. Weather impact (if available)
    if 'Weather_Category' in df.columns:
        weather_data = df.groupby('Weather_Category').agg({
            'ID': 'count',
            'Severity': 'mean'
        }).reset_index()
        weather_data.columns = ['Weather_Category', 'Accident_Count', 'Avg_Severity']
    else:
        weather_data = pd.DataFrame()
    
    # 4. Cities with most accidents (top 50)
    if 'City' in df.columns:
        city_data = df.groupby(['State', 'City']).size().reset_index(name='Accident_Count')
        city_data = city_data.sort_values('Accident_Count', ascending=False).head(50)
    else:
        city_data = pd.DataFrame()
    
    return {
        'main_data': df,
        'state_data': state_data,
        'time_data': time_data,
        'hour_data': hour_data,
        'weekday_data': weekday_data,
        'weather_data': weather_data,
        'city_data': city_data
    }

def save_processed_data(datasets):
    """Save the processed datasets."""
    logger.info("Saving processed datasets...")
    
    # Save a sample of the main dataset (if it's very large)
    if len(datasets['main_data']) > 100000:
        sample_data = datasets['main_data'].sample(n=100000, random_state=42)
        sample_data.to_csv(PROCESSED_DIR / "accidents_sample.csv", index=False)
    else:
        datasets['main_data'].to_csv(PROCESSED_DIR / "accidents_processed.csv", index=False)
    
    # Save aggregated datasets
    for name, data in datasets.items():
        if name != 'main_data' and not data.empty:
            data.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)
    
    logger.info(f"Processed data saved to {PROCESSED_DIR}")

def main():
    """Main function to execute the preprocessing pipeline."""
    logger.info("Starting data preprocessing pipeline")
    
    ensure_directories()
    raw_data = load_raw_data()
    processed_datasets = preprocess_data(raw_data)
    save_processed_data(processed_datasets)
    
    logger.info("Data preprocessing completed successfully.")

if __name__ == "__main__":
    main()

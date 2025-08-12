import streamlit as st
import pandas as pd
from datetime import datetime, time
from PIL import Image
import requests
from io import BytesIO
import os

# [Previous functions remain the same until the save_data section]

def save_data(df):
    """Save data to CSV with AM/PM time format"""
    # Make a copy to avoid modifying the original dataframe
    csv_df = df.copy()
    
    # Convert times back to AM/PM format for CSV
    if 'Start_Time' in csv_df.columns:
        csv_df['Start_Time'] = pd.to_datetime(csv_df['Start_Time'], format='%H:%M').dt.strftime('%I:%M %p').str.lstrip('0')
    if 'End_Time' in csv_df.columns:
        csv_df['End_Time'] = pd.to_datetime(csv_df['End_Time'], format='%H:%M').dt.strftime('%I:%M %p').str.lstrip('0')
    
    csv_df.to_csv("checklist_records.csv", index=False)

def main():
    # [Previous main() code remains the same until the data submission part]
    
        # Create new record with whatever data is available
        new_data = {
            "Date": [date.strftime('%Y-%m-%d') if date else ""],
            "Start_Time": [time_started.strftime('%H:%M') if time_started else ""],  # Store as 24-hour for calculations
            "End_Time": [time_completed.strftime('%H:%M') if time_completed else ""],  # Store as 24-hour for calculations
            "Duration_Minutes": [duration_minutes if duration_minutes is not None else ""],
            "From_Part": [product_from if product_from else ""],
            "To_Part": [product_to if product_to else ""],
            "Operator": [operator_name if operator_name else ""],
            **{step: [completed] for step, completed in zip(
                t['length_steps'] + t['three_point_steps'] + t['burring_steps'],
                length_steps_completed + three_point_steps_completed + burring_steps_completed
            )},
            "Remarks": [remarks if remarks else ""],
            "Timestamp": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            "Language": [lang]
        }
        
        new_df = pd.DataFrame(new_data)
        df = pd.concat([df, new_df], ignore_index=True)
        save_data(df)  # This will now save with AM/PM format
        
    # [Rest of the main() function remains the same]

if __name__ == "__main__":
    main()

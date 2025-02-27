import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# Streamlit app title
st.title("Crime Pattern Analysis")

# File uploader widget
file_path = st.file_uploader("D:\Criminal Management System 2\30_Auto_theft(in).csv", type="csv")
if file_path is not None:
    # Load the dataset
    data = pd.read_csv(file_path)

    # Drop the 'Unnamed: 2' column as it contains only null values
    data = data.drop(columns=['Unnamed: 2'])

    # Rename columns to standardize and strip any whitespace
    data.columns = data.columns.str.strip().str.replace(' ', '_').str.lower()

    # Check for any remaining missing values and fill or drop them as appropriate
    data = data.dropna(subset=['area_name', 'date', 'group_name', 'sub_group_name', 'auto_theft_stolen'])

    # Convert 'date' to datetime format
    data['date'] = pd.to_datetime(data['date'], errors='coerce')

    # Drop rows where date conversion failed (NaT values)
    data = data.dropna(subset=['date'])

    # Display basic dataset information
    st.write("Cleaned Dataset Information:")
    st.write(data.info())
    st.write("\nFirst few rows of the cleaned dataset:")
    st.write(data.head())

    # ===============================
    # Crime Pattern Analysis
    # ===============================

    # 1. Crime Counts by Area
    st.subheader("Total Crime Incidents by Area")
    area_counts = data['area_name'].value_counts()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=area_counts.index, y=area_counts.values, palette='viridis', ax=ax)
    plt.xticks(rotation=90)
    plt.title('Total Crime Incidents by Area')
    plt.xlabel('Area Name')
    plt.ylabel('Crime Count')
    st.pyplot(fig)

    # 2. Auto Theft Analysis by Type (Coordinated, Recovered, Stolen)
    st.subheader("Auto Theft Incidents by Type")
    theft_cols = ['auto_theft_coordinated/traced', 'auto_theft_recovered', 'auto_theft_stolen']
    theft_totals = data[theft_cols].sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    theft_totals.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'], ax=ax)
    plt.title('Auto Theft Incidents by Type')
    plt.xlabel('Type of Auto Theft')
    plt.ylabel('Number of Incidents')
    st.pyplot(fig)

    # 3. Monthly Crime Trends
    st.subheader("Monthly Crime Trend")
    data['month'] = data['date'].dt.to_period('M')
    monthly_trend = data.groupby('month').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_trend.plot(ax=ax)
    plt.title('Monthly Crime Trend')
    plt.xlabel('Month')
    plt.ylabel('Number of Crimes')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 4. Crime Patterns by Group and Sub Group
    st.subheader("Crime Patterns by Group and Sub Group")
    fig, ax = plt.subplots(figsize=(14, 10))
    group_counts = data.groupby(['group_name', 'sub_group_name']).size().unstack()
    sns.heatmap(group_counts, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True, ax=ax)
    plt.title('Crime Patterns by Group and Sub Group')
    plt.xlabel('Sub Group Name')
    plt.ylabel('Group Name')
    st.pyplot(fig)

    # 5. Auto Theft Analysis by Area
    st.subheader("Auto Theft Incidents by Area")
    auto_theft_by_area = data.groupby('area_name')[theft_cols].sum()
    fig, ax = plt.subplots(figsize=(12, 8))
    auto_theft_by_area.plot(kind='bar', stacked=True, color=['#1f77b4', '#ff7f0e', '#2ca02c'], ax=ax)
    plt.title('Auto Theft Incidents by Area')
    plt.xlabel('Area Name')
    plt.ylabel('Number of Incidents')
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # 6. Detailed Analysis of Auto Theft Recovery Rate by Area
    st.subheader("Auto Theft Recovery Rate by Area")
    data['recovery_rate'] = data['auto_theft_recovered'] / data['auto_theft_stolen'] * 100
    recovery_by_area = data.groupby('area_name')['recovery_rate'].mean().dropna()
    fig, ax = plt.subplots(figsize=(10, 6))
    recovery_by_area.sort_values().plot(kind='bar', color='teal', ax=ax)
    plt.title('Auto Theft Recovery Rate by Area')
    plt.xlabel('Area Name')
    plt.ylabel('Average Recovery Rate (%)')
    plt.xticks(rotation=90)
    st.pyplot(fig)

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Load the datasets
fietsdata = pd.read_csv('fietsdata2021_rentals_by_day.csv')
weather_data = pd.read_csv('weather_london.csv')

# Convert the 'Day' column to datetime
fietsdata['Day'] = pd.to_datetime(fietsdata['Day'], errors='coerce').dt.date  # Ensure 'Day' column is of type datetime.date
weather_data['tavg_date'] = pd.to_datetime(weather_data.index)

# Streamlit app
st.title("Bike Rentals and Weather Data")

# Date Picker for selecting a specific day in 2021
selected_date = st.date_input("Select a date in 2021", min_value=datetime(2021, 1, 1), max_value=datetime(2021, 12, 31))

# Find the week number for the selected date
selected_week = selected_date.isocalendar()[1]

# Display the selected week
st.write(f"Selected Date: {selected_date} (Week {selected_week})")

# Calculate start and end of the week without converting to date again
start_of_week = selected_date - pd.Timedelta(days=selected_date.weekday())  # Start of the week
end_of_week = start_of_week + pd.Timedelta(days=6)  # End of the week

# Filter data for the selected week (7 days before and after)
week_fietsdata = fietsdata[(fietsdata['Day'] >= start_of_week) & (fietsdata['Day'] <= end_of_week)]

# Filter the weather data for the same week
week_weather = weather_data[(weather_data['tavg_date'].dt.date >= start_of_week) & (weather_data['tavg_date'].dt.date <= end_of_week)]

# Allow the user to select which graph they want to see
graph_option = st.selectbox("Select a graph to display", ["Total Rentals", "Average Temperature", "Precipitation", "Temperature vs Rentals"])

# Plot the selected graph
if graph_option == "Total Rentals":
    # Plot Total Rentals for the selected week
    plt.figure(figsize=(10, 6))
    plt.plot(week_fietsdata['Day'], week_fietsdata['Total Rentals'], marker='o', color='b')
    plt.title("Total Rentals for the Week")
    plt.xlabel("Day")
    plt.ylabel("Total Rentals")
    st.pyplot()

elif graph_option == "Average Temperature":
    # Plot the Average Temperature for the selected week
    plt.figure(figsize=(10, 6))
    plt.plot(week_weather['tavg_date'], week_weather['tavg'], marker='o', color='r')
    plt.title("Average Temperature for the Week")
    plt.xlabel("Day")
    plt.ylabel("Temperature (°C)")
    st.pyplot()

elif graph_option == "Precipitation":
    # Plot Precipitation for the selected week
    plt.figure(figsize=(10, 6))
    plt.bar(week_weather['tavg_date'], week_weather['prcp'], color='g')
    plt.title("Precipitation for the Week")
    plt.xlabel("Day")
    plt.ylabel("Precipitation (mm)")
    st.pyplot()

elif graph_option == "Temperature vs Rentals":
    # Plot Temperature vs Total Rentals for the selected week
    plt.figure(figsize=(10, 6))
    plt.plot(week_weather['tavg_date'], week_weather['tavg'], marker='o', label="Temperature (°C)", color='r')
    plt.plot(week_fietsdata['Day'], week_fietsdata['Total Rentals'], marker='o', label="Total Rentals", color='b')
    plt.title("Temperature vs Rentals for the Week")
    plt.xlabel("Day")
    plt.ylabel("Values")
    plt.legend()
    st.pyplot()

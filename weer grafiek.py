# Get the data for temperature and precipitation for the selected week
# Ensure that 'Date' column is in datetime format for filtering
filtered_weather_data = weer_data_2021[weer_data_2021['Date'].isin(filtered_data_week_reset['Date'])]

# Set the plot size and style
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")

# Plot temperature data
plt.plot(filtered_weather_data['Date'], filtered_weather_data['tavg'], label="Gemiddelde Temperatuur (°C)", marker='o')
plt.plot(filtered_weather_data['Date'], filtered_weather_data['tmin'], label="Minimale Temperatuur (°C)", marker='x')
plt.plot(filtered_weather_data['Date'], filtered_weather_data['tmax'], label="Maximale Temperatuur (°C)", marker='s')

# Plot precipitation data
plt.bar(filtered_weather_data['Date'], filtered_weather_data['prcp'], label="Neerslag (mm)", color='blue', alpha=0.3)

# Customize the plot
plt.title(f"Temperatuur en Neerslag voor Week {week_nummer} van 2021")
plt.xlabel("Datum")
plt.ylabel("Waarde")
plt.xticks(rotation=45)
plt.legend()

# Display the plot in Streamlit
st.pyplot(plt)

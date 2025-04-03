# Get the data for temperature and precipitation for the selected week

# Ensure that 'Date' column is in datetime format for filtering
with tab3:
    st.header("🌤️ Weerdata voor 2021")

    # Zet de 'Unnamed: 0' kolom om naar een datetime-object
    weer_data['Date'] = pd.to_datetime(weer_data['Unnamed: 0'], format='%Y-%m-%d')

    # Zet de datum in de fietsdata correct
    fiets_rentals = pd.read_csv('fietsdata2021_rentals_by_day.csv')
    fiets_rentals["Day"] = pd.to_datetime(fiets_rentals["Day"])

    # Merge de weerdata en fietsdata op datum
    weer_data = pd.merge(weer_data, fiets_rentals[['Day', 'Total Rentals']], left_on='Date', right_on='Day', how='left')

    # Filter de data voor 2021
    weer_data_2021 = weer_data[weer_data['Date'].dt.year == 2021]

    # Vertaling van kolomnamen
    column_mapping = {
        'Total Rentals': 'Aantal Verhuurde Fietsen',
        'tavg': 'Gemiddelde Temperatuur (°C)',
        'tmin': 'Minimale Temperatuur (°C)',
        'tmax': 'Maximale Temperatuur (°C)',
        'prcp': 'Neerslag (mm)',
        'snow': 'Sneeuwval (cm)',
        'wdir': 'Windrichting (°)',
        'wspd': 'Windsnelheid (m/s)',
        'wpgt': 'Windstoten (m/s)',
        'pres': 'Luchtdruk (hPa)',
        'tsun': 'Zonduur (uren)'
    }

    # Kalender om een specifieke datum te kiezen
    datum = st.date_input("*Selecteer een datum in 2021*", min_value=pd.to_datetime("2021-01-01"), max_value=pd.to_datetime("2021-12-31"))

    # Haal het weeknummer van de geselecteerde datum op
    week_nummer = datum.isocalendar()[1]

    # Filter de data voor de geselecteerde week
    weer_data_2021['Week'] = weer_data_2021['Date'].dt.isocalendar().week
    filtered_data_week = weer_data_2021[weer_data_2021['Week'] == week_nummer]

    # Toon de gegevens voor de geselecteerde week
    if not filtered_data_week.empty:
        st.write(f"Gegevens voor week {week_nummer} van 2021 (rondom {datum.strftime('%d-%m-%Y')}):")

        # Vervang kolomnamen met de vertaalde versie
        filtered_data_week = filtered_data_week.rename(columns=column_mapping)

        # Reset de index en voeg de aangepaste index toe die begint bij 1
        filtered_data_week_reset = filtered_data_week.reset_index(drop=True)
        filtered_data_week_reset.index = filtered_data_week_reset.index + 1  # Start index vanaf 1

        # Datum formatteren
        filtered_data_week_reset['Date'] = filtered_data_week_reset['Date'].dt.strftime('%d %B %Y')

        # Kolommen herschikken om "Aantal Verhuurde Fietsen" direct na de datum te zetten
        kolommen = ['Date', 'Aantal Verhuurde Fietsen', 'Gemiddelde Temperatuur (°C)', 'Minimale Temperatuur (°C)', 
                    'Maximale Temperatuur (°C)', 'Neerslag (mm)', 'Sneeuwval (cm)', 'Windrichting (°)', 
                    'Windsnelheid (m/s)', 'Windstoten (m/s)', 'Luchtdruk (hPa)', 'Zonduur (uren)']
        
        st.dataframe(filtered_data_week_reset[kolommen])

    else:
        st.write(f"Geen gegevens gevonden voor week {week_nummer} van 2021.")

        # Data inladen
fiets_rentals = pd.read_csv('fietsdata2021_rentals_by_day.csv')
weer_data = pd.read_csv('weather_london.csv')

# Zorg ervoor dat de datums in datetime-formaat staan
fiets_rentals["Day"] = pd.to_datetime(fiets_rentals["Day"])
weer_data["Date"] = pd.to_datetime(weer_data["Unnamed: 0"])  # Zet de juiste kolomnaam om

# Merge de datasets op datum
combined_df = pd.merge(fiets_rentals, weer_data, left_on="Day", right_on="Date", how="inner")

# Verwijder de dubbele datumkolom (we houden "Day")
combined_df.drop(columns=["Date"], inplace=True)

# Streamlit-app titel
st.title("Regressieanalyse: Fietsverhuur en Weer")

# Selecteer een weerfactor voor de regressie
weerfactor = st.selectbox("Kies een weerfactor:", ["tavg", "tmin", "tmax", "prcp", "wspd"])

# X en Y variabelen
x = combined_df[weerfactor]  # Weerfactor (bijv. temperatuur)
y = combined_df["Total Rentals"]  # Aantal fietsverhuringen

# Regressiemodel maken
x_with_constant = sm.add_constant(x)  # Constante toevoegen voor de regressie
model = sm.OLS(y, x_with_constant).fit()
r_squared = model.rsquared  # R²-waarde van de regressie
equation = f"y = {model.params[1]:.2f}x + {model.params[0]:.2f}"  # Regressievergelijking

# Plot maken met seaborn
fig, ax = plt.subplots(figsize=(8, 5))
sns.regplot(x=x, y=y, line_kws={'color': 'red'}, scatter_kws={'alpha': 0.5}, ax=ax)
ax.set_xlabel(weerfactor)
ax.set_ylabel("Aantal Fietsverhuringen")
ax.set_title(f"Regressie: {weerfactor} vs. Fietsverhuur\nR² = {r_squared:.2f}")
ax.text(0.05, 0.9, equation, transform=ax.transAxes, fontsize=12, color="red")

# Toon de plot in Streamlit
st.pyplot(fig)
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

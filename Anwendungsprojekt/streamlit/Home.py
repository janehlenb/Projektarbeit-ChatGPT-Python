import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import plotly.express as px
import requests

API_KEY = '8458a13ebaeba1acef15ef61c32b8d4e'

# TODO: Daten in Tabelle einfügen (Calculate.py) (API-Request fehlt)
# TODO: Metric testen (https://docs.streamlit.io/library/api-reference/session-state)
# TODO: Beschreibung? (API-Request fehlt)


def convert_temp(temperatures, target_unit):
    match target_unit:
        case "°C":
            return temperatures
        case "°F":
            return [(temp * 9/5) + 32 for temp in temperatures]
        case "°K":
            return [temp + 273.15 for temp in temperatures]

def convert_wind_speed(wind_speeds_mps, target_unit):
    match target_unit:
        case "m/s":
            return wind_speeds_mps
        case "km/h":
            return round(wind_speeds_mps * 3.6, 1)
        case "mph":
            return round(wind_speeds_mps * 2.23694, 1)
        case "knt":
            return round(wind_speeds_mps * 1.94384, 1)
        case "Bft":
            beaufort_scale = [
                (0.0, 0),
                (0.3, 0),
                (1.6, 1),
                (3.4, 2),
                (5.5, 3),
                (8.0, 4),
                (10.8, 5),
                (13.9, 6),
                (17.2, 7),
                (20.8, 8),
                (24.5, 9),
                (28.5, 10),
                (32.7, 11)
            ]

            bft_speeds = []
            for wind in wind_speeds_mps:
                bft = None
                for cutoff, bft_value in beaufort_scale:
                    if wind < cutoff:
                        bft = bft_value
                        break
                if bft == None:
                    bft = '12+'
                bft_speeds.append(bft)
                
            return bft_speeds

@st.cache_data
def get_weatherData():
    response = requests.get(f"")
    data = response.json()
    
    min_temp = []
    max_temp = []
    avg_temp = []
    avg_wind = []
    max_gusts = []
    
    return min_temp, max_temp, avg_temp, avg_wind, max_gusts

@st.cache_data
def get_weatherMap():
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}")
    data = response.json()
        
    latitude = data[0]['lat']
    longitude = data[0]['lon']
        
    st.map(data={'LATITUDE': [latitude], 'LONGITUDE': [longitude]}, zoom=12)

@st.cache_data
def get_currentWeatherData(data):
    current_temp = data['main']['temp']
    current_wind_speed = data['wind']['speed']
    current_humidity = data['main']['humidity']  # Extract humidity
    weather_description = data['weather'][0]['description']  # Extract weather description
    weather_icon = data['weather'][0]['icon']
    
    return current_temp, current_wind_speed, current_humidity, weather_description, weather_icon

@st.cache_data # Bei richtigen Daten entfernen
def get_table():
    # Daten bestimmen
    daten = [date.today() + timedelta(days=i) for i in range(6)]
    
    # Temperatur- und Winddaten erhalten
    #min_temp, max_temp, avg_temp, avg_wind, max_gusts = get_weatherData(city)
    
    # Daten ausgeben
    return pd.DataFrame({
        'Tag': daten,
        #'min. Temp.': min_temp,
        #'max. Temp.': max_temp,
        #'Ø Temp.': avg_temp,
        #'Ø Wind': avg_wind,
        #'max. Böen': max_gusts,
        'min. Temp.': [np.random.randint(-15, 20) for _ in range(len(daten))],
        'max. Temp.': [np.random.randint(20, 35) for _ in range(len(daten))],
        'Ø Temp.': [np.random.randint(0, 15) for _ in range(len(daten))],
        'Ø Wind': [np.random.randint(0, 15) for _ in range(len(daten))],
        'max. Böen': [np.random.randint(0, 15) for _ in range(len(daten))]
    })

def get_diagramms_humid_temp(type, only_tomorrow=False):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=de&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if only_tomorrow:
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        api_data = []
    else:
        times = []
        values = []
    
    for entry in data['list']:
        timestamp = entry['dt']
        if only_tomorrow:
            entry_date = datetime.utcfromtimestamp(timestamp).date()
            if entry_date == tomorrow:
                time = datetime.utcfromtimestamp(timestamp).strftime('%H:%M')
                value = entry['main'][type]
                api_data.append((time, value))
                
                times, values = zip(*api_data)
        else:
            value = entry['main']['temp']
            times.append(timestamp)
            values.append(value)
    
    if not only_tomorrow:
        times = [datetime.utcfromtimestamp(ts).strftime('%d.%m.   %H:%M') for ts in times]
    
    match type:
        case 'temp':
            fig = px.line(x=times, y=values, color_discrete_sequence=['red'], height=300)
            fig.update_yaxes(title_text='Temperatur (°C)')
            if only_tomorrow:
                fig.update_xaxes(title_text='Uhrzeit')
                fig.update_layout(title_text=f'Temperaturverlauf morgen in {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
            else:
                fig.update_xaxes(title_text='Datum und Uhrzeit')
                fig.update_layout(title_text=f'5-Tage-Temperaturvorhersage für {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))  
        case 'humidity':
            fig = px.line(x=times, y=values, color_discrete_sequence=['blue'], height=300)
            fig.update_yaxes(title_text='Luftfeuchtigkeit (%)')
            if only_tomorrow:
                fig.update_xaxes(title_text='Uhrzeit')
                fig.update_layout(title_text=f'Luftfeuchtigkeitsverlauf morgen in {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
            else:
                fig.update_xaxes(title_text='Datum und Uhrzeit')
        
    return fig

def get_diagramms_states():
    response = requests.get(url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=de&cnt=8&appid={API_KEY}")
    data = response.json()
    
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    weather_counts = {}
    
    for entry in data['list']:
        timestamp = entry['dt']
        entry_date = datetime.utcfromtimestamp(timestamp).date()

        if entry_date == tomorrow:
            weather = entry['weather'][0]['description']

            if weather not in weather_counts:
                weather_counts[weather] = 1
            else:
                weather_counts[weather] += 1

    labels = list(weather_counts.keys())
    values = list(weather_counts.values())
    
    fig = px.pie(values=values, names=labels, color_discrete_sequence=px.colors.sequential.Blues_r, height=300)
    fig.update_layout(title_text=f'Verteilung der Wetterzustände morgen in {city}')
    st.plotly_chart(fig, use_container_width=True)

def get_diagramms_comparison():
    url_base = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=de&appid={}"
    
    temperatures = []
    humidities = []
    
    for city in st.session_state.cities_comparison_diagramm:
        url = url_base.format(city, API_KEY)
        response = requests.get(url)
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
    
        temperatures.append(temperature)
        humidities.append(humidity)
    
    fig = px.bar(x=st.session_state.cities_comparison_diagramm, y=temperatures, color_discrete_sequence=['red'], height=300)
    fig.update_xaxes(title_text='Städte')
    fig.update_yaxes(title_text='Temperatur (°C)')
    fig.update_layout(title_text=f'Vergleich von Temperatur')
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(page_title="Wetter App", page_icon="🌤️", layout='wide')
st.sidebar.header("Parameter")

with st.sidebar.expander("Wetterdaten auswählen", expanded=True):
    city = st.text_input("Stadt")
    
    show_comparison = st.checkbox("Vergleich mit anderen Städten anzeigen")
    if 'cities_comparison_diagramm' not in st.session_state:
        st.session_state.cities_comparison_diagramm = []
    if show_comparison:
        add_cities_comparison_diagramm = st.text_input("Stadt zum Vergleich hinzufügen")
        if add_cities_comparison_diagramm:
            st.session_state.cities_comparison_diagramm.append(add_cities_comparison_diagramm)
            #st.write('Städte: ' + ', '.join(st.session_state.cities_comparison_diagramm))
        
        if st.button('Liste zurücksetzen'):
            st.session_state.cities_comparison_diagramm = []

with st.sidebar.expander("Einstellungen", expanded=True):
    temp_unit = st.radio("Temperatur-Einheit", ("°C", "°F", "°K"))
    wind_unit = st.radio("Wind-Einheit", ("m/s", "km/h", "mph", "knt", "Bft"))
   
#if chose_city:
if city:
    # Aktuelle Wetterdaten abrufen und testen ob Stadt verfügbar ist
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
    if response.status_code == 200:
        data = response.json()
        current_temp, current_wind_speed, current_humidity, weather_description, weather_icon = get_currentWeatherData(data)
        
        st.title(f"Wetter in {city}")
        col1, col2 = st.columns(2)
        with col1:
            #col11, col12 = st.columns(2)
            #with col11:
            #    # Karte anzeigen
            #    get_weatherMap()
            #with col12:
            #    st.image(f"http://openweathermap.org/img/w/{weather_icon}.png")
            #    st.write(weather_description)
            st.image(f"http://openweathermap.org/img/w/{weather_icon}.png")
            st.write(weather_description)
            
            st.write("Aktuelle Wetterdaten:")
            col11,col12, col13 = st.columns(3)
            with col11:
                metric_temp = st.metric(label="Temperatur", value=f"{current_temp:.1f} °C")
            with col12:
                metric_wind = st.metric(label="Windgeschwindigkeit", value=f"{current_wind_speed:.1f} m/s")
            with col13:
                metric_humidity = st.metric(label="Luftfeuchtigkeit", value=f"{current_humidity} %")
            
            # Wetterdaten anzeigen
            df = get_table()
            df['min. Temp.'] = convert_temp(df['min. Temp.'], temp_unit)
            df['max. Temp.'] = convert_temp(df['max. Temp.'], temp_unit)
            df['Ø Temp.'] = convert_temp(df['Ø Temp.'], temp_unit)
            df['Ø Wind'] = convert_wind_speed(df['Ø Wind'], wind_unit)
            df['max. Böen'] = convert_wind_speed(df['max. Böen'], wind_unit)
            
            st.warning("Die Werte in der Tabelle sind zufällig generiert!")
            st.dataframe(df,
                        column_config={
                            "Tag": st.column_config.DateColumn(
                                format="DD.MM.YYYY",
                            ),
                            "min. Temp.": st.column_config.NumberColumn(
                                format=f"%d {temp_unit}" if temp_unit == "°C" else f"%.1f {temp_unit}" if temp_unit != "°K" else f"%.2f {temp_unit}",
                            ),
                            "max. Temp.": st.column_config.NumberColumn(
                                format=f"%d {temp_unit}" if temp_unit == "°C" else f"%.1f {temp_unit}" if temp_unit != "°K" else f"%.2f {temp_unit}",
                            ),
                            "Ø Temp.": st.column_config.NumberColumn(
                                format=f"%d {temp_unit}" if temp_unit == "°C" else f"%.1f {temp_unit}" if temp_unit != "°K" else f"%.2f {temp_unit}",
                            ),
                            "Ø Wind": st.column_config.NumberColumn(
                                format=f"%d {wind_unit}" if wind_unit == "Bft" or wind_unit == "m/s" else f"%.1f {wind_unit}",
                            ),
                            "max. Böen": st.column_config.NumberColumn(
                                format=f"%d {wind_unit}" if wind_unit == "Bft" or wind_unit == "m/s" else f"%.1f {wind_unit}",
                            ),
                            },
                        hide_index=True,
                        width=600,
                        use_container_width=True
            )
                  
            # Wetterzustände morgen anzeigen
            get_diagramms_states()
            
        with col2:
            # Diagramme anzeigen
            st.plotly_chart(get_diagramms_humid_temp('humidity', only_tomorrow=True), use_container_width=True)
            st.plotly_chart(get_diagramms_humid_temp('temp', only_tomorrow=True), use_container_width=True)
            st.plotly_chart(get_diagramms_humid_temp('temp'), use_container_width=True)
            
            if show_comparison and st.session_state.cities_comparison_diagramm:
                get_diagramms_comparison() 
                
    else:
        st.title("WetterApp")
        st.error(f"Die Stadt **{city}** konnte nicht gefunden werden!")
        
else:
    st.title("WetterApp")
    st.error("Bitte geben Sie eine Stadt an!")
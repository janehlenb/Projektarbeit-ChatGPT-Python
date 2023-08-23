import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import plotly.express as px
import requests

API_KEY = '8458a13ebaeba1acef15ef61c32b8d4e'

# TODO: Daten in Tabelle einfügen (Calculate.py)
# TODO: Metric testen (https://docs.streamlit.io/library/api-reference/session-state)


def convert_wind_speed(wind_speeds_mps, target_unit):
    match target_unit:
        case "km/h":
            return round(wind_speeds_mps * 3.6, 1)
        case "mph":
            return round(wind_speeds_mps * 2.23694, 1)
        case "knots":
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

            for cutoff, description in beaufort_scale:
                for wind in wind_speeds_mps:
                    if wind < cutoff:
                        wind = description
                        break
                    else:
                        wind = 12
                
            return wind_speeds_mps

@st.cache_data
def get_weatherData(city):
    response = requests.get(f"")
    data = response.json()
    
    return min_temp, max_temp, avg_temp, avg_wind, max_gusts

@st.cache_data
def get_currentWeatherData(data):
    current_temp = data['main']['temp']
    current_wind_speed = data['wind']['speed']
    current_humidity = data['main']['humidity']  # Extract humidity
    weather_description = data['weather'][0]['description']  # Extract weather description
    weather_icon = data['weather'][0]['icon']
    
    return current_temp, current_wind_speed, current_humidity, weather_description, weather_icon

# @st.cache_data # Bei richtigen Daten entfernen
# def get_table():
#     # Daten bestimmen
#     heutiges_datum = date.today()
#     alle_daten = [heutiges_datum + timedelta(days=i) for i in range(6)]
#     daten = [datum.strftime("%d.%m.%Y") for datum in alle_daten]
    
#     # Temperatur- und Winddaten erhalten
#     min_temp, max_temp, avg_temp, avg_wind, max_gusts = get_weatherData(city)
    
#     # Daten ausgeben
#     return pd.DataFrame({
#         'Tag': daten,
#         'min. Temp.': min_temp,
#         'max. Temp.': max_temp,
#         'Ø Temp.': avg_temp,
#         'Ø Wind': avg_wind,
#         'max. Böen': max_gusts,
#         })

def get_diagramms_humid_temp(url, type, only_tomorrow=False):
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
            return px.line(x=times, y=values, color_discrete_sequence=['red'], height=300)
        case 'humidity':
            return px.line(x=times, y=values, color_discrete_sequence=['blue'], height=300)

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

def get_diagramms():
    # Feuchtigkeitsverlauf morgen
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=de&cnt=8&appid={API_KEY}"
    fig = get_diagramms_humid_temp(url, 'humidity', only_tomorrow=True)
    fig.update_xaxes(title_text='Uhrzeit')
    fig.update_yaxes(title_text='Luftfeuchtigkeit (%)')
    fig.update_layout(title_text=f'Luftfeuchtigkeitsverlauf morgen in {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    st.plotly_chart(fig, use_container_width=True)

    # Temperaturverlauf morgen
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=de&cnt=8&appid={API_KEY}"
    fig = get_diagramms_humid_temp(url, 'temp', only_tomorrow=True)
    fig.update_xaxes(title_text='Uhrzeit')
    fig.update_yaxes(title_text='Temperatur (°C)')
    fig.update_layout(title_text=f'Temperaturverlauf morgen in {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    st.plotly_chart(fig, use_container_width=True)
    
    # Temperaturverlauf 5 Tage
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=de&appid={API_KEY}"
    fig = get_diagramms_humid_temp(url, 'temp')
    fig.update_xaxes(title_text='Datum und Uhrzeit')
    fig.update_yaxes(title_text='Temperatur (°C)')
    fig.update_layout(title_text=f'5-Tage-Temperaturvorhersage in {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
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
            # df = get_table()
            # match temp_unit:
            #     case "°F":
            #         df['min. Temp.'] = df['min. Temp.'].apply(lambda x: round((x * 9/5) + 32, 1))
            #         df['max. Temp.'] = df['max. Temp.'].apply(lambda x: round((x * 9/5) + 32, 1))
            #         df['Ø Temp.'] = df['Ø Temp.'].apply(lambda x: round((x * 9/5) + 32, 1))
            #     case "°K":
            #         df['min. Temp.'] = df['min. Temp.'].apply(lambda x: round(x + 273.15, 2))
            #         df['max. Temp.'] = df['max. Temp.'].apply(lambda x: round(x + 273.15, 2))
            #         df['Ø Temp.'] = df['Ø Temp.'].apply(lambda x: round(x + 273.15, 2))
                
            # match wind_unit:
            #     case "km/h":
            #         df['Ø Wind'] = convert_wind_speed(df['Ø Wind'], "km/h")
            #         df['max. Böen'] = convert_wind_speed(df['max. Böen'], "km/h")
            #     case "mph":
            #         df['Ø Wind'] = convert_wind_speed(df['Ø Wind'], "mph")
            #         df['max. Böen'] = convert_wind_speed(df['max. Böen'], "mph")
            #     case "knt":
            #         df['Ø Wind'] = convert_wind_speed(df['Ø Wind'], "knt")
            #         df['max. Böen'] = convert_wind_speed(df['max. Böen'], "knt")
            #     case "Bft":
            #         df['Ø Wind'] = convert_wind_speed(df['Ø Wind'], "Bft")
            #         df['max. Böen'] = convert_wind_speed(df['max. Böen'], "Bft")
                    
            # st.dataframe(df, hide_index=True, width=600)
            
            # Wetterzustände morgen anzeigen
            get_diagramms_states()
            
        with col2:
            # Diagramme anzeigen
            get_diagramms()
            
            if show_comparison and st.session_state.cities_comparison_diagramm:
                get_diagramms_comparison() 
                
    else:
        st.title("WetterApp")
        st.error(f"Die Stadt **{city}** konnte nicht gefunden werden!")
        
else:
    st.title("WetterApp")
    st.error("Bitte geben Sie eine Stadt an!")
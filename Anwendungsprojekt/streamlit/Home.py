import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import plotly.graph_objs as go
import plotly.express as px
import requests

API_KEY = '8458a13ebaeba1acef15ef61c32b8d4e'


@st.cache_data # Bei richtigen Daten entfernen
def get_table():
    # Daten bestimmen
    heutiges_datum = date.today()
    alle_daten = [heutiges_datum + timedelta(days=i) for i in range(6)]
    daten = [datum.strftime("%d.%m.%Y") for datum in alle_daten]
    
    # Temperaturdaten erhalten
    # ...
    
    # Daten ausgeben
    return pd.DataFrame({
        'Tag': daten,
        'min. Temp.': [np.random.randint(-15, 20) for _ in range(len(daten))],
        'max. Temp.': [np.random.randint(20, 35) for _ in range(len(daten))],
        'Ø Temp.': [np.random.randint(0, 15) for _ in range(len(daten))],
        'Ø Wind': [np.random.randint(0, 15) for _ in range(len(daten))],
        })

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
    
    return px.line(x=times, y=values, color_discrete_sequence=['orange'], height=300)

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
    
    fig = px.pie(values=values, names=labels, color_discrete_sequence=px.colors.sequential.Oranges_r, height=300)
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
    
    fig = px.bar(x=st.session_state.cities_comparison_diagramm, y=temperatures, color_discrete_sequence=['orange'], height=300)
    fig.update_xaxes(title_text='Städte')
    fig.update_yaxes(title_text='Temperatur (°C)')
    fig.update_layout(title_text=f'Vergleich von Temperatur und Luftfeuchtigkeit')
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
    wind_unit = st.radio("Wind-Einheit", ("km/h", "m/s", "mph"))
   
#if chose_city:
if city:
    st.title(f"Wetter in {city}")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Placeholder (Wetter-Text) ")
        
        # Wetterdaten anzeigen
        df = get_table()
        match temp_unit:
            #case "°C":
            #    st.dataframe(df, hide_index=True)
            case "°F":
                df['min. Temp.'] = df['min. Temp.'].apply(lambda x: int((x * 9/5) + 32))
                df['max. Temp.'] = df['max. Temp.'].apply(lambda x: int((x * 9/5) + 32))
                df['Ø Temp.'] = df['Ø Temp.'].apply(lambda x: int((x * 9/5) + 32))
            case "°K":
                df['min. Temp.'] = df['min. Temp.'].apply(lambda x: int(x + 273.15))
                df['max. Temp.'] = df['max. Temp.'].apply(lambda x: int(x + 273.15))
                df['Ø Temp.'] = df['Ø Temp.'].apply(lambda x: int(x + 273.15))
            
        match wind_unit:
            #case "km/h":
            #    st.dataframe(df, hide_index=True)
            case "m/s":
                df['Ø Wind'] = df['Ø Wind'].apply(lambda x: round(x * 0.277778, 2))
            case "mph":
                df['Ø Wind'] = df['Ø Wind'].apply(lambda x: round(x * 0.621371, 2))

        st.dataframe(df, hide_index=True, width=600)
        
        # Wetterzustände morgen anzeigen
        get_diagramms_states()
         
    with col2:
        # Diagramme anzeigen
        get_diagramms()
        
        if show_comparison and st.session_state.cities_comparison_diagramm:
            get_diagramms_comparison()

else:
    st.title("WetterApp")
    st.error("Bitte geben Sie eine Stadt an!")
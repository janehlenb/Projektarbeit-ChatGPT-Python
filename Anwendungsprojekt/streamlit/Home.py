import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
from timezonefinder import TimezoneFinder
import plotly.express as px
import requests
import pytz
import locale
import all from database_operations

API_KEY = '8458a13ebaeba1acef15ef61c32b8d4e'

# TODO: Fehlermeldung bei falscher Vergleichsangabe


def convert_timezone(timestamp, timezone):
    dt = datetime.fromtimestamp(timestamp)
    if timezone == "Ortszeit":
        tz = pytz.timezone(TimezoneFinder().timezone_at(lng=DATA_BASE['coord']['lon'], lat=DATA_BASE['coord']['lat']))
        return tz, datetime.fromtimestamp(timestamp, tz=tz).strftime("%H:%M"), tz.tzname(datetime.utcnow())
    elif timezone == "Europa/Berlin":
        return pytz.timezone('Europe/Berlin'), datetime.fromtimestamp(timestamp, tz=pytz.timezone('Europe/Berlin')).strftime("%H:%M"), pytz.timezone('Europe/Berlin').tzname(datetime.utcnow())
    elif timezone == "UTC":
        return pytz.timezone('UTC'), datetime.fromtimestamp(timestamp, tz=pytz.timezone('UTC')).strftime("%H:%M"), pytz.timezone('UTC').tzname(datetime.utcnow())

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
            return [round(wind_speed_mps * 3.6, 1) for wind_speed_mps in wind_speeds_mps]
        case "mph":
            return [round(wind_speed_mps * 2.23694, 1) for wind_speed_mps in wind_speeds_mps]
        case "knt":
            return [round(wind_speed_mps * 1.94384, 1) for wind_speed_mps in wind_speeds_mps]
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

def get_forecastWeatherData():
    today = datetime.now()
    temp_mins = []
    temp_maxs = []
    wind_gusts = []
    min_temps_per_day = []
    max_temps_per_day = []
    max_wind_gusts_per_day = []
    avg_temps = []
    avg_winds = []
    
    current_day = None
    min_temp_day = float('inf')
    max_temp_day = float('-inf')
    max_wind_gust_day = 0
    per_day_counter = 0
    day_counter = 0
    
    for entry in DATA_FORECAST['list']:
    # Zeitpunkt des Datensatzes
        timestamp = datetime.fromtimestamp(entry['dt'])
    
        # Nur Daten für die nächsten 5 Tage berücksichtigen
        if today.date() <= timestamp.date() <= today.date() + timedelta(days=5):
            if current_day is None:
                current_day = timestamp.date()
                per_day_counter = 0
                avg_temps.append(0)
                avg_winds.append(0)
            elif current_day != timestamp.date():
                min_temps_per_day.append(min_temp_day)
                max_temps_per_day.append(max_temp_day)
                max_wind_gusts_per_day.append(max_wind_gust_day)
                min_temp_day = float('inf')
                max_temp_day = float('-inf')
                max_wind_gust_day = 0
                avg_temps[day_counter] = avg_temps[day_counter] / per_day_counter
                avg_winds[day_counter] = avg_winds[day_counter] / per_day_counter
                current_day = timestamp.date()
                day_counter += 1
                per_day_counter = 0
                avg_temps.append(0)
                avg_winds.append(0)
            
            temperature = entry['main']['temp']
            temp_min = entry['main']['temp_min']
            temp_max = entry['main']['temp_max']
            wind_speed = entry['wind']['speed']
            wind_gust = entry['wind'].get('gust', 0)  # gust ist nicht immer vorhanden
            
            temp_mins.append(temp_min)
            temp_maxs.append(temp_max)
            wind_gusts.append(wind_gust)
            
            min_temp_day = min(min_temp_day, temp_min)
            max_temp_day = max(max_temp_day, temp_max)
            max_wind_gust_day = max(max_wind_gust_day, wind_gust)
            
            avg_temps[day_counter] += temperature
            avg_winds[day_counter] += wind_speed
            per_day_counter += 1

    avg_temps[day_counter] = avg_temps[day_counter] / per_day_counter
    avg_winds[day_counter] = avg_winds[day_counter] / per_day_counter

    # Füge die Temperaturen des letzten Tages hinzu
    min_temps_per_day.append(min_temp_day)
    max_temps_per_day.append(max_temp_day)
    max_wind_gusts_per_day.append(max_wind_gust_day)
  
    return min_temps_per_day, max_temps_per_day, avg_temps, avg_winds, max_wind_gusts_per_day

def get_currentWeatherData():
    current_temp = DATA_BASE['main']['temp']
    current_temp = convert_temp([current_temp], temp_unit)[0]
    current_wind_speed = DATA_BASE['wind']['speed']
    current_wind_speed = convert_wind_speed([current_wind_speed], wind_unit)[0]
    current_humidity = DATA_BASE['main']['humidity']  # Extract humidity
    weather_description = DATA_BASE['weather'][0]['description']  # Extract weather description
    weather_icon = DATA_BASE['weather'][0]['icon']
    
    return current_temp, current_wind_speed, current_humidity, weather_description, weather_icon

def get_weatherMap():
    data = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}").json()
        
    latitude = data[0]['lat']
    longitude = data[0]['lon']
        
    st.map(data={'LATITUDE': [latitude], 'LONGITUDE': [longitude]}, zoom=12)

def get_table():
    # Daten bestimmen
    locale.setlocale(locale.LC_ALL, "de_DE")
    today = datetime.today()
    dates = []
    
    dates.append("Heute")
    for i in range(1, 6):
        dates.append((today + timedelta(days=i)).strftime('%A'))

    # Temperatur- und Winddaten erhalten
    min_temp, max_temp, avg_temp, avg_wind, max_gusts = get_forecastWeatherData()
    
    # Daten ausgeben
    return pd.DataFrame({
        'Tag': dates,
        'min. Temp.': convert_temp(min_temp, temp_unit),
        'max. Temp.': convert_temp(max_temp, temp_unit),
        'Ø Temp.': convert_temp(avg_temp, temp_unit),
        'Ø Wind': convert_wind_speed(avg_wind, wind_unit),
        'max. Böen': convert_wind_speed(max_gusts, wind_unit),
    })

def get_diagramms_humid_temp(type, only_tomorrow=False):
    if only_tomorrow:
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        api_data = []
    else:
        times = []
        values = []
    
    for entry in DATA_FORECAST['list']:
        timestamp = entry['dt']
        if only_tomorrow:
            entry_date = datetime.utcfromtimestamp(timestamp).date()
            if entry_date == tomorrow:
                time = datetime.utcfromtimestamp(timestamp).strftime('%H:%M')
                value = entry['main'][type]
                api_data.append((time, value))
                
                times, values = zip(*api_data)
        else:
            value = entry['main'][type]
            times.append(timestamp)
            values.append(value)
    
    if not only_tomorrow:
        times = [datetime.utcfromtimestamp(ts).strftime('%d.%m.   %H:%M') for ts in times]
    
    match type:
        case 'temp':
            values = convert_temp(values, temp_unit)
            fig = px.line(x=times, y=values, color_discrete_sequence=['#E76F51'], height=300)
            fig.update_yaxes(title_text=f'Temperatur ({temp_unit})')
            if only_tomorrow:
                fig.update_xaxes(title_text='Uhrzeit')
                fig.update_layout(title_text=f'Temperaturverlauf morgen in {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
            else:
                fig.update_xaxes(title_text='Datum und Uhrzeit')
                fig.update_layout(title_text=f'5-Tage-Temperaturvorhersage für {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))  
        case 'humidity':
            fig = px.line(x=times, y=values, color_discrete_sequence=['#5386E4'], height=300)
            fig.update_yaxes(title_text='Luftfeuchtigkeit (%)')
            if only_tomorrow:
                fig.update_xaxes(title_text='Uhrzeit')
                fig.update_layout(title_text=f'Luftfeuchtigkeitsverlauf morgen in {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
            else:
                fig.update_xaxes(title_text='Datum und Uhrzeit')
                fig.update_layout(title_text=f'5-Tage-Luftfeuchtigkeitsvorhersage für {city}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
        
    return fig

def get_diagramms_states():
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    weather_counts = {}
    
    for entry in DATA_FORECAST['list']:
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
    
    fig = px.pie(values=values, names=labels, color_discrete_sequence=px.colors.sequential.Greens_r, height=300)
    fig.update_layout(title_text=f'Verteilung der Wetterzustände morgen in {city}')
    st.plotly_chart(fig, use_container_width=True)

def get_diagramms_comparison():
    url_base = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=de&appid={}"
    
    temperatures = []
    humidities = []
    
    for city in st.session_state.cities_comparison_diagramm:
        url = url_base.format(city, API_KEY)
        data = requests.get(url).json()
        temperature = data['main']['temp']
        temperature = convert_temp([temperature], temp_unit)[0]
        humidity = data['main']['humidity']
    
        temperatures.append(temperature)
        humidities.append(humidity)
    
    fig = px.bar(x=st.session_state.cities_comparison_diagramm, y=temperatures, color_discrete_sequence=['#E76F51'], height=255)
    fig.update_xaxes(title_text='Städte')
    fig.update_yaxes(title_text=f'Temperatur ({temp_unit})')
    fig.update_layout(title_text=f'Vergleich von Temperaturen in {", ".join(st.session_state.cities_comparison_diagramm)}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    st.plotly_chart(fig, use_container_width=True)
    
    fig = px.bar(x=st.session_state.cities_comparison_diagramm, y=humidities, color_discrete_sequence=['#5386E4'], height=255)
    fig.update_xaxes(title_text='Städte')
    fig.update_yaxes(title_text='Luftfeuchtigkeit (%)')
    fig.update_layout(title_text=f'Vergleich von Luftfeuchtigkeiten in {", ".join(st.session_state.cities_comparison_diagramm)}', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(page_title="WetterApp", page_icon="🌤️", layout='wide')
st.sidebar.header("Parameter")

with st.sidebar.expander("**Wetterdaten auswählen**", expanded=True):
    city = st.text_input("Stadt")
    
    show_comparison = st.checkbox("Vergleich mit anderen Städten anzeigen")
    if 'cities_comparison_diagramm' not in st.session_state:
        st.session_state.cities_comparison_diagramm = []
    if show_comparison:
        city_comparison_diagramm = st.text_input("Stadt zum Vergleich hinzufügen")
        add_cities_comparison_diagramm = st.button("Stadt hinzufügen")
        if add_cities_comparison_diagramm:
            if city_comparison_diagramm not in st.session_state.cities_comparison_diagramm:
                request_test = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_comparison_diagramm}&appid={API_KEY}")
                if request_test.status_code == 200:
                    st.session_state.cities_comparison_diagramm.append(city_comparison_diagramm)
                #else:
                #    st.error(f"Die Stadt **{city_comparison_diagramm}** konnte nicht gefunden werden!")
            #st.write('Städte: ' + ', '.join(st.session_state.cities_comparison_diagramm))
        
        if st.button('Vergleich zurücksetzen'):
            st.session_state.cities_comparison_diagramm = []

with st.sidebar.expander("**Einstellungen**", expanded=True):
    timezone = st.radio("Zeitzone", ("Ortszeit", "Europa/Berlin", "UTC"))
    temp_unit = st.radio("Temperatur-Einheit", ("°C", "°F", "°K"))
    wind_unit = st.radio("Wind-Einheit", ("m/s", "km/h", "mph", "knt", "Bft"))

with st.sidebar.expander("**Verlauf**", expanded=False):
    most_searched_cities = most_searched_cities_db()
    if most_searched_cities:
        st.write("Meist gesuchte Städte:")
        i = 1
        for searched_city in most_searched_cities:
            st.write(f"{i}. {searched_city}")
            i += 1
    
    clear_most_searched_cities = st.button("Liste zurücksetzen")
    if clear_most_searched_cities:
        clear_most_searched_cities_db()
        st.write("Meistgesuchte Städte Liste wurde zurückgesetzt.")


if city:
    URL_BASE = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=de'
    URL_FORECAST = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=de&appid={API_KEY}'
    # Aktuelle Wetterdaten von API abrufen und testen ob Stadt verfügbar ist
    response = requests.get(URL_BASE)
    if response.status_code == 200:
        # Stadt in Datenbank speichern
        save_to_db(city)
        
        # Aktuelle Wetterdaten von API abrufen
        DATA_BASE = response.json()
        current_temp, current_wind_speed, current_humidity, weather_description, weather_icon = get_currentWeatherData()
        
        # Forecast-Wetterdaten von API abrufen
        DATA_FORECAST = requests.get(URL_FORECAST).json()
        
        # Zeitzone der Stadt bestimmen
        tz, tz_time, tz_abbreviation = convert_timezone(DATA_BASE['dt'], timezone)

        # Wetterdaten für ausgewählte Stadt anzeigen
        st.title(f"Wetter in {city}")
        st.caption(f"Aktualisiert um {tz_time} {tz_abbreviation}")
        col1, col2 = st.columns(2)
        with col1:
            # AKtuelle Wetterdaten anzeigen
            col11,col12, col13 = st.columns(3)
            with col11:
                metric_temp = st.metric(label="Temperatur", value=f"{current_temp:.1f} {temp_unit}" if temp_unit != "°K" else f"{current_temp:.2f} {temp_unit}")
            with col12:
                metric_wind = st.metric(label="Windgeschwindigkeit", value=f"{current_wind_speed:.1f} {wind_unit}" if wind_unit != "Bft" else f"{current_wind_speed} {wind_unit}")
            with col13:
                metric_humidity = st.metric(label="Luftfeuchtigkeit", value=f"{current_humidity} %")
            
            # Sonnenuntergang und Sonnenaufgang anzeigen
            sunrise_time = datetime.fromtimestamp(DATA_BASE['sys']['sunrise'], tz=tz).strftime('%H:%M')
            sunset_time = datetime.fromtimestamp(DATA_BASE['sys']['sunset'], tz=tz).strftime('%H:%M')
            col11, col12, col13 = st.columns(3)
            with col11:
                st.write(f"{weather_description}")
                st.image(f"http://openweathermap.org/img/w/{weather_icon}.png")
            with col12:
                st.metric(label="Sonnenaufgang", value=f"{sunrise_time} {tz_abbreviation}")
            with col13:
                st.metric(label="Sonnenuntergang", value=f"{sunset_time} {tz_abbreviation}")  
            
            # Wetterdaten anzeigen
            st.subheader("Wettervorhersage")
            st.dataframe(get_table(),
                        column_config={
                            #"Tag": st.column_config.DateColumn(
                            #    format="DD.MM.YYYY",
                            #),
                            "min. Temp.": st.column_config.NumberColumn(
                                format=f"%.1f {temp_unit}" if temp_unit != "°K" else f"%.2f {temp_unit}",
                            ),
                            "max. Temp.": st.column_config.NumberColumn(
                                format=f"%.1f {temp_unit}" if temp_unit != "°K" else f"%.2f {temp_unit}",
                            ),
                            "Ø Temp.": st.column_config.NumberColumn(
                                format=f"%.1f {temp_unit}" if temp_unit != "°K" else f"%.2f {temp_unit}",
                            ),
                            "Ø Wind": st.column_config.NumberColumn(
                                format=f"%d {wind_unit}" if wind_unit == "Bft"else f"%.1f {wind_unit}",
                            ),
                            "max. Böen": st.column_config.NumberColumn(
                                format=f"%d {wind_unit}" if wind_unit == "Bft"else f"%.1f {wind_unit}",
                            ),
                            },
                        hide_index=True,
                        width=600,
                        use_container_width=True
            )
                
        with col2:
            # Karte anzeigen
            if not show_comparison:
                get_weatherMap()
            # Städtevergleich anzeigen
            else:
                if st.session_state.cities_comparison_diagramm:
                    get_diagramms_comparison()
                else:
                    st.warning("Bitte fügen Sie Städte zum Vergleich hinzu!")
            
        st.subheader("Wetterstatistiken")
        col1, col2 = st.columns(2)
        with col1:
            # Diagramm anzeigen
            st.plotly_chart(get_diagramms_humid_temp('temp'), use_container_width=True)   
            st.plotly_chart(get_diagramms_humid_temp('humidity'), use_container_width=True)
            
            # Wetterzustände morgen anzeigen
            get_diagramms_states()
            
        with col2:
            # Diagramme anzeigen
            st.plotly_chart(get_diagramms_humid_temp('temp', only_tomorrow=True), use_container_width=True) 
            st.plotly_chart(get_diagramms_humid_temp('humidity', only_tomorrow=True), use_container_width=True)
                     
    else:
        st.title("WetterApp")
        st.error(f"Die Stadt **{city}** konnte nicht gefunden werden!")
        
else:
    st.title("WetterApp")
    st.error("Bitte geben Sie eine Stadt an!")

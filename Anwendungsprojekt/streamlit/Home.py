import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta
import plotly.graph_objs as go

@st.cache_data
def get_data():
    heutiges_datum = date.today()
    alle_daten = [heutiges_datum + timedelta(days=i) for i in range(6)]
    daten = [datum.strftime("%d.%m.%Y") for datum in alle_daten]

    return pd.DataFrame({
        'Tag': daten,
        'min. Temp.': [np.random.randint(-15, 20) for _ in range(len(daten))],
        'max. Temp.': [np.random.randint(20, 35) for _ in range(len(daten))],
        'Ø Temp.': [np.random.randint(0, 15) for _ in range(len(daten))],
        'Ø Wind': [np.random.randint(0, 15) for _ in range(len(daten))],
        })

#@st.cache_data
def get_diagramms():
    mat_fig = plt.figure()
    arr = np.random.normal(-10, 40, size=10)
    arr2 = np.random.normal(-10, 40, size=10)
    x_axis = np.sort(arr)
    y_axis = arr2
    
    plt.plot(x_axis, y_axis)
    #plt.title('Placeholder')
    #plt.xlabel('x_axis name')
    #plt.ylabel('y_axis name')
    #plt.grid(True)
    
    fig = go.Figure(data=go.Scatter(x=x_axis, y=y_axis))
    fig.update_xaxes(title_text='x_axis name')
    fig.update_yaxes(title_text='y_axis name')
    fig.update_layout(title_text='Placeholder', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    
    return fig


st.set_page_config(page_title="Wetter App", page_icon="🌤️", layout='wide')

st.sidebar.header("Parameter")

with st.sidebar.expander("Wetterdaten auswählen", expanded=True):
    city = st.text_input("Stadt")
    #chose_city = st.button("Stadt auswählen")
    
    st.write("Placeholder")

with st.sidebar.expander("Einstellungen", expanded=True):
    temp_unit = st.radio("Temperatur-Einheit", ("°C", "°F", "°K"))
    wind_unit = st.radio("Wind-Einheit", ("km/h", "m/s", "mph"))
    
    st.write("Placeholder")
   
#if chose_city:
if city:
    st.title(f"Wetter in {city}")
    #getdata(city)
    col1, col2 = st.columns(2)

    with col1:
        st.write("Placeholder (Wetter-Text) ")
        
        df = get_data()
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
    
    with col2:
        st.plotly_chart(get_diagramms(), use_container_width=True)
        st.plotly_chart(get_diagramms(), use_container_width=True)
        st.plotly_chart(get_diagramms(), use_container_width=True)

else:
    st.title("WetterApp")
    st.error("Bitte geben Sie eine Stadt an!")
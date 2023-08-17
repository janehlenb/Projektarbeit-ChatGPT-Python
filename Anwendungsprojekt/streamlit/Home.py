import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

@st.cache_data
def get_data():
    daten = ["Heute", "Morgen", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    return pd.DataFrame({
        'Datum': daten,
        'min. Temp.': [np.random.randint(-15, 20) for _ in range(len(daten))],
        'max. Temp.': [np.random.randint(20, 35) for _ in range(len(daten))]
        })

#@st.cache_data
def get_diagramms():
    fig = plt.figure()
    arr = np.random.normal(-10, 40, size=10)
    arr2 = np.random.normal(-10, 40, size=10)
    x_axis = np.sort(arr)
    y_axis = arr2
    
    plt.plot(x_axis, y_axis)
    plt.title('Placeholder')
    plt.xlabel('x_axis name')
    plt.ylabel('y_axis name')
    plt.grid(True)
    
    return fig


st.set_page_config(page_title="Wetter App", page_icon="🌤️")#, layout='wide')

st.title("Wetter App")

st.sidebar.header("Parameter")

with st.sidebar.expander("Wetterdaten auswählen", expanded=True):
    city = st.text_input("Stadt")
    
    st.write("Placeholder")

with st.sidebar.expander("Einstellungen", expanded=True):
    unit = st.radio("Einheit", ("°C", "°F", "°K"))
    
    st.write("Placeholder")
   

if city != "":
    col1, col2 = st.columns(2)

    with col1:
        st.write("Placeholder (Tag, Min., Max.)")
        df = get_data()
        
        match unit:
            case "°C":
                st.table(df)
            case "°F":
                df['min. Temp.'] = df['min. Temp.'].apply(lambda x: int((x * 9/5) + 32))
                df['max. Temp.'] = df['max. Temp.'].apply(lambda x: int((x * 9/5) + 32))
                st.table(df)
            case "°K":
                df['min. Temp.'] = df['min. Temp.'].apply(lambda x: int(x + 273.15))
                df['max. Temp.'] = df['max. Temp.'].apply(lambda x: int(x + 273.15))
                st.table(df)

    with col2:
        st.write("Placeholder (Diagramme)")

        st.pyplot(get_diagramms())
        st.pyplot(get_diagramms())
        st.pyplot(get_diagramms())

else:
    st.error("Bitte geben Sie eine Stadt an!")
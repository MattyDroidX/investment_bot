# dashboard/streamlit_app.py
import streamlit as st
import pandas as pd
import json
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Trading Dashboard", layout="wide")

st.title("📊 AI Trading Bot Dashboard")

# Load signal log
try:
    signals = pd.read_csv("data/last_signals.csv")
    st.subheader("🧠 Últimas señales del bot")
    st.dataframe(signals.tail(10))
except:
    st.warning("No se encontraron señales aún.")

# Load portfolio status
try:
    with open("data/portfolio_status.json", "r") as f:
        status = json.load(f)

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Cash disponible", f"${status['cash']:.2f}")
    col2.metric("📦 Posición actual", status['position'])
    col3.metric("📈 Valor actual portafolio", f"${status['portfolio_value']:.2f}")
except:
    st.warning("Estado de portafolio no disponible.")

# Chart (opcional si guardas precios históricos)
try:
    st.subheader("📈 Historial de precios")
    fig, ax = plt.subplots()
    signals['date'] = pd.to_datetime(signals['date'])
    ax.plot(signals['date'], signals['price'], label='Precio')
    ax.plot(signals['date'], signals['predicted'], label='Predicción LSTM')
    ax.legend()
    st.pyplot(fig)
except:
    pass

# Refresh every 30 sec
st.caption("Actualizando cada 30 segundos")
st_autorefresh = st.experimental_rerun
time.sleep(30)

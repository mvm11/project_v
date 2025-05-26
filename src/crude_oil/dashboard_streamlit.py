import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Cargar datos
DATA_PATH = "src/crude_oil/static/data/crude_oil_enriched.csv"
df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

# KPIs
st.title(" Precio del Petróleo")

st.subheader("Indicadores Clave (KPIs)")
col1, col2, col3 = st.columns(3)

tasa_variacion = ((df["close"].iloc[-1] - df["close"].iloc[-2]) / df["close"].iloc[-2]) * 100
media_movil = df["rolling_mean_7"].iloc[-1]
volatilidad = df["rolling_std_7"].iloc[-1]
retorno_acum = ((df["close"].iloc[-1] / df["close"].iloc[0]) - 1) * 100

col1.metric("Tasa de variación (%)", f"{tasa_variacion:.2f}")
col2.metric("Media móvil 7 días", f"{media_movil:.2f}")
col3.metric("Volatilidad 7 días", f"{volatilidad:.2f}")

st.metric("Retorno acumulado (%)", f"{retorno_acum:.2f}")

# Gráfico de precios
st.subheader("Evolución del Precio de Cierre")
fig1, ax1 = plt.subplots()
ax1.plot(df["date"], df["close"], label="Precio de cierre")
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Precio")
ax1.grid(True)
st.pyplot(fig1)

# Gráfico de retornos logarítmicos
st.subheader("Retorno Logarítmico Diario")
fig2, ax2 = plt.subplots()
ax2.plot(df["date"], df["log_return"], color="orange", label="Retorno Logarítmico")
ax2.set_xlabel("Fecha")
ax2.set_ylabel("Log Return")
ax2.grid(True)
st.pyplot(fig2)

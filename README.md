# Análisis y Predicción del Precio del Petróleo Crudo

Este proyecto implementa un pipeline completo para el análisis, modelado y visualización del precio del petróleo crudo. El sistema descarga datos históricos desde Yahoo Finance, los enriquece mediante transformaciones de series de tiempo, entrena un modelo de regresión y genera un dashboard con indicadores clave (KPIs). Todo el flujo está automatizado y organizado por fases.

---

## Fases del Pipeline

1. **Recolección de Datos**

   * Se accede a Yahoo Finance y se extrae la historia del contrato de futuros del crudo (CL=F).
   * Se guardan y consolidan datos nuevos en `static/data/crude_oil.csv`.

2. **Enriquecimiento**

   * Se aplican transformaciones temporales:

     * Media móvil de 7 días
     * Desviación estándar de 7 días
     * Retorno logarítmico diario
     * Día de la semana (0-6)
     * Precio del día siguiente como variable objetivo (`target`)

3. **Modelado**

   * Se entrena un modelo de regresión lineal con los atributos enriquecidos.
   * Se evalúa con MAE y RMSE y se guarda en `static/models/model.pkl`.

4. **Dashboard**
   * Se generan un dashboard en Streamlit, en dashboard_streamlit.py
   * Se generan, adicionalmente gráficos con Matplotlib y una tabla de KPIs.
   * Los dos gráficos de MatplotLib se guarda en `static/dashboard/` como PNGs y CSVs.

---

## KPIs Generados

* Tasa de variación diaria (%)
* Media móvil de 7 días
* Volatilidad (rolling std 7 días)
* Retorno acumulado (%)
* Desviación estándar del precio

---

## Justificación de Métricas del Modelo

Para evaluar el rendimiento del modelo de regresión, se utilizaron dos métricas comunes: el MAE (Error Absoluto Medio) y el RMSE (Raíz del Error Cuadrático Medio).

El **MAE** indica, en promedio, cuánto se equivoca el modelo al hacer una predicción. Su interpretación es sencilla, ya que refleja directamente el error medio sin dar mayor peso a los errores extremos. En este caso, el modelo presentó un MAE de **1.4304**, lo que significa que, en promedio, sus predicciones se desvían del valor real en aproximadamente **1.43 dólares**.

El **RMSE**, por otro lado, penaliza con mayor fuerza aquellos errores que son más grandes. Esta característica lo convierte en una métrica útil cuando se busca controlar los errores más significativos. El valor obtenido fue de **1.9018**, lo cual sugiere que existieron algunas predicciones con errores mayores que incrementaron el promedio cuadrático.

Ambas métricas se complementan: mientras el MAE ofrece una visión clara del error general, el RMSE ayuda a identificar si el modelo comete errores importantes en ciertos casos.
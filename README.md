# 🇬🇹 Sistema de Monitoreo Climático Interactivo (INSIVUMEH)

> **Herramienta de Inteligencia de Negocios (BI) aplicada al sector AgroTech de Guatemala.**

🚀 **[VER DASHBOARD EN VIVO (Click Aquí)](https://dashboard-clima-guatemala-bewnkfvypafure26wqwpxu.streamlit.app/)**

---

## 📋 Sobre el Proyecto
Este proyecto nació de la necesidad de democratizar el acceso a la información climática histórica de Guatemala. Procesando datos del **INSIVUMEH (1900-2024)**, desarrollé una aplicación web que permite visualizar patrones de precipitación y temperatura para mejorar la planificación de cultivos.

## 📸 Galería del Sistema

### 1. Panel de Control Geoespacial
![Vista General](captura1.png)
*Mapa interactivo que permite filtrar datos seleccionando estaciones georreferenciadas. Incluye KPIs en tiempo real (Lluvia total, Temperaturas extremas).*

### 2. Análisis Comparativo Histórico
![Comparativa](captura2.png)
*Módulo diseñado para contrastar el comportamiento del clima entre diferentes años*

### 3. Ubicación Geográfica de las Estaciones
![Comparativa](captura3.png)
*Segmentación de estaciones por ubicación*

---

## 🔧 Ingeniería de Datos y Desarrollo del Backend

Más allá de la visualización, el núcleo de este proyecto reside en un robusto proceso de ingeniería para transformar datos meteorológicos crudos en información accionable:

* **Data Wrangling con Pandas:** Implementé un flujo de trabajo para procesar registros históricos (1990–2024), realizando la limpieza de inconsistencias, normalización de nombres de estaciones y gestión de valores nulos (NaN) para asegurar la integridad analítica.
* **Refinamiento Lógico e Iterativo:** El código fuente fue desarrollado a través de múltiples ciclos de iteración, optimizando la lógica de los filtros dinámicos y la arquitectura de las funciones para garantizar un rendimiento fluido y escalable.
* **Optimización de Almacenamiento (Gzip):** Para superar las limitaciones de carga en la nube, se migró la base de datos de formatos pesados (Excel 25MB) a **archivos CSV con compresión Gzip**. Esto redujo el peso en un **80%**, permitiendo tiempos de respuesta inmediatos incluso en conexiones de baja velocidad.
* **Arquitectura Escalable:** El backend está diseñado de forma modular para facilitar la integración anual de nuevos datasets (como el próximo ciclo 2025) sin necesidad de reescribir la lógica principal del sistema.
* **Despliegue e Integración Continua (CI/CD):** Configuré una conexión directa entre este repositorio y **Streamlit Cloud**, permitiendo que cada mejora en el código fuente se refleje automáticamente en la aplicación en vivo.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Core:** Pandas & NumPy (Procesamiento vectorial)
* **Visualización:** Plotly Express (Gráficos interactivos) & Streamlit (Framework Web)

---

## 👨‍💻 Autor
**José Esquina**


*Especialista en Investigación Agrícola | Python & GIS | Transformación Digital*
[www.linkedin.com/in/jose-esquina-0350aa159]

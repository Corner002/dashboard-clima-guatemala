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
*Módulo diseñado para contrastar el comportamiento del clima entre diferentes años

### 3. Ubicación Geográfica de las Estaciones
![Comparativa](captura3.png)
*Diseñado para filtras las estaciones por ubicación



---

## 🔧 Ingeniería y Optimización (Backend)
Más allá de la visualización, este proyecto implicó desafíos de **Ingeniería de Datos**:

* **Optimización de Carga:** Se migró de una base de datos en Excel (25MB) a un sistema de **archivos planos comprimidos (CSV Gzip)**. Esto redujo el peso en un **80%**, permitiendo que la aplicación cargue en segundos incluso en conexiones móviles.
* **Limpieza de Datos:** Script de Python dedicado a la normalización de nombres de estaciones y manejo de valores nulos para garantizar la integridad estadística.
* **Despliegue Cloud:** CI/CD integrado entre GitHub y Streamlit Cloud para actualizaciones automáticas.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Core:** Pandas & NumPy (Procesamiento vectorial)
* **Visualización:** Plotly Express (Gráficos interactivos) & Streamlit (Framework Web)

---

## 👨‍💻 Autor
**José Esquina**
*Especialista en Investigación Agrícola | Python & GIS | Transformación Digital*
[www.linkedin.com/in/jose-esquina-0350aa159]

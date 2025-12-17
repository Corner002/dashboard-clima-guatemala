# 🚀 Roadmap del Proyecto: Monitoreo Climático GT

Este documento detalla las etapas de desarrollo y las mejoras planificadas para evolucionar este sistema de visualización hacia una plataforma de inteligencia climática avanzada.

## ✅ Fase 1: Cimiento y Visualización (Completado - 2024/2025)
- [x] Limpieza y normalización de datos históricos (1990-2024) con Pandas.
- [x] Optimización de almacenamiento mediante compresión Gzip.
- [x] Desarrollo de Dashboard interactivo en Streamlit.
- [x] Despliegue en la nube y control de versiones en GitHub.

## 🛰️ Fase 2: Inteligencia Espacial y ML (Planificado - 2026)
- [ ] **Imputación de Datos:** Implementar modelos de **Random Forest** para completar vacíos históricos en las estaciones.
- [ ] **Interpolación Dinámica:** Integración de `leafmap` y `pykrige` para generar superficies continuas (Kriging/IDW).
- [ ] **Análisis Multivariado:** Relacionar variables de temperatura y precipitación con índices de rendimiento agrícola local.



## 🤖 Fase 3: Automatización y Tiempo Real (Visión Largo Plazo)
- [ ] **Pipeline Automático:** Uso de `n8n` o `GitHub Actions` para captura automática de datos.
- [ ] **Integración de APIs:** Conexión con servicios globales (NASA POWER/OpenWeather) para validación cruzada.
- [ ] **Alertas Inteligentes:** Sistema de notificaciones basado en umbrales críticos para cultivos específicos.

---
> *Nota: Este proyecto es parte de un proceso de aprendizaje autodidacta en Ciencia de Datos aplicada al sector agroambiental.*

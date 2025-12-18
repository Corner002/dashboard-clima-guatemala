import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import unicodedata

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN Y ESTILOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Climático PRO",
    page_icon="🌩️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS 
st.markdown("""
<style>
.stApp { background-color: #0e1117; }
.block-container { padding-top: 2rem; padding-bottom: 5rem; }

/* Tarjetas Neón */
div[data-testid="stMetric"] {
    background-color: #1f2937;
    border: 1px solid #374151;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #00e6e6;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
div[data-testid="stMetricLabel"] p { color: #9ca3af !important; font-weight: 600; font-size: 13px; }
div[data-testid="stMetricValue"] div { color: #ffffff !important; font-size: 26px !important; font-weight: bold; text-shadow: 0 0 8px rgba(0, 230, 230, 0.4); }

/* Header Estación */
.active-station-header {
    background-color: #1f2937;
    border: 1px solid #00e6e6;
    color: #00e6e6;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 0 15px rgba(0, 230, 230, 0.1);
}

/* Botones */
div.stButton > button {
    background-color: #ef4444; color: white; width: 100%; border-radius: 8px; border: none; font-weight: bold;
}

h1, h2, h3 { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ENCABEZADO (SOLUCIÓN DEL ERROR HTML)
# -----------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: white;'>🇬🇹 Sistema de Monitoreo Climático - INSIVUMEH</h1>", unsafe_allow_html=True)

# AQUÍ ESTABA EL ERROR: El HTML debe estar pegado a la izquierda dentro de las comillas
st.markdown("""
<div style="text-align: center; margin-top: -10px; margin-bottom: 15px;">
    <p style="color: white; font-size: 1rem; margin-bottom: 5px;">Realizado por:</p>
    
    <div style="color: #00f2ff; font-size: 1.6rem; font-weight: bold; text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff; margin-bottom: 10px;">
        José Esquina
    </div>

    <a href="https://www.linkedin.com/in/jose-esquina-0350aa159" target="_blank" style="text-decoration: none; color: white; border: 1px solid #00f2ff; padding: 6px 18px; border-radius: 25px; font-weight: bold; display: inline-block; margin-bottom: 10px; transition: 0.3s;">
        🔗 Contactar en LinkedIn
    </a>

    <p style="color: #cccccc; font-size: 0.9rem;">
        <b>AgroDATA</b> | Especialista en Investigación Agrícola | Python & GIS | Enfocado en Agricultura de Precisión
    </p>
</div>
<hr>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. LÓGICA Y DATOS
# -----------------------------------------------------------------------------
ORDEN_MESES = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

if 'estado_depto' not in st.session_state: st.session_state.estado_depto = 'Todos'
if 'estado_estacion' not in st.session_state: st.session_state.estado_estacion = 'Todas'

def reset_filtros():
    st.session_state.estado_depto = 'Todos'
    st.session_state.estado_estacion = 'Todas'
    st.session_state['sb_depto'] = 'Todos'
    st.session_state['sb_estacion'] = 'Todas'
    if 'years_select' in st.session_state: del st.session_state['years_select']
    st.session_state.sb_m_ini = 'Enero'
    st.session_state.sb_m_fin = 'Diciembre'

def normalizar_texto(texto):
    if pd.isna(texto): return ""
    texto = str(texto).strip().upper()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

@st.cache_data
def cargar_datos():
    try:
        df_clima = pd.read_csv('DATOS_CLIMA.csv.gz') 
        df_coords = pd.read_csv('COORDENADAS.csv.gz')
        
        # Normalización
        df_clima['NOMBRE_ESTACIÓN'] = df_clima['NOMBRE_ESTACIÓN'].apply(normalizar_texto)
        df_coords['Estación'] = df_coords['Estación'].apply(normalizar_texto)
        
        # Fechas
        df_clima['FECHA'] = pd.to_datetime(df_clima['FECHA'])
        df_clima['Año'] = df_clima['FECHA'].dt.year
        df_clima['Mes_Num'] = df_clima['FECHA'].dt.month
        
        # Mapeo Meses
        meses_map = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio',
                     7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}
        df_clima['Mes_Nombre'] = df_clima['Mes_Num'].map(meses_map)
        df_clima['Mes_Nombre'] = pd.Categorical(df_clima['Mes_Nombre'], categories=ORDEN_MESES, ordered=True)
        
        # Merge
        df_final = pd.merge(df_clima, df_coords, left_on='NOMBRE_ESTACIÓN', right_on='Estación', how='inner')
        
        # Columnas Numéricas
        renombres = {'TEMPERATURA_MÁXIMA': 'Temp_Max', 'TEMPERATURA_MÍNIMA': 'Temp_Min', 
                     'TEMPERATURA_MEDIA': 'Temp_Media', 'PRECIPITACIÓN': 'Precipitacion', 'HUMEDAD_RELATIVA': 'Humedad'}
        df_final.rename(columns=renombres, inplace=True)
        
        cols_num = ['Temp_Max', 'Temp_Min', 'Temp_Media', 'Precipitacion', 'Humedad']
        df_final[cols_num] = df_final[cols_num].apply(pd.to_numeric, errors='coerce')
        for col in cols_no_cero := ['Temp_Max', 'Temp_Min', 'Temp_Media', 'Humedad']:
            df_final.loc[df_final[col] == 0, col] = np.nan
            
        return df_final.sort_values('FECHA')
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        st.stop()

df = cargar_datos()

# -----------------------------------------------------------------------------
# 4. PANEL LATERAL
# -----------------------------------------------------------------------------
st.sidebar.header("🎛️ Panel de Control")
if st.sidebar.button("🧹 RESTAURAR TODO"):
    reset_filtros()
    st.rerun()

# Depto
deptos = ['Todos'] + sorted(df['Departamento'].unique().tolist())
idx_depto = deptos.index(st.session_state.estado_depto) if st.session_state.estado_depto in deptos else 0
depto_selec = st.sidebar.selectbox("1. Departamento", deptos, index=idx_depto, key='sb_depto')

if depto_selec != st.session_state.estado_depto:
    st.session_state.estado_depto = depto_selec
    st.session_state.estado_estacion = 'Todas'
    if 'sb_estacion' in st.session_state: del st.session_state['sb_estacion']
    st.rerun()

# Estación
estaciones_disp = ['Todas'] + sorted(df[df['Departamento'] == depto_selec]['NOMBRE_ESTACIÓN'].unique().tolist()) if depto_selec != 'Todos' else ['Todas'] + sorted(df['NOMBRE_ESTACIÓN'].unique().tolist())
idx_est = estaciones_disp.index(st.session_state.estado_estacion) if st.session_state.estado_estacion in estaciones_disp else 0
estacion_selec = st.sidebar.selectbox("2. Estación", estaciones_disp, index=idx_est, key='sb_estacion')

if estacion_selec != st.session_state.estado_estacion:
    st.session_state.estado_estacion = estacion_selec
    st.rerun()

# Tiempo
st.sidebar.markdown("---")
años_disp = sorted([int(x) for x in df['Año'].dropna().unique().tolist()], reverse=True)
años_selec = st.sidebar.multiselect("Años", años_disp, default=años_disp[:1], key='years_select')

col_m1, col_m2 = st.sidebar.columns(2)
mes_inicio = col_m1.selectbox("Desde", ORDEN_MESES, index=0, key='sb_m_ini')
mes_fin = col_m2.selectbox("Hasta", ORDEN_MESES, index=11, key='sb_m_fin')
mes_inicio_num = ORDEN_MESES.index(mes_inicio) + 1
mes_fin_num = ORDEN_MESES.index(mes_fin) + 1

# Filtros
mask = pd.Series(True, index=df.index)
if depto_selec != 'Todos': mask &= (df['Departamento'] == depto_selec)
if estacion_selec != 'Todas': mask &= (df['NOMBRE_ESTACIÓN'] == estacion_selec)
if años_selec: mask &= df['Año'].isin(años_selec)
if mes_inicio_num <= mes_fin_num:
    mask &= (df['Mes_Num'] >= mes_inicio_num) & (df['Mes_Num'] <= mes_fin_num)
else:
    st.sidebar.error("'Desde' debe ser menor que 'Hasta'")

df_filtrado = df[mask].copy()

# -----------------------------------------------------------------------------
# 5. GRAFICACIÓN
# -----------------------------------------------------------------------------
def plot_barras(data, x, y, titulo, color_hex):
    fig = px.bar(data, x=x, y=y, title=titulo, color_discrete_sequence=[color_hex], 
                 template='plotly_dark', category_orders={x: ORDEN_MESES},
                 labels={x: "Mes", "Precipitacion": "Lluvia (mm)"})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=20))
    return fig

def plot_linea(data, x, y, titulo, color_hex):
    # GRAFICA CORREGIDA: Eje X limpio con Meses
    fig = px.line(data, x=x, y=y, title=titulo, markers=True, color_discrete_sequence=[color_hex], 
                  template='plotly_dark', category_orders={x: ORDEN_MESES},
                  labels={x: "Mes", y: "Temperatura (°C)"})
    fig.update_traces(connectgaps=False) 
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=20))
    return fig

# -----------------------------------------------------------------------------
# 6. VISUALIZACIÓN
# -----------------------------------------------------------------------------
tab_resumen, tab_comp = st.tabs(["📊 RESUMEN GENERAL & MAPA", "🆚 COMPARATIVA ANUAL"])

with tab_resumen:
    anios_str = ", ".join(map(str, sorted(años_selec))) if años_selec else "Todos"
    
    # Header Estación
    if estacion_selec != 'Todas':
        depto_actual = df[df['NOMBRE_ESTACIÓN'] == estacion_selec]['Departamento'].iloc[0]
        st.markdown(f'<div class="active-station-header">📡 ESTACIÓN: {estacion_selec} | 📍 {depto_actual} | 📅 {anios_str}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="active-station-header" style="border-color:#555; color:#aaa;">📡 TODAS LAS ESTACIONES ({depto_selec}) | 📅 {anios_str}</div>', unsafe_allow_html=True)

    if df_filtrado.empty:
        st.warning("⚠️ No hay datos disponibles.")
    else:
        # KPIs
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("💧 Lluvia Total", f"{df_filtrado['Precipitacion'].sum():,.1f} mm")
        k2.metric("🌡️ Media", f"{df_filtrado['Temp_Media'].mean():.1f} °C")
        k3.metric("🔥 Máxima", f"{df_filtrado['Temp_Max'].max():.1f} °C")
        k4.metric("❄️ Mínima", f"{df_filtrado['Temp_Min'].min():.1f} °C")
        k5.metric("💨 Humedad", f"{df_filtrado['Humedad'].mean():.1f} %")

        st.markdown("---")
        
        # GRÁFICAS PRINCIPALES
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            df_lluvia = df_filtrado.groupby(['Mes_Nombre'], observed=False)['Precipitacion'].sum().reset_index()
            st.plotly_chart(plot_barras(df_lluvia, 'Mes_Nombre', 'Precipitacion', "🌧️ Precipitación Mensual", "#00e6e6"), use_container_width=True)
        
        with col_g2:
            # LÓGICA MENSUAL (Para eje X limpio)
            df_temp = df_filtrado.groupby(['Mes_Nombre'], observed=False)['Temp_Media'].mean().reset_index()
            st.plotly_chart(plot_linea(df_temp, 'Mes_Nombre', 'Temp_Media', "🌡️ Temperatura Media Mensual", "#ffe600"), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        df_h = df_filtrado.groupby(['Mes_Nombre'], observed=False)['Humedad'].mean().reset_index()
        fig_h = px.area(df_h, x='Mes_Nombre', y='Humedad', title="Humedad Relativa (%)", 
                        color_discrete_sequence=['#d900ff'], template='plotly_dark',
                        category_orders={'Mes_Nombre': ORDEN_MESES},
                        labels={'Mes_Nombre': 'Mes', 'Humedad': 'Humedad (%)'})
        fig_h.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_range=[0, 100])
        st.plotly_chart(fig_h, use_container_width=True)

        # MAPA (RESTAURADO)
        st.markdown("---")
        st.subheader("📍 Ubicación Geográfica")
        
        if depto_selec != 'Todos':
            df_mapa = df[df['Departamento'] == depto_selec].groupby(['NOMBRE_ESTACIÓN', 'Latitud', 'Longitud', 'Departamento']).agg({'Precipitacion': 'sum'}).reset_index()
            zoom_ini = 9
        else:
            df_mapa = df.groupby(['NOMBRE_ESTACIÓN', 'Latitud', 'Longitud', 'Departamento']).agg({'Precipitacion': 'sum'}).reset_index()
            zoom_ini = 6.5
            
        neon_palette = ['#ff00ff', '#00ff00', '#e6e600', '#ff4500', '#00bfff', '#9400d3', '#ff1493', '#00fa9a', '#ffc400', '#ADFF2F']
        deptos_unicos = sorted(df_mapa['Departamento'].unique())
        color_map_deptos = {depto: neon_palette[i % len(neon_palette)] for i, depto in enumerate(deptos_unicos)}
        
        df_mapa['Color_Final'] = df_mapa.apply(lambda x: '#000000' if x['NOMBRE_ESTACIÓN'] == estacion_selec else color_map_deptos.get(x['Departamento'], '#555555'), axis=1)
        df_mapa['Size_Final'] = df_mapa['NOMBRE_ESTACIÓN'].apply(lambda x: 35 if x == estacion_selec else 14)

        fig_map = px.scatter_mapbox(df_mapa, lat="Latitud", lon="Longitud", hover_name="NOMBRE_ESTACIÓN", zoom=zoom_ini, mapbox_style="carto-positron", height=550, custom_data=['NOMBRE_ESTACIÓN', 'Departamento'])
        fig_map.update_traces(marker=dict(color=df_mapa['Color_Final'], size=df_mapa['Size_Final'], opacity=0.9, allowoverlap=True))
        fig_map.update_layout(clickmode='event+select', margin={"r":0,"t":0,"l":0,"b":0})
        
        event = st.plotly_chart(fig_map, on_select="rerun", selection_mode="points", use_container_width=True, key="mapa_main")
        
        if event and len(event['selection']['points']) > 0:
            punto = event['selection']['points'][0]
            estacion_click = punto['customdata'][0]
            depto_click = punto['customdata'][1]
            if estacion_click != st.session_state.estado_estacion:
                st.session_state.estado_depto = depto_click
                st.session_state.estado_estacion = estacion_click
                if 'sb_depto' in st.session_state: del st.session_state['sb_depto']
                if 'sb_estacion' in st.session_state: del st.session_state['sb_estacion']
                st.rerun()

        # TABLA
        with st.expander("📋 Ver Tabla de Datos Crudos"):
            st.dataframe(df_filtrado[['FECHA', 'NOMBRE_ESTACIÓN', 'Temp_Max', 'Temp_Min', 'Temp_Media', 'Precipitacion', 'Humedad']], use_container_width=True)

# PESTAÑA 2: COMPARATIVA
with tab_comp:
    if estacion_selec != 'Todas': st.markdown(f"### 🆚 Comparando: {estacion_selec}")
    if len(años_selec) < 2:
        st.info("💡 Selecciona al menos 2 años para comparar.")
    else:
        df_c = df_filtrado.groupby(['Año', 'Mes_Nombre'], observed=False).agg({'Precipitacion':'sum', 'Temp_Media':'mean', 'Humedad':'mean'}).reset_index()
        df_c['Año'] = df_c['Año'].astype(str)
        c1, c2 = st.columns(2)
        with c1: 
            st.plotly_chart(px.line(df_c, x='Mes_Nombre', y='Precipitacion', color='Año', title="🌧️ Lluvias Comparativas", template='plotly_dark', category_orders={"Mes_Nombre": ORDEN_MESES}), use_container_width=True)
        with c2: 
            st.plotly_chart(px.line(df_c, x='Mes_Nombre', y='Temp_Media', color='Año', title="🌡️ Temperaturas Comparativas", template='plotly_dark', category_orders={"Mes_Nombre": ORDEN_MESES}), use_container_width=True)
        st.plotly_chart(px.bar(df_c, x='Mes_Nombre', y='Humedad', color='Año', barmode='group', title="💨 Humedad Comparativa", template='plotly_dark', category_orders={"Mes_Nombre": ORDEN_MESES}), use_container_width=True)

# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 08:21:53 2022

@author: scedermas
"""
import pandas as pd
import sqlite3
import datetime as dt
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image

desde=dt.datetime.now()

con = sqlite3.connect("proyecciones_db_2023.db")

informe = st.sidebar.selectbox(
    'Elegí uno de los informes disponibles',
    ('Inicio', 'Dias', 'Ver Reductores', 'Editar Reductores', 'Dotacion', 'Resultados operativos', '4')
    )

if informe=="Inicio":
    st.title("Calculadora proyecciones")
    st.text("elegí una opcion...")
    image = Image.open('images.jfif')

    st.image(image, caption='P&L')

if informe=="Dias":
    df_dias=pd.read_sql('select * from s_dias', con)
    st.table(df_dias)

if informe=="Ver Reductores":
    df_kpi_operativos=pd.read_sql('select mes_anio, ausentismo_remunerado, ausentismo_no_remunerado, hs_sin_conexion, auxiliares_no_pagos, vacaciones, capa_inicial, over_under from kpis_operativos', con)
    st.table(df_kpi_operativos)
    
if informe=="Editar Reductores":
    ausentismo_remunerado=[]
    ausentismo_no_remunerado=[]
    hs_sin_conexion=[]
    auxiliares_no_pagos=[]
    vacaciones=[]
    capa_inicial=[]
    over_under=[]
    
    df_reductores=pd.read_sql('select * from kpis_operativos', con)
    with st.beta_expander("Ausentismo Remunerado"):
        for i in range (len(df_reductores)):
            ausentismo_remunerado.append(0)
            ausentismo_remunerado[i] = st.text_input("Mes:"+str(i+1), value=df_reductores.iloc[i][1], max_chars=6)
 
    with st.beta_expander("Ausentismo NO Remunerado"):
        for i in range (len(df_reductores)):
            ausentismo_no_remunerado.append(0)
            ausentismo_no_remunerado[i] = st.text_input("Mes :"+str(i+1), value=df_reductores.iloc[i][2], max_chars=6)

    with st.beta_expander("Horas sin conexion"):
        for i in range (len(df_reductores)):
            hs_sin_conexion.append(0)
            hs_sin_conexion[i] = st.text_input("Mes "+str(i+1), value=df_reductores.iloc[i][3], max_chars=6)

    with st.beta_expander("Auxiliares no pagos"):
        for i in range (len(df_reductores)):
            auxiliares_no_pagos.append(0)
            auxiliares_no_pagos[i] = st.text_input("Mes"+str(i+1), value=df_reductores.iloc[i][4], max_chars=6)
                  
    with st.beta_expander("Vacaciones"):
        for i in range (len(df_reductores)):
            vacaciones.append(0)
            vacaciones[i] = st.text_input("Mes_"+str(i+1), value=df_reductores.iloc[i][5], max_chars=6)
                  
    with st.beta_expander("Capa Inicial"):
        for i in range (len(df_reductores)):
            capa_inicial.append(0)
            capa_inicial[i] = st.text_input("Mes _"+str(i+1), value=df_reductores.iloc[i][8], max_chars=6)

    with st.beta_expander("Desperdicio Over/Under"):
        for i in range (len(df_reductores)):
            over_under.append(0)
            over_under[i] = st.text_input("Mes:_"+str(i+1), value=df_reductores.iloc[i][9], max_chars=6)
                                        
    cursorobj=con.cursor()
    
    
    figo = go.Figure()
    figo.add_trace(go.Scatter(x=df_reductores['mes_anio'], y=df_reductores['ausentismo_remunerado'],line=dict(color='black', width=2), name='Ausentismo NO remunerado'))
    figo.add_trace(go.Scatter(x=df_reductores['mes_anio'], y=df_reductores['ausentismo_no_remunerado'],line=dict(color='blue', width=3), name='Ausentismo remunerado'))
    figo.add_trace(go.Scatter(x=df_reductores['mes_anio'], y=df_reductores['hs_sin_conexion'],line=dict(color='brown', width=2), name='Hs sin conexion'))
    figo.add_trace(go.Scatter(x=df_reductores['mes_anio'], y=df_reductores['auxiliares_no_pagos'],line=dict(color='orange', width=3), name='Aux no pagos'))
    figo.add_trace(go.Scatter(x=df_reductores['mes_anio'], y=df_reductores['vacaciones'],line=dict(color='yellow', width=3), name='vacaciones'))
    figo.add_trace(go.Scatter(x=df_reductores['mes_anio'], y=df_reductores['capa_inicial'],line=dict(color='cyan', width=3), name='capa_inicial'))
    figo.add_trace(go.Scatter(x=df_reductores['mes_anio'], y=df_reductores['over_under'],line=dict(color='violet', width=3), name='over_under'))
                   
    figo.update_xaxes(type='category')
    figo.update_layout(height=550, width=1500)
    st.plotly_chart(figo, use_container_width=True)
      
    
    if st.button("Actualizar"):
        for i in range(12):
            cursorobj.execute('update kpis_operativos set ausentismo_remunerado="'+str(ausentismo_remunerado[i])+'" where cast(substr(mes_anio, 1,2) as int)='+str(i+1)+';')
            con.commit()
            cursorobj.execute('update kpis_operativos set ausentismo_no_remunerado="'+str(ausentismo_no_remunerado[i])+'" where cast(substr(mes_anio, 1,2) as int)='+str(i+1)+';')
            con.commit()
            cursorobj.execute('update kpis_operativos set hs_sin_conexion="'+str(hs_sin_conexion[i])+'" where cast(substr(mes_anio, 1,2) as int)='+str(i+1)+';')
            con.commit()      
            cursorobj.execute('update kpis_operativos set auxiliares_no_pagos="'+str(auxiliares_no_pagos[i])+'" where cast(substr(mes_anio, 1,2) as int)='+str(i+1)+';')
            con.commit()      
            cursorobj.execute('update kpis_operativos set vacaciones="'+str(vacaciones[i])+'" where cast(substr(mes_anio, 1,2) as int)='+str(i+1)+';')
            con.commit()      
            cursorobj.execute('update kpis_operativos set capa_inicial="'+str(capa_inicial[i])+'" where cast(substr(mes_anio, 1,2) as int)='+str(i+1)+';')
            con.commit()     
            cursorobj.execute('update kpis_operativos set over_under="'+str(over_under[i])+'" where cast(substr(mes_anio, 1,2) as int)='+str(i+1)+';')
            con.commit()   
            
            
if informe=="Dotacion":
    df_dotacion=pd.read_sql('select mes_anio, cantidad from dotacion', con)
    cantidad=[]
    for i in range (len(df_dotacion)):
        cantidad.append(0)
        cantidad[i] = st.text_input(" Mes:"+str(i+1), value=df_dotacion.iloc[i][1], max_chars=6)

    cursorobj=con.cursor()

    figd = go.Figure()
    figd.add_trace(go.Scatter(x=df_dotacion['mes_anio'], y=df_dotacion['cantidad'],line=dict(color='green', width=3), name='dotacion racs'))

    figd.update_xaxes(type='category')
    figd.update_layout(height=550, width=1500)
    st.plotly_chart(figd, use_container_width=True)

    
    if st.button("Actualizar dotacion"):
        for i in range(12):
            cursorobj.execute('update dotacion set cantidad="'+str(cantidad[i])+'" where cast(substr(mes_anio, 1,2) as int)='+str(i+1)+';')
            con.commit()


if informe=="Resultados operativos":
    df_resultados_operativos=pd.read_sql('select * from s_dotacion_hs_prod', con)
    st.table(df_resultados_operativos)

    df_resultados_operativos=df_resultados_operativos.reset_index()

    figr= go.Figure()
    figr.add_trace(go.Scatter(x=df_resultados_operativos['mes_anio'], y=df_resultados_operativos['progra_horas'],line=dict(color='black', width=3), name='Hs programadas'))
    figr.add_trace(go.Scatter(x=df_resultados_operativos['mes_anio'], y=df_resultados_operativos['horas_pagas'],line=dict(color='blue', width=3), name='Hs pagas'))
    figr.add_trace(go.Scatter(x=df_resultados_operativos['mes_anio'], y=df_resultados_operativos['horas_productivas'],line=dict(color='brown', width=3), name='Hs productivas'))
    figr.add_trace(go.Scatter(x=df_resultados_operativos['mes_anio'], y=df_resultados_operativos['horas_facturadas'],line=dict(color='green', width=3), name='Hs facturadas'))
    figr.update_xaxes(type='category')
    figr.update_layout(height=550, width=1500)
    st.plotly_chart(figr, use_container_width=True)


    figrd= go.Figure()
    figrd.add_trace(go.Scatter(x=df_resultados_operativos['mes_anio'], y=df_resultados_operativos['cantidad'],line=dict(color='black', width=3), name='Dotacion'))

    figrd.update_xaxes(type='category')
    figrd.update_layout(height=550, width=1500)
    st.plotly_chart(figrd, use_container_width=True)


    figrr= go.Figure()
    figrr.add_trace(go.Scatter(x=df_resultados_operativos['mes_anio'], y=df_resultados_operativos['rendimiento_prod'],line=dict(color='black', width=3), name='productivo/pago'))
    figrr.add_trace(go.Scatter(x=df_resultados_operativos['mes_anio'], y=df_resultados_operativos['rendimiento_pago'],line=dict(color='green', width=3), name='facturado/pago'))
    figrr.update_xaxes(type='category')
    figrr.update_layout(height=550, width=1500)
    st.plotly_chart(figrr, use_container_width=True)

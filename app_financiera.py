import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="App Financiera Constructora", layout="wide")
st.title("📈 Panel Financiero de Constructora")

archivo = st.file_uploader("Por favor, sube un archivo Excel con las hojas: Estado Resultados, Balance General, Flujo Efectivo, IVA Facturas", type=[".xlsx"])

if archivo:
    try:
        xls = pd.ExcelFile(archivo)

        # Cargar hojas
        df_resultados = pd.read_excel(xls, sheet_name="Estado Resultados")
        df_balance = pd.read_excel(xls, sheet_name="Balance General")
        df_flujo = pd.read_excel(xls, sheet_name="Flujo Efectivo")
        df_iva = pd.read_excel(xls, sheet_name="IVA Facturas")

        st.subheader("Estado de Resultados")
        st.dataframe(df_resultados)
        fig_resultados = px.bar(df_resultados, x="Tipo", y="Monto", title="Detalle Estado de Resultados")
        st.plotly_chart(fig_resultados, use_container_width=True)

        st.subheader("Balance General")
        st.dataframe(df_balance)
        fig_balance = px.bar(df_balance, x="Cuenta", y="Monto", title="Composición del Balance General")
        st.plotly_chart(fig_balance, use_container_width=True)

        st.subheader("Flujo de Efectivo")
        st.dataframe(df_flujo)
        fig_flujo = px.bar(df_flujo, x="Periodo", y=["Monto Entrada", "Monto Salida"], barmode="group", title="Flujo de Efectivo por Periodo")
        st.plotly_chart(fig_flujo, use_container_width=True)

        st.subheader("IVA por Facturas")
        st.dataframe(df_iva)
        iva_ventas = df_iva[df_iva["Tipo"] == "Factura Venta"]["IVA (19%)"].sum()
        iva_compras = df_iva[df_iva["Tipo"] == "Factura Compra"]["IVA (19%)"].sum()
        iva_pagar = iva_ventas - iva_compras

        st.metric("IVA Ventas", f"${iva_ventas:,.0f}")
        st.metric("IVA Compras", f"${iva_compras:,.0f}")
        st.metric("IVA a Pagar", f"${iva_pagar:,.0f}", delta=f"{'+' if iva_pagar >= 0 else ''}{iva_pagar:,.0f}")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

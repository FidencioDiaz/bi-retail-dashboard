"""
app.py
Executive Business Intelligence (BI) Dashboard para GlobalRetail Insights.
Construido con Streamlit, Plotly y Pandas.
"""

import datetime
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_generator import generate_sales_data

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="GlobalRetail Insights | Executive BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para tarjetas ejecutivas y aspecto moderno
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fc 100%);
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin: 4px 0;
    }
    .metric-delta-positive {
        font-size: 0.85rem;
        font-weight: 600;
        color: #16a34a;
    }
    .metric-delta-negative {
        font-size: 0.85rem;
        font-weight: 600;
        color: #dc2626;
    }
    .badge-filter {
        display: inline-block;
        background-color: #e0e7ff;
        color: #3730a3;
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. CARGA Y CACHÉ DE DATOS
# ==========================================
DATA_FILE = "sales_data.csv"

@st.cache_data(show_spinner="Cargando datos del almacén analítico...")
def load_data():
    if not os.path.exists(DATA_FILE):
        df = generate_sales_data(num_records=1800)
        df.to_csv(DATA_FILE, index=False, encoding="utf-8")
    else:
        df = pd.read_csv(DATA_FILE)
        df["order_date"] = pd.to_datetime(df["order_date"])
    return df

df_raw = load_data()


# ==========================================
# 3. BARRA LATERAL (FILTROS REACTIVOS)
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80", use_container_width=True)
st.sidebar.title("🎛️ Filtros de Control BI")
st.sidebar.markdown("Personaliza los parámetros del análisis en tiempo real.")

min_date = df_raw["order_date"].min().date()
max_date = df_raw["order_date"].max().date()

# Selector de Rango de Fechas
date_range = st.sidebar.date_input(
    "📅 Período de Análisis:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Filtro de Región
all_regions = sorted(df_raw["region"].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "🌍 Regiones Comerciales:",
    options=all_regions,
    default=all_regions
)

# Filtro de Categoría de Producto
all_categories = sorted(df_raw["category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "📦 Categorías de Producto:",
    options=all_categories,
    default=all_categories
)

# Filtro de Segmento de Cliente
all_segments = sorted(df_raw["customer_segment"].unique().tolist())
selected_segments = st.sidebar.multiselect(
    "👥 Segmento de Cliente:",
    options=all_segments,
    default=all_segments
)

# Filtro de Canal de Ventas
all_channels = ["Todos"] + sorted(df_raw["sales_channel"].unique().tolist())
selected_channel = st.sidebar.selectbox(
    "🛒 Canal de Venta:",
    options=all_channels,
    index=0
)

# Botón para regenerar datos sintéticos
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Generar Nuevos Datos Aleatorios"):
    df_new = generate_sales_data(num_records=1800, seed=int(datetime.datetime.now().timestamp()))
    df_new.to_csv(DATA_FILE, index=False, encoding="utf-8")
    st.cache_data.clear()
    st.rerun()


# ==========================================
# 4. APLICACIÓN DE FILTROS AL DATASET
# ==========================================
mask = (
    (df_raw["order_date"].dt.date >= start_date) &
    (df_raw["order_date"].dt.date <= end_date) &
    (df_raw["region"].isin(selected_regions)) &
    (df_raw["category"].isin(selected_categories)) &
    (df_raw["customer_segment"].isin(selected_segments))
)

if selected_channel != "Todos":
    mask = mask & (df_raw["sales_channel"] == selected_channel)

df_filtered = df_raw[mask].copy()


# ==========================================
# 5. ENCABEZADO Y CONTROL DE ESTADO VACÍO
# ==========================================
col_header, col_status = st.columns([3, 1])
with col_header:
    st.title("📊 GlobalRetail Insights")
    st.markdown("**Executive Business Intelligence Dashboard** | Análisis de Rendimiento Comercial, Rentabilidad y Clientes")

with col_status:
    st.write("")
    st.info(f"**Registros activos:** {len(df_filtered):,} de {len(df_raw):,}\n\n**Período:** {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}")

st.markdown("---")

if df_filtered.empty:
    st.warning("⚠️ No se encontraron transacciones para la combinación de filtros seleccionada. Por favor amplía los criterios en la barra lateral.")
    st.stop()


# ==========================================
# 6. TARJETAS DE KPIS EJECUTIVOS
# ==========================================
total_revenue = df_filtered["revenue"].sum()
total_profit = df_filtered["profit"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_orders = len(df_filtered)
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
avg_satisfaction = df_filtered["customer_rating"].mean()
total_units = df_filtered["quantity"].sum()

# Cálculo comparativo (primera mitad vs segunda mitad del período para obtener variación estimada)
median_date = start_date + (end_date - start_date) // 2
df_p1 = df_filtered[df_filtered["order_date"].dt.date < median_date]
df_p2 = df_filtered[df_filtered["order_date"].dt.date >= median_date]

rev_p1 = df_p1["revenue"].sum()
rev_p2 = df_p2["revenue"].sum()
delta_rev_pct = ((rev_p2 - rev_p1) / rev_p1 * 100) if rev_p1 > 0 else 0

profit_p1 = df_p1["profit"].sum()
profit_p2 = df_p2["profit"].sum()
delta_profit_pct = ((profit_p2 - profit_p1) / profit_p1 * 100) if profit_p1 > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    delta_class = "metric-delta-positive" if delta_rev_pct >= 0 else "metric-delta-negative"
    sign = "+" if delta_rev_pct >= 0 else ""
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #2563eb;">
        <div class="metric-label">Ingresos Totales</div>
        <div class="metric-value">${total_revenue:,.0f}</div>
        <div class="{delta_class}">{sign}{delta_rev_pct:.1f}% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    delta_class = "metric-delta-positive" if delta_profit_pct >= 0 else "metric-delta-negative"
    sign = "+" if delta_profit_pct >= 0 else ""
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #10b981;">
        <div class="metric-label">Beneficio Neto</div>
        <div class="metric-value">${total_profit:,.0f}</div>
        <div class="{delta_class}">Margen: {profit_margin:.1f}% ({sign}{delta_profit_pct:.1f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #f59e0b;">
        <div class="metric-label">Ticket Promedio (AOV)</div>
        <div class="metric-value">${avg_order_value:,.2f}</div>
        <div style="font-size: 0.85rem; color: #64748b;">{total_units:,} unidades vendidas</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #8b5cf6;">
        <div class="metric-label">Volumen de Pedidos</div>
        <div class="metric-value">{total_orders:,}</div>
        <div style="font-size: 0.85rem; color: #64748b;">Entrega prom.: {df_filtered['delivery_days'].mean():.1f} días</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #ec4899;">
        <div class="metric-label">Satisfacción Cliente</div>
        <div class="metric-value">{avg_satisfaction:.2f} <span style="font-size:1.1rem;">★</span></div>
        <div style="font-size: 0.85rem; color: #64748b;">Basado en calificaciones 1-5</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# 7. PESTAÑAS DE VISUALIZACIÓN BI
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tendencias Financieras",
    "📦 Categorías y Productos",
    "🌍 Análisis Geográfico & Canales",
    "📋 Explorador de Datos"
])


# --- PESTAÑA 1: TENDENCIAS FINANCIERAS ---
with tab1:
    st.subheader("Evolución Temporal de Ingresos y Beneficios")
    
    # Agrupación temporal dinámica (mensual o semanal)
    df_trend = df_filtered.copy()
    df_trend["period"] = df_trend["order_date"].dt.to_period("M").dt.to_timestamp()
    trend_group = df_trend.groupby("period")[["revenue", "profit"]].sum().reset_index()

    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(
        x=trend_group["period"],
        y=trend_group["revenue"],
        mode="lines+markers",
        name="Ingresos Brutos ($)",
        line=dict(color="#2563eb", width=3),
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.08)"
    ))
    fig_timeline.add_trace(go.Scatter(
        x=trend_group["period"],
        y=trend_group["profit"],
        mode="lines+markers",
        name="Beneficio Neto ($)",
        line=dict(color="#10b981", width=3, dash="dot"),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.08)"
    ))

    fig_timeline.update_layout(
        template="plotly_white",
        hovermode="x unified",
        height=380,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="Mes",
        yaxis_title="Monto ($ USD)"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("##### 💵 Distribución de Descuentos vs Margen")
        fig_discount = px.scatter(
            df_filtered,
            x="discount_pct",
            y="profit_margin_pct",
            color="category",
            size="revenue",
            hover_data=["subcategory", "customer_segment"],
            labels={"discount_pct": "Tasa de Descuento", "profit_margin_pct": "Margen de Beneficio (%)"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_discount.update_layout(template="plotly_white", height=320, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_discount, use_container_width=True)

    with col_t2:
        st.markdown("##### 🏆 Top 5 Subcategorías por Margen Absoluto")
        top_subcats = df_filtered.groupby("subcategory")["profit"].sum().nlargest(5).reset_index()
        fig_subcat = px.bar(
            top_subcats,
            x="profit",
            y="subcategory",
            orientation="h",
            text="profit",
            color="profit",
            color_continuous_scale="Viridis",
            labels={"profit": "Beneficio Total ($)", "subcategory": "Subcategoría"}
        )
        fig_subcat.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig_subcat.update_layout(template="plotly_white", height=320, margin=dict(l=10, r=30, t=20, b=10), showlegend=False)
        st.plotly_chart(fig_subcat, use_container_width=True)


# --- PESTAÑA 2: CATEGORÍAS Y PRODUCTOS ---
with tab2:
    st.subheader("Desglose y Rendimiento por Categoría")
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown("##### 📊 Ingresos vs Beneficios por Categoría")
        cat_summary = df_filtered.groupby("category")[["revenue", "profit"]].sum().reset_index()
        fig_cat_bar = go.Figure(data=[
            go.Bar(name="Ingresos", x=cat_summary["category"], y=cat_summary["revenue"], marker_color="#3b82f6"),
            go.Bar(name="Beneficio", x=cat_summary["category"], y=cat_summary["profit"], marker_color="#10b981")
        ])
        fig_cat_bar.update_layout(
            barmode="group",
            template="plotly_white",
            height=360,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_cat_bar, use_container_width=True)

    with col_c2:
        st.markdown("##### 🌳 Mapa Jerárquico de Ingresos (Treemap)")
        fig_tree = px.treemap(
            df_filtered,
            path=["category", "subcategory"],
            values="revenue",
            color="profit_margin_pct",
            color_continuous_scale="RdYlGn",
            labels={"revenue": "Ingresos ($)", "profit_margin_pct": "Margen Promedio (%)"}
        )
        fig_tree.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=360)
        st.plotly_chart(fig_tree, use_container_width=True)


# --- PESTAÑA 3: ANÁLISIS GEOGRÁFICO & CANALES ---
with tab3:
    st.subheader("Distribución Territorial y Canales Comerciales")
    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        st.markdown("##### 🌎 Ventas por País")
        geo_data = df_filtered.groupby(["country", "region"])[["revenue", "profit", "quantity"]].sum().reset_index()
        fig_geo = px.bar(
            geo_data.sort_values(by="revenue", ascending=True),
            x="revenue",
            y="country",
            color="region",
            orientation="h",
            text="revenue",
            labels={"revenue": "Ingresos ($)", "country": "País", "region": "Región"},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_geo.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig_geo.update_layout(template="plotly_white", height=420, margin=dict(l=20, r=30, t=20, b=20))
        st.plotly_chart(fig_geo, use_container_width=True)

    with col_g2:
        st.markdown("##### 🛒 Cuota por Canal de Venta")
        channel_data = df_filtered.groupby("sales_channel")["revenue"].sum().reset_index()
        fig_donut = px.pie(
            channel_data,
            values="revenue",
            names="sales_channel",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent+label")
        fig_donut.update_layout(template="plotly_white", height=420, showlegend=False, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_donut, use_container_width=True)


# --- PESTAÑA 4: EXPLORADOR DE DATOS ---
with tab4:
    st.subheader("Explorador de Registros y Descarga Analítica")
    st.markdown("Inspecciona las transacciones en detalle o descárgalas para análisis en herramientas externas (Excel, PowerBI, Tableau).")

    # Formato legible para visualización
    display_cols = [
        "order_id", "order_date", "region", "country", "customer_segment",
        "sales_channel", "category", "subcategory", "unit_price", "quantity",
        "discount_pct", "revenue", "profit", "profit_margin_pct", "customer_rating"
    ]
    df_display = df_filtered[display_cols].copy()
    df_display["order_date"] = df_display["order_date"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "order_id": "ID Pedido",
            "order_date": "Fecha",
            "region": "Región",
            "country": "País",
            "customer_segment": "Segmento",
            "sales_channel": "Canal",
            "category": "Categoría",
            "subcategory": "Subcategoría",
            "unit_price": st.column_config.NumberColumn("Precio Unitario", format="$%.2f"),
            "quantity": "Cant.",
            "discount_pct": st.column_config.NumberColumn("Desc.", format="%.0f%%"),
            "revenue": st.column_config.NumberColumn("Ingresos", format="$%.2f"),
            "profit": st.column_config.NumberColumn("Beneficio", format="$%.2f"),
            "profit_margin_pct": st.column_config.NumberColumn("Margen %", format="%.1f%%"),
            "customer_rating": st.column_config.NumberColumn("Rating", format="%d ⭐")
        }
    )

    # Botón de descarga CSV
    csv_bytes = df_filtered.to_csv(index=False, encoding="utf-8").encode("utf-8")
    st.download_button(
        label="📥 Descargar Dataset Filtrado en CSV",
        data=csv_bytes,
        file_name=f"globalretail_data_{datetime.date.today()}.csv",
        mime="text/csv"
    )

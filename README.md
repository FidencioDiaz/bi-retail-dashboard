# 📊 GlobalRetail Insights - BI Executive Dashboard

Dashboard interactivo de Inteligencia de Negocios (**Business Intelligence**) desarrollado en Python para monitoreo de métricas comerciales, rentabilidad, análisis geográfico y comportamiento de clientes.

---

## ✨ DEMO de la Aplicación:

https://fiden-retail-bi.streamlit.app/

---

## 🚀 Inicio Rápido (Cómo Ejecutar la Aplicación)

El entorno virtual `.venv` y todas las dependencias ya están instaladas y listas en este directorio.

### 1. Iniciar el Dashboard
Para lanzar la aplicación localmente, abre tu terminal en esta carpeta y ejecuta:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

*O si ya tienes el entorno activado:*
```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado en:
👉 **`http://localhost:8501`**

---

## 📁 Estructura del Proyecto

```
Antigravity_Test/
├── .venv/                   # Entorno virtual de Python (librerías aisladas)
├── data_generator.py        # Generador de transacciones realistas y KPIs
├── sales_data.csv           # Dataset de muestra con 1,500 pedidos generados
├── app.py                   # Código principal del Dashboard (Streamlit + Plotly)
├── requirements.txt         # Lista de dependencias (streamlit, plotly, pandas, numpy)
└── README.md                # Esta guía
```

---

## 🛠️ Tecnologías y Librerías Utilizadas

* **[Streamlit](https://streamlit.io/)**: Framework moderno para construir interfaces analíticas y dashboards reactivos en Python sin necesidad de escribir HTML/CSS o JavaScript manual.
* **[Plotly Express & Graph Objects](https://plotly.com/python/)**: Visualizaciones interactivas con tooltips detallados, zoom, selecciones y paletas de color ejecutivas.
* **[Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)**: Procesamiento de series temporales, agregaciones matemáticas (AOV, márgenes, variaciones porcentuales) y filtrado en memoria.

---

## 💡 Funcionalidades del Dashboard

1. **Barra Lateral de Filtros Reactivos:**
   * Selector dinámico de rango de fechas.
   * Filtros multiselección para Regiones (Norteamérica, Europa, Latinoamérica, Asia-Pacífico).
   * Filtros por Categorías de Producto y Segmentos de Cliente (B2B, B2C, Corporativo).
   * Selector de Canal de Ventas (Tienda Online, Venta Directa, Distribuidores, etc.).
   * Botón de regeneración de datos aleatorios para pruebas.
2. **KPIs Ejecutivos en Tarjetas Visuales:**
   * **Ingresos Totales ($)** con variación porcentual frente al período anterior.
   * **Beneficio Neto ($)** y **Margen de Ganancia (%)**.
   * **Ticket Promedio (AOV)** y total de unidades colocadas.
   * **Volumen Total de Pedidos** y tiempo promedio de entrega.
   * **Índice de Satisfacción (CSAT / NPS)** con calificación en estrellas.
3. **Pestañas de Análisis BI:**
   * **Tendencias Financieras:** Evolución temporal de ingresos vs beneficios y análisis de elasticidad de descuentos vs margen.
   * **Categorías y Productos:** Gráficos agrupados y Treemap jerárquico de ventas por producto.
   * **Análisis Geográfico & Canales:** Ingresos por país y cuota de mercado por canal de venta (gráfico Donut).
   * **Explorador de Datos:** Tabla paginada interactiva con formato numérico y botón de descarga directa a archivo CSV.

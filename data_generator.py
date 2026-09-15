"""
data_generator.py
Generador de datos sintéticos realistas de transacciones comerciales para el Dashboard de BI.
"""

import datetime
import numpy as np
import pandas as pd


def generate_sales_data(num_records: int = 1200, seed: int = 42) -> pd.DataFrame:
    """Genera un DataFrame estructurado con métricas de ventas y rendimiento comercial."""
    np.random.seed(seed)

    # Catálogo de productos y subcategorías con rangos de precio base
    catalog = {
        "Tecnología": {
            "subcategories": ["Laptops & Ultrabooks", "Smartphones 5G", "Monitores 4K", "Auriculares Inalámbricos", "Accesorios"],
            "base_price_range": (80, 1400),
            "cost_ratio": (0.60, 0.75)
        },
        "Mobiliario y Oficina": {
            "subcategories": ["Sillas Ergonómicas", "Escritorios Regulables", "Lámparas LED", "Organizadores"],
            "base_price_range": (40, 450),
            "cost_ratio": (0.50, 0.68)
        },
        "Moda y Calzado": {
            "subcategories": ["Calzado Deportivo", "Ropa Casual", "Accesorios y Bolsos", "Abrigos Técnicos"],
            "base_price_range": (25, 220),
            "cost_ratio": (0.35, 0.55)
        },
        "Hogar y Electro": {
            "subcategories": ["Cafeteras Express", "Aspiradoras Robot", "Purificadores de Aire", "Domótica"],
            "base_price_range": (50, 600),
            "cost_ratio": (0.55, 0.70)
        }
    }

    # Distribución geográfica
    geo_structure = {
        "Norteamérica": ["Estados Unidos", "Canadá", "México"],
        "Europa": ["España", "Alemania", "Reino Unido", "Francia"],
        "Latinoamérica": ["Colombia", "Chile", "Argentina", "Brasil", "Perú"],
        "Asia-Pacífico": ["Japón", "Australia", "Singapur", "Corea del Sur"]
    }

    segments = ["Consumidor Final (B2C)", "Empresas (B2B)", "Corporativo"]
    channels = ["Tienda Online", "Venta Directa", "Distribuidores", "Marketplace"]

    categories = list(catalog.keys())
    regions = list(geo_structure.keys())

    # Generación de fechas (últimos 12 meses hasta hoy)
    end_date = datetime.date(2026, 9, 1)
    start_date = end_date - datetime.timedelta(days=365)
    days_range = (end_date - start_date).days

    records = []
    for i in range(1, num_records + 1):
        order_id = f"ORD-{20250000 + i}"
        
        # Fecha aleatoria con ligera ponderación de estacionalidad
        random_day = int(np.random.beta(2, 2) * days_range)
        order_date = start_date + datetime.timedelta(days=random_day)

        category = np.random.choice(categories, p=[0.38, 0.22, 0.20, 0.20])
        cat_info = catalog[category]
        subcategory = np.random.choice(cat_info["subcategories"])

        region = np.random.choice(regions, p=[0.35, 0.30, 0.20, 0.15])
        country = np.random.choice(geo_structure[region])

        segment = np.random.choice(segments, p=[0.55, 0.30, 0.15])
        channel = np.random.choice(channels, p=[0.45, 0.25, 0.20, 0.10])

        # Precios y cantidades según segmento
        base_min, base_max = cat_info["base_price_range"]
        unit_price = round(float(np.random.uniform(base_min, base_max)), 2)

        if segment == "Corporativo":
            quantity = int(np.random.randint(5, 25))
            discount = round(float(np.random.choice([0.10, 0.15, 0.20, 0.25])), 2)
        elif segment == "Empresas (B2B)":
            quantity = int(np.random.randint(2, 10))
            discount = round(float(np.random.choice([0.05, 0.10, 0.15])), 2)
        else:
            quantity = int(np.random.randint(1, 4))
            discount = round(float(np.random.choice([0.00, 0.05, 0.10])), 2)

        gross_revenue = round(unit_price * quantity, 2)
        revenue = round(gross_revenue * (1 - discount), 2)

        c_min, c_max = cat_info["cost_ratio"]
        unit_cost = unit_price * np.random.uniform(c_min, c_max)
        cost = round(unit_cost * quantity, 2)
        profit = round(revenue - cost, 2)
        profit_margin = round((profit / revenue) * 100, 2) if revenue > 0 else 0.0

        customer_rating = int(np.random.choice([3, 4, 5], p=[0.10, 0.35, 0.55]))
        delivery_days = int(np.random.randint(1, 6))

        records.append({
            "order_id": order_id,
            "order_date": pd.to_datetime(order_date),
            "region": region,
            "country": country,
            "customer_segment": segment,
            "sales_channel": channel,
            "category": category,
            "subcategory": subcategory,
            "unit_price": unit_price,
            "quantity": quantity,
            "discount_pct": discount,
            "gross_revenue": gross_revenue,
            "revenue": revenue,
            "cost": cost,
            "profit": profit,
            "profit_margin_pct": profit_margin,
            "customer_rating": customer_rating,
            "delivery_days": delivery_days
        })

    df = pd.DataFrame(records)
    # Ordenar por fecha
    df = df.sort_values(by="order_date").reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = generate_sales_data(1500)
    output_path = "sales_data.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Dataset generado exitosamente con {len(df)} registros en '{output_path}'.")
    print(f"Columnas: {list(df.columns)}")
    print(f"Total Ingresos: ${df['revenue'].sum():,.2f} | Total Beneficio: ${df['profit'].sum():,.2f}")

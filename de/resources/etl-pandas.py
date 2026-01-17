import pandas as pd

# ========== E ==========
df_products = pd.read_csv("pdi_product.csv")
df_manufacturers = pd.read_csv("pdi_manufacturer.csv", sep=";")

# ========== T ==========
# Filtramos los productos de la categoría Mix
df_products_filtered = df_products.where(df_products["Category"] == "Mix")
# Join de productos con fabricantes
df_joined = df_products_filtered.merge(
    df_manufacturers,
    on="ManufacturerID",
    how="left"
)
# Creamos la nueva columna
df_joined["ProductAndManufacturer"] = (
    df_joined["Product"] + " (" + df_joined["Manufacturer"] + ")"
)

# ========== L ==========
df_joined.to_json("pdi_product_mix.json", orient="records", lines=True,)

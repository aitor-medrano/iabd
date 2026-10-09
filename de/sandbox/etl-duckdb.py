import duckdb

# ========== E ==========
duckdb.execute("""
CREATE VIEW productos AS
SELECT *
FROM read_csv('pdi_product.csv', header=true);
""")

duckdb.execute("""
CREATE VIEW fabricantes AS
SELECT *
FROM read_csv('pdi_manufacturer.csv', header=true, delim=';');
""")

# ========== T ==========
duckdb.execute("""
CREATE VIEW productos_plus AS
SELECT
    p.ProductID,
    p.Product,
    p.Category,
    p.Segment,
    p.ManufacturerID,
    f.Manufacturer,
    p.Product || ' (' || f.Manufacturer || ')' AS ProductNombreCompleto
FROM productos p
    LEFT JOIN fabricantes f
    ON p.ManufacturerID = f.ManufacturerID
WHERE p.Category = 'Mix';
""")

# ========== L ==========
duckdb.execute("""
COPY productos_plus
TO 'pdi_product_mix_ddb.json'
""")

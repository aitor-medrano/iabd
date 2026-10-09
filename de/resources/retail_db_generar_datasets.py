"""
Genera dos ficheros derivados de retail_db para la sesion de modelado dimensional:

  1. clientes_historico.csv : 5 extracciones trimestrales de la tabla `customers`,
     con cambios reales entre extracciones -> materia prima para una SCD tipo 2.
  2. stock_diario.csv       : existencias diarias por producto y almacen
                              -> snapshot periodico con metricas de los 3 tipos.

Reproducible: semilla fija. Requiere los CSV originales de retail_db.
"""
import duckdb
import random
import csv
import datetime as dt
from pathlib import Path

SEED = 20260723
random.seed(SEED)

BASE = Path("/home/claude/data/retail_db")
OUT = Path("/mnt/user-data/outputs")
OUT.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(":memory:")
for t in ["customers", "orders", "order_items", "products"]:
    con.execute(
        f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{BASE}/retail_db_{t}.csv')"
    )

# ---------------------------------------------------------------- 1. CLIENTES
EXTRACCIONES = [
    dt.date(2013, 7, 1),
    dt.date(2013, 10, 1),
    dt.date(2014, 1, 1),
    dt.date(2014, 4, 1),
    dt.date(2014, 7, 1),
]

COLS = [
    "customer_id", "customer_fname", "customer_lname", "customer_email",
    "customer_street", "customer_city", "customer_state", "customer_zipcode",
]

clientes = {
    r[0]: dict(zip(COLS, r))
    for r in con.execute(f"SELECT {','.join(COLS)} FROM customers ORDER BY customer_id").fetchall()
}
ids = sorted(clientes)

# ubicaciones reales del propio dataset, para que los cambios sean coherentes
ubicaciones = con.execute(
    "SELECT DISTINCT customer_street, customer_city, customer_state, customer_zipcode FROM customers"
).fetchall()

primer_pedido = dict(
    con.execute(
        "SELECT order_customer_id, CAST(min(order_date) AS DATE) FROM orders GROUP BY 1"
    ).fetchall()
)

# --- altas: clientes que aparecen en una extraccion posterior.
# Solo se eligen clientes cuyo primer pedido es posterior a esa fecha, para no
# generar hechos anteriores a la existencia de la dimension.
altas = {}
usados = set()
for fecha, cuantos in [(EXTRACCIONES[1], 150), (EXTRACCIONES[2], 100), (EXTRACCIONES[3], 50)]:
    candidatos = [
        c for c in ids
        if c not in usados and c in primer_pedido and primer_pedido[c] >= fecha
    ]
    elegidos = random.sample(candidatos, cuantos)
    for c in elegidos:
        altas[c] = fecha
        usados.add(c)

base_ids = [c for c in ids if c not in altas]

# --- mudanzas y correcciones
disponibles = [c for c in base_ids]
random.shuffle(disponibles)
mudanza_1 = set(disponibles[:600])
mudanza_2 = set(disponibles[600:720])
typo_lname = set(disponibles[720:870])

# a quien se muda, en que extraccion le toca (nunca en la primera)
cuando_muda = {}
for c in mudanza_1:
    cuando_muda[c] = [random.choice(EXTRACCIONES[1:])]
for c in mudanza_2:
    f1, f2 = sorted(random.sample(EXTRACCIONES[1:], 2))
    cuando_muda[c] = [f1, f2]
cuando_corrige = {c: random.choice(EXTRACCIONES[1:]) for c in typo_lname}


def con_typo(apellido: str) -> str:
    """Introduce una errata plausible: elimina una letra interior."""
    if len(apellido) < 4:
        return apellido + apellido[-1]
    i = random.randint(1, len(apellido) - 2)
    return apellido[:i] + apellido[i + 1:]


apellido_erroneo = {c: con_typo(clientes[c]["customer_lname"]) for c in typo_lname}


def nueva_ubicacion(estado_actual: str):
    """Devuelve una ubicacion real del dataset cuyo estado sea distinto del actual,
    para que toda mudanza simulada produzca de verdad una version nueva."""
    while True:
        u = random.choice(ubicaciones)
        if u[2] != estado_actual:
            return u


nuevas_ubis = {}
for c in cuando_muda:
    estado = clientes[c]["customer_state"]
    destinos = []
    for _ in cuando_muda[c]:
        u = nueva_ubicacion(estado)
        destinos.append(u)
        estado = u[2]
    nuevas_ubis[c] = destinos

filas_clientes = []
for fecha in EXTRACCIONES:
    for c in ids:
        if c in altas and fecha < altas[c]:
            continue  # todavia no existe
        r = dict(clientes[c])
        # apellido: erroneo hasta que se corrige
        if c in typo_lname and fecha < cuando_corrige[c]:
            r["customer_lname"] = apellido_erroneo[c]
        # ubicacion: la ultima mudanza cuya fecha ya ha ocurrido
        if c in cuando_muda:
            for i, f in enumerate(cuando_muda[c]):
                if fecha >= f:
                    calle, ciudad, estado, cp = nuevas_ubis[c][i]
                    r["customer_street"], r["customer_city"] = calle, ciudad
                    r["customer_state"], r["customer_zipcode"] = estado, cp
        filas_clientes.append([fecha.isoformat()] + [r[k] for k in COLS])

ruta_clientes = OUT / "retail_db_clientes_historico.csv"
with open(ruta_clientes, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["extract_date"] + COLS)
    w.writerows(filas_clientes)

# ------------------------------------------------------------------ 2. STOCK
ALMACENES = ["ALMACEN_NORTE", "ALMACEN_CENTRO", "ALMACEN_SUR"]
PESOS = [0.45, 0.33, 0.22]

ventas = con.execute(
    """
    SELECT CAST(o.order_date AS DATE) AS fecha,
           oi.order_item_product_id   AS product_id,
           SUM(oi.order_item_quantity) AS unidades
    FROM orders o
    JOIN order_items oi ON oi.order_item_order_id = o.order_id
    GROUP BY ALL
    """
).fetchall()

demanda = {}
for fecha, pid, uds in ventas:
    demanda.setdefault(pid, {})[fecha] = int(uds)

productos = sorted(demanda)
precio = dict(con.execute("SELECT product_id, product_price FROM products").fetchall())

fecha_ini = min(f for f, _, _ in ventas)
fecha_fin = max(f for f, _, _ in ventas)
dias = [fecha_ini + dt.timedelta(days=i) for i in range((fecha_fin - fecha_ini).days + 1)]


def reparte(total: int) -> list:
    """Reparte unidades entre almacenes conservando el total exacto."""
    if total == 0:
        return [0, 0, 0]
    trozos = [int(total * p) for p in PESOS]
    resto = total - sum(trozos)
    for _ in range(resto):
        trozos[random.randrange(3)] += 1
    return trozos


filas_stock = []
for pid in productos:
    coste = round(precio.get(pid, 0) * 0.6, 2)
    # El reparto entre almacenes se decide UNA vez por dia, para que la suma de
    # los tres almacenes coincida exactamente con las unidades de order_items.
    reparto = {d: reparte(demanda[pid].get(d, 0)) for d in dias}

    for j, alm in enumerate(ALMACENES):
        serie = [reparto[d][j] for d in dias]
        media_alm = max(sum(serie) / len(dias), 0.5)
        pico = max(serie) if serie else 0
        # se dimensiona contra el pico, no solo contra la media: la demanda es
        # muy irregular (mediana 5 uds/dia, percentil 99 en 249)
        punto_pedido = int(max(media_alm * 15, pico * 4, 15))
        lote = int(max(media_alm * 30, pico * 8, 30))
        stock = int(max(media_alm * 45, pico * 10, 40))
        pendientes = {}
        for d, vendidas in zip(dias, serie):
            recibidas = pendientes.pop(d, 0)
            inicial = stock
            stock += recibidas
            if vendidas > stock:
                raise RuntimeError(f"rotura de stock en {pid}/{alm}/{d}")
            stock -= vendidas
            filas_stock.append(
                [d.isoformat(), pid, alm, inicial, recibidas, vendidas, stock, coste]
            )
            if stock < punto_pedido and len(pendientes) < 2:
                pendientes[d + dt.timedelta(days=random.randint(2, 4))] = lote

ruta_stock = OUT / "retail_db_stock_diario.csv"
with open(ruta_stock, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([
        "fecha", "product_id", "almacen", "stock_inicial",
        "unidades_recibidas", "unidades_vendidas", "stock_final", "coste_unitario",
    ])
    w.writerows(filas_stock)

print("retail_db_clientes_historico.csv:", len(filas_clientes), "filas")
print("retail_db_stock_diario.csv:", len(filas_stock), "filas")
print("productos:", len(productos), "dias:", len(dias), "almacenes:", len(ALMACENES))

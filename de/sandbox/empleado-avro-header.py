raw = open("empleados.avro", "rb").read()

# Los "números mágicos" que identifican un fichero Avro
print(f"Números mágicos: {raw[:4]}")

# El sync marker son los últimos 16 bytes (cierran el último bloque)
sync = raw[-16:]
print(f"Sync marker: {sync.hex()}")

# Aparece dos veces: al final de la cabecera y al cerrar el único bloque
print(f"Veces que aparece en el fichero: {raw.count(sync)}")
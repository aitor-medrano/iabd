import pyarrow.parquet as pq

pf = pq.ParquetFile('pdi_sales.parquet')
md = pf.metadata
print(f"Filas: {md.num_rows} | Row groups: {md.num_row_groups}")

cabecera = (f"  {'columna':<10} {'compr.':<8} {'codificación':<28} "
            f"{'codificado':>11} {'comprimido':>11} {'ratio':>6}  "
            f"{'min':<14} {'max':<14} {'nulos':>6}")

for r in range(md.num_row_groups):
    rg = md.row_group(r)
    print(f"\n--- Row group {r}: {rg.num_rows} filas, {rg.total_byte_size/1024**2:.1f} MiB ---")
    print(cabecera)
    for i in range(rg.num_columns):
        col = rg.column(i)
        st = col.statistics
        sin, con = col.total_uncompressed_size, col.total_compressed_size
        linea = (f"  {col.path_in_schema:<10} {str(col.compression):<8} "
                 f"{', '.join(col.encodings):<28} "
                 f"{sin/1024:>7.1f} KiB {con/1024:>7.1f} KiB {sin/con:>5.1f}x  ")
        if st is None:
            print(linea + "(sin estadísticas)")
        else:
            print(linea + f"{str(st.min)[:14]:<14} {str(st.max)[:14]:<14} {st.null_count:>6}")
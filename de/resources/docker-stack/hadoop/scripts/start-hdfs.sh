#!/bin/bash
# Arranque del NameNode: formatea el sistema de ficheros HDFS únicamente
# la primera vez (cuando aún no existe el directorio "current" de metadatos).
set -e

NAME_DIR=/opt/hadoop/dfs/name

if [ ! -d "${NAME_DIR}/current" ]; then
  echo ">> HDFS sin formatear. Formateando NameNode..."
  hdfs namenode -format -force -nonInteractive
else
  echo ">> NameNode ya formateado. Se conserva el estado existente."
fi

echo ">> Arrancando NameNode..."
exec hdfs namenode

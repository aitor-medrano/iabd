# Imagen de Hive (Metastore + HiveServer2) con el driver JDBC de MySQL incorporado.
# La imagen oficial no trae el conector, así que lo añadimos a /opt/hive/lib.
ARG HIVE_VERSION=4.1.0
FROM apache/hive:${HIVE_VERSION}

# Versión del conector MySQL Connector/J (compatible con MySQL 8.x)
ARG MYSQL_CONNECTOR_VERSION=8.4.0

USER root
ADD https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/${MYSQL_CONNECTOR_VERSION}/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar \
    /opt/hive/lib/mysql-connector-j.jar
RUN chmod 644 /opt/hive/lib/mysql-connector-j.jar

# Jar de Hadoop AWS y bundle para acceder a MinIO (S3)
RUN cp /opt/hadoop/share/hadoop/tools/lib/hadoop-aws-*.jar \
    /opt/hadoop/share/hadoop/tools/lib/bundle-*.jar \
    /opt/hive/lib/

USER hive


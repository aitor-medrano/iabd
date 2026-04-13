# ---- Stage 1: Copiar Spark desde la misma imagen del cluster ----
FROM apache/spark:4.1.1 AS spark-base

# ---- Stage 2: Imagen ligera con Jupyter ----
FROM python:3.10-slim

# Java 21 (necesario para Spark)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-21-jre-headless \
        curl \
        procps \
        tini && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# Copiar Spark completo desde la imagen oficial (misma version que el cluster)
COPY --from=spark-base /opt/spark /opt/spark

ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"
ENV PYTHONPATH="${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.9.9-src.zip:${PYTHONPATH}"

# JupyterLab + librerias esenciales (NO instalar pyspark via pip)
RUN pip install --no-cache-dir \
    jupyterlab \
    pyarrow \
    pandas \
    numpy

# Directorio de trabajo
RUN useradd -m -s /bin/bash spark
USER spark
WORKDIR /home/spark/work

EXPOSE 8888 4040

ENTRYPOINT ["tini", "--"]
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", \
     "--IdentityProvider.token=spark"]

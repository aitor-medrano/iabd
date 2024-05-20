FROM alpine:latest

# Instalar dependencias necesarias
RUN apk update
RUN apk add --no-cache python3 py3-pip py3-setuptools
RUN apk add bash \
    && apk add curl zip git unzip iputils
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install -i /usr/local/aws-cli -b /usr/local/bin \
    && rm awscliv2.zip
RUN pip install boto3 --break-system-packages
RUN pip install pymongo --break-system-packages

# Crear un directorio de trabajo
WORKDIR /app

# Copiar cualquier script o archivo necesario a la imagen (opcional)
COPY scripts/prueba.py /app/

# Comando por defecto
CMD ["python3"]
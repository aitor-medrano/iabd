
docker run -p 8086:8086 -v "./data:/var/lib/influxdb2" -v "./config:/etc/influxdb2" influxdb:2

docker exec influxdb influx setup --username iabd --password iabd --org s8a --bucket h2v --force

docker run --name influxdb -d -p 8086:8086 -v "./data:/var/lib/influxdb2" -v "./config:/etc/influxdb2" -e DOCKER_INFLUXDB_INIT_MODE=setup -e DOCKER_INFLUXDB_INIT_USERNAME=iabd -e DOCKER_INFLUXDB_INIT_PASSWORD=IABDs8a. -e DOCKER_INFLUXDB_INIT_ORG=s8a -e DOCKER_INFLUXDB_INIT_BUCKET=h2v influxdb

Operator API Token
UWavL-R4L0UgLeYeXI8IUXgF-jMVLKzdXD6uR86z7TF7RPW_TAnox1mrDzt5aDCkTh-TZSBVn9ajCWA6uvsrmg==
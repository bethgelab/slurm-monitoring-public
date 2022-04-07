up-influx:
			docker-compose up -d influxdb

up-grafana:
			docker-compose up -d grafana

# Start Collecting
start-collection:
			./start-collecting.sh
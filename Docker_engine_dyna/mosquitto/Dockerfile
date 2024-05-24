FROM eclipse-mosquitto

WORKDIR /mosquitto

COPY config/mosquitto.conf /mosquitto/config/mosquitto.conf

VOLUME /mosquitto/data
VOLUME /mosquitto/logs

CMD ["mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]

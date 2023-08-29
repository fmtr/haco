#!/usr/bin/with-contenv bashio

export HACO_IS_ADDON=true
export HACO_CONFIGS_PATH="/config/haco"
export MQTT_HOST="$(bashio::services mqtt 'host')"
export MQTT_PASSWORD="$(bashio::services mqtt 'password')"
export MQTT_PORT="$(bashio::services mqtt 'port')"
export MQTT_USERNAME="$(bashio::services mqtt 'username')"

haco-daemon
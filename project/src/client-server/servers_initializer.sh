#!/bin/bash


# Server settings
NUMBER_OF_SERVERS=3
FIRST_SERVER_PORT=3030

SERVER_PORT=$FIRST_SERVER_PORT

# Terminal settings / variables
TAB="--tab"
SERVER_START_CMD_QUERY=""
FOLDER_CREATION_CDM_QUERY=""

# Auxiliar Variables
LAST_SERVER_PORT=$((FIRST_SERVER_PORT+NUMBER_OF_SERVERS-1))
START=1
FOLDER_PATH="../outputs/server_id_"
SERVERS_INFO=$"server_id,server_port\n"

# setting up servers_info.txt
for i in $(eval echo "{$START..$NUMBER_OF_SERVERS}")
do
  SERVERS_INFO+=$"$i,$SERVER_PORT\n"
  SERVER_PORT=$((SERVER_PORT+1))
done

for i in $(eval echo "{$START..$NUMBER_OF_SERVERS}")
do
  CMD="python server.py '$i' '$NUMBER_OF_SERVERS' '$FIRST_SERVER_PORT'"


  FIRST_SERVER_PORT=$((FIRST_SERVER_PORT+1))

  SERVER_START_CMD_QUERY+=($TAB -e "$CMD")

  FOLDER_NAME="$FOLDER_PATH$i"

  mkdir -p "$FOLDER_NAME"
  # mkdir -p "$FOLDER_NAME/dataLocation"
  mkdir -p "$FOLDER_NAME/graphData"

  echo -e $SERVERS_INFO > "$FOLDER_NAME/servers_info.txt"

done

gnome-terminal "${SERVER_START_CMD_QUERY[@]}"

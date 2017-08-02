#!/bin/bash

# Server settings
NUMBER_OF_SERVERS=`awk '/number_of_servers/ {print $2}' config.json`
# echo $NUMBER_OF_SERVERS

SERVER_PORT=$FIRST_THRIFT_SERVER_PORT

# Terminal settings / variables
TAB="--tab"
SERVER_START_CMD_QUERY=""
FOLDER_CREATION_CDM_QUERY=""

# Auxiliar Variables
START=1
FOLDER_PATH="../outputs/server_id_"


for i in $(eval echo "{$START..$NUMBER_OF_SERVERS}")
do
  for j in $(eval echo "{$START..$NUMBER_OF_SERVERS}")
  do
    
    CMD="python server.py $i $j"
    # echo dbg $CMD
  
    SERVER_START_CMD_QUERY+=($TAB -e "$CMD")

    FOLDER_NAME="$FOLDER_PATH$i"

    mkdir -p "$FOLDER_NAME"
  done
done

gnome-terminal "${SERVER_START_CMD_QUERY[@]}"

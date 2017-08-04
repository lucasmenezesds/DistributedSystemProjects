#!/bin/bash

# alias roda='./tmux_init.sh ; tmux kill-session; tmux ls'

# Server settings
NUMBER_OF_SERVERS=`awk '/number_of_servers/ {print $2}' config.json`
# echo $NUMBER_OF_SERVERS

tmux \
  new-session          "echo command1 ; ./server.py 1 1 ; read" \; \
  split-window -p 66 -t 0 -h "echo command2 ; ./server.py 1 2 ; read" \; \
  split-window -p 50 -t 1 -h "echo command3 ; ./server.py 1 3 ; read" \; \
  split-window -p 66 -t 0 -v "echo command4 ; ./server.py 2 1 ; read" \; \
  split-window -p 50 -t 3 -v "echo command7 ; ./server.py 3 1 ; read" \; \
  split-window -p 66 -t 1 -v "echo command5 ; ./server.py 2 2 ; read" \; \
  split-window -p 50 -t 5 -v "echo command8 ; ./server.py 3 2 ; read" \; \
  split-window -p 66 -t 2 -v "echo command6 ; ./server.py 2 3 ; read" \; \
  split-window -p 50 -t 7 -v "echo command9 ; ./server.py 3 3 ; read" \; \
  bind -n C-x setw synchronize-panes on
  bind -n M-x setw synchronize-panes off
  # setw synchronize-panes on
  # select-layout even-vertical
  # select-layout even-horizontal
  # select-layout tiled
  # set-remain-on-exit on



tmux kill-session;
tmux ls;
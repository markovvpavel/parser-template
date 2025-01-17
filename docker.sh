#!/bin/bash

MODE=$1
ACTION=$2

# Check for valid mode
if [ "$MODE" != "prod" ] && [ "$MODE" != "dev" ]; then
    echo "usage: $0 {prod|dev} {up|down}"
    exit 1
fi

# Check for valid action
if [ "$ACTION" != "up" ] && [ "$ACTION" != "down" ]; then
    echo "usage: $0 {prod|dev} {up|down}"
    exit 1
fi

# Set Dockerfile based on mode
if [ "$MODE" == "prod" ]; then
    DOCKERFILE="docker/Dockerfile.prod"
elif [ "$MODE" == "dev" ]; then
    DOCKERFILE="docker/Dockerfile.dev"
fi

if [ "$ACTION" == "up" ]; then
    echo "starting in $MODE mode..."
    if [ "$MODE" == "prod" ]; then
        DOCKERFILE=$DOCKERFILE docker compose -f compose.yml up --build --remove-orphans -d
    elif [ "$MODE" == "dev" ]; then
        DOCKERFILE=$DOCKERFILE docker compose -f compose.yml up --build --remove-orphans
    fi
elif [ "$ACTION" == "down" ]; then
    echo "stopping in $MODE mode..."
    docker compose -f compose.yml down
fi

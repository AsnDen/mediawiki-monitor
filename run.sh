#!/usr/bin/env bash
docker compose -f compose.yaml up --build "$@"
read -p "Press Enter to continue..."

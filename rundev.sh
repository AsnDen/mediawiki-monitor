#!/usr/bin/env bash
docker compose -f compose.yaml -f compose.dev.yaml up --build "$@"
read -p "Press Enter to continue..."

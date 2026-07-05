@echo off
set ARGS=%*
docker compose -f compose.yaml -f compose.dev.yaml up --build %ARGS%

@echo off
set ARGS=%*
docker compose -f compose.yaml up --build %ARGS%
pause

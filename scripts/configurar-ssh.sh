#!/usr/bin/env bash
set -euo pipefail

: "${DEPLOY_HOST:?Falta el secreto DEPLOY_HOST}"
: "${DEPLOY_USER:?Falta el secreto DEPLOY_USER}"
: "${DEPLOY_PORT:?Falta el secreto DEPLOY_PORT}"
: "${DEPLOY_KEY:?Falta el secreto DEPLOY_KEY}"
: "${DEPLOY_KNOWN_HOSTS:?Falta la variable DEPLOY_KNOWN_HOSTS}"
[[ "$DEPLOY_HOST" =~ ^[A-Za-z0-9._:-]+$ ]]
[[ "$DEPLOY_USER" =~ ^[a-zA-Z0-9_][a-zA-Z0-9_-]*$ ]]
[[ "$DEPLOY_PORT" =~ ^[0-9]{1,5}$ ]]
(( 10#$DEPLOY_PORT >= 1 && 10#$DEPLOY_PORT <= 65535 ))

directorio=$1
umask 077
mkdir -p "$directorio"
printf '%s\n' "$DEPLOY_KEY" | tr -d '\r' > "$directorio/credencial"
printf '%s\n' "$DEPLOY_KNOWN_HOSTS" | tr -d '\r' > "$directorio/known_hosts"
cat > "$directorio/ssh_config" <<CONFIG
Host inventario
  HostName $DEPLOY_HOST
  Port $DEPLOY_PORT
  User $DEPLOY_USER
  IdentityFile "$directorio/credencial"
  UserKnownHostsFile "$directorio/known_hosts"
  StrictHostKeyChecking yes
  IdentitiesOnly yes
  BatchMode yes
  ConnectTimeout 10
CONFIG

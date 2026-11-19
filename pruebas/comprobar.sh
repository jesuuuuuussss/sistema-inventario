#!/usr/bin/env bash
set -euo pipefail

directorio=$1
base_datos=$2
accion=$3
consulta=${4:-PR7-001}
puerto=${INVENTARIO_TEST_PORT:-8765}
version=$(cat "$directorio/VERSION")
registro=$(mktemp)
python3 "$directorio/src/main.py" --port "$puerto" --db "$base_datos" > "$registro" 2>&1 &
proceso=$!
limpiar() {
  kill "$proceso" 2>/dev/null || true
  wait "$proceso" 2>/dev/null || true
  cat "$registro"
  rm -f -- "$registro"
}
trap limpiar EXIT

printf 'Comprobación de %s en %s (%s)\n' "$version" "$(hostname)" "$accion"
python3 "$directorio/pruebas/verificar.py" --url "http://127.0.0.1:$puerto" \
  --version "$version" --accion "$accion" --consulta "$consulta"

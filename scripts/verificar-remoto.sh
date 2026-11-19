#!/usr/bin/env bash
set -euo pipefail

configuracion=$1
tag=$2
anterior=${3:-}
filtro=${4:-PR7-001}
[[ "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]
[[ -z "$anterior" || "$anterior" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]
[[ "$filtro" =~ ^[A-Za-z0-9-]+$ ]]

ssh -F "$configuracion" inventario bash -s -- "$tag" "'$anterior'" "$filtro" <<'REMOTO'
set -euo pipefail
tag=$1
anterior=$2
filtro=$3
base="$HOME/sistema-inventario"
nueva="$base/versiones/$tag"
mkdir -p "$base/datos"
datos=$(mktemp -d "$base/datos/prueba.XXXXXXXX")
db="$datos/inventario.sqlite3"
printf 'Equipo de destino: %s\n' "$(hostname)"
uname -srm
python3 --version

if [[ -z "$anterior" ]]; then
  bash "$nueva/pruebas/comprobar.sh" "$nueva" "$db" registrar
  exit 0
fi

estable="$base/versiones/$anterior"
printf '\nVersión estable antes del cambio\n'
bash "$estable/pruebas/comprobar.sh" "$estable" "$db" registrar

printf '\nVerificación de la segunda versión\n'
bash "$nueva/pruebas/comprobar.sh" "$nueva" "$db" consultar "$filtro"

printf '\nSimulación de un arranque con una ruta de SQLite inválida\n'
printf 'python3 %s/src/main.py --db %s\n' "$nueva" "$datos"
set +e
timeout 8 python3 "$nueva/src/main.py" --db "$datos" > "$datos/fallo.log" 2>&1
estado=$?
set -e
tail -n 3 "$datos/fallo.log"
printf 'Código de salida: %s\n' "$estado"
[[ "$estado" == 1 ]]
grep -Fq 'unable to open database file' "$datos/fallo.log"

printf '\nRecuperación desde el ZIP conservado\n'
zip="$base/paquetes/$anterior/sistema-inventario-$anterior.zip"
recuperada=$(mktemp -d "$base/recuperada-$anterior.XXXXXXXX")
sha256sum "$zip"
python3 -m zipfile -e "$zip" "$recuperada"
printf 'Archivo de origen: %s\nVersión recuperada en: %s\n' "$zip" "$recuperada"
bash "$recuperada/pruebas/comprobar.sh" "$recuperada" "$db" consultar
REMOTO

#!/usr/bin/env bash
set -euo pipefail

configuracion=$1
tag=$2
paquete=$3
nombre=$(basename "$paquete")
if [[ ! "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ || "$nombre" != "sistema-inventario-$tag.zip" ]]; then
  printf 'La etiqueta y el nombre del paquete no corresponden.\n' >&2
  exit 1
fi

checksum=$(sha256sum "$paquete")
checksum=${checksum%% *}
ssh_destino=(ssh -F "$configuracion" inventario)
recepcion=$("${ssh_destino[@]}" '
  set -eu
  umask 077
  mkdir -p "$HOME/sistema-inventario"
  basename "$(mktemp -d "$HOME/sistema-inventario/.recepcion.XXXXXXXX")"
')
[[ "$recepcion" =~ ^\.recepcion\.[A-Za-z0-9]{8}$ ]]
scp -F "$configuracion" "$paquete" "inventario:sistema-inventario/$recepcion/"
printf 'Transferencia SCP completada: %s\n' "$nombre"

"${ssh_destino[@]}" bash -s -- "$tag" "$nombre" "$recepcion" "$checksum" <<'REMOTO'
set -euo pipefail
tag=$1
archivo=$2
base="$HOME/sistema-inventario"
temporal="$base/$3"
recibido="$temporal/$archivo"
checksum=$4
trap 'rm -rf -- "$temporal"' EXIT
printf '%s  %s\n' "$checksum" "$recibido" | sha256sum -c -

paquetes="$base/paquetes/$tag"
conservado="$paquetes/$archivo"
destino="$base/versiones/$tag"
mkdir -p "$paquetes" "$base/versiones"

if [[ -e "$conservado" ]] && ! cmp -s "$conservado" "$recibido"; then
  printf 'El ZIP conservado para esta etiqueta difiere. Revisa la Release.\n' >&2
  exit 1
fi

if [[ ! -e "$destino" ]]; then
  python3 -m zipfile -e "$recibido" "$temporal/contenido"
  test -f "$temporal/contenido/src/main.py"
  [[ $(cat "$temporal/contenido/VERSION") == "$tag" ]]
  if [[ ! -e "$conservado" ]]; then
    mv -- "$recibido" "$conservado"
  fi
  mv -T -- "$temporal/contenido" "$destino"
else
  test -f "$destino/src/main.py"
  [[ $(cat "$destino/VERSION") == "$tag" ]]
  cmp -s "$conservado" "$recibido"
fi

printf 'Servidor %s: versión %s preparada.\n' "$(hostname)" "$tag"
ls -lh -- "$conservado" "$destino/src/main.py"
REMOTO

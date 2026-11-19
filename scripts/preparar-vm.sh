#!/usr/bin/env bash
set -euo pipefail

destino=$1
umask 077
mkdir -p "$destino"
sudo apt-get -qq update
sudo apt-get -qq install -y --no-install-recommends qemu-system-x86 cloud-image-utils ovmf
origen=https://cloud-images.ubuntu.com/minimal/releases/noble/release
imagen=ubuntu-24.04-minimal-cloudimg-amd64.img
curl -fsS --retry 3 "$origen/$imagen" -o "$destino/$imagen"
curl -fsS --retry 3 "$origen/SHA256SUMS" -o "$destino/SHA256SUMS"
(
  cd "$destino"
  grep -F " *$imagen" SHA256SUMS | sha256sum -c -
)
ssh-keygen -q -t ed25519 -N '' -f "$destino/credencial"
ssh-keygen -q -t ed25519 -N '' -f "$destino/maquina"
read -r tipo clave _ < "$destino/maquina.pub"
printf '[127.0.0.1]:2222 %s %s\n' "$tipo" "$clave" > "$destino/known_hosts"

{
  cat <<'CLOUD'
#cloud-config
hostname: inventario-destino
manage_etc_hosts: true
ssh_pwauth: false
ssh_deletekeys: true
ssh_genkeytypes: []
users:
  - name: despliegue
    shell: /bin/bash
    lock_passwd: true
    ssh_authorized_keys:
CLOUD
  printf '      - %s\nssh_keys:\n  ed25519_private: |\n' "$(cat "$destino/credencial.pub")"
  sed 's/^/    /' "$destino/maquina"
  printf '  ed25519_public: %s\n' "$(cat "$destino/maquina.pub")"
} > "$destino/user-data"
printf 'instance-id: practica-deploy-%s\nlocal-hostname: inventario-destino\n' "$GITHUB_RUN_ID" \
  > "$destino/meta-data"
cloud-localds "$destino/seed.img" "$destino/user-data" "$destino/meta-data"
cp /usr/share/OVMF/OVMF_VARS_4M.fd "$destino/OVMF_VARS.fd"

aceleracion=(-accel tcg,thread=multi -cpu max)
if [[ -r /dev/kvm && -w /dev/kvm ]]; then
  aceleracion=(-accel kvm -cpu host)
fi
qemu-system-x86_64 -machine q35 "${aceleracion[@]}" -m 1536 -smp 2 \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd \
  -drive if=pflash,format=raw,file="$destino/OVMF_VARS.fd" \
  -drive file="$destino/$imagen",format=qcow2,if=virtio \
  -drive file="$destino/seed.img",format=raw,if=virtio \
  -netdev user,id=practica,hostfwd=tcp:127.0.0.1:2222-:22 \
  -device virtio-net-pci,netdev=practica -display none -monitor none \
  -serial file:"$destino/arranque.log" -pidfile "$destino/qemu.pid" -daemonize

cat > "$destino/ssh_config" <<CONFIG
Host inventario
  HostName 127.0.0.1
  Port 2222
  User despliegue
  IdentityFile "$destino/credencial"
  UserKnownHostsFile "$destino/known_hosts"
  StrictHostKeyChecking yes
  IdentitiesOnly yes
  BatchMode yes
  ConnectTimeout 4
CONFIG

for _ in {1..60}; do
  if ssh -F "$destino/ssh_config" inventario true 2>/dev/null; then
    ssh -F "$destino/ssh_config" inventario \
      'hostname; whoami; grep "^PRETTY_NAME" /etc/os-release; systemctl is-active ssh; python3 --version'
    exit 0
  fi
  sleep 4
done
printf 'La VM no respondió a la conexión SSH.\n' >&2
exit 1

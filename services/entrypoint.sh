#!/bin/bash

set -Eeuo pipefail

declare -A MOUNTS

MOUNTS["/root/.cache"]="/userdata/kohya-ss-gui/.cache"
MOUNTS["${ROOT}/SmilingWolf"]="/userdata/kohya-ss-gui/SmilingWolf"

for to_path in "${!MOUNTS[@]}"; do
  set -Eeuo pipefail
  from_path="${MOUNTS[${to_path}]}"
  rm -rf "${to_path}"
  if [ ! -f "$from_path" ]; then
    mkdir -vp "$from_path"
  fi
  mkdir -vp "$(dirname "${to_path}")"
  ln -sT "${from_path}" "${to_path}"
  echo Mounted $(basename "${from_path}")
done

exec "$@"

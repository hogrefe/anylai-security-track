#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
test -x "$ROOT/runtime/bin/python3.14"
export PYTHONDONTWRITEBYTECODE=1
exec "$ROOT/runtime/bin/python3.14" -m security_assessment.reproduce

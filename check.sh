#!/usr/bin/env bash
set -e

pytest
tests/cli.sh
tests/doc.sh
dev/lint.sh

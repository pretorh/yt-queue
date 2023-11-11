#!/usr/bin/env bash
set -e

pytest
tests/cli.sh
dev/lint.sh

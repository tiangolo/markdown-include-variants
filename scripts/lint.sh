#!/usr/bin/env bash

set -e
set -x

mypy src
ty check src
ruff check .
ruff format --check .

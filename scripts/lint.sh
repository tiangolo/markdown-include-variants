#!/usr/bin/env bash

set -e
set -x

mypy src
ruff check .
ruff format --check .

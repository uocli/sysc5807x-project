#!/bin/bash
set -e

echo "Running tests with coverage..."

pytest "$@" --cov=src --cov-report=term-missing --cov-report=html

echo "Coverage report generated at htmlcov/index.html"
open htmlcov/index.html 2>/dev/null || true

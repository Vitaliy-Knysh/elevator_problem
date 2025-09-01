#!/bin/bash
if ![ -d ".venv" ]; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requiremets.txt
fi
python3 main.py
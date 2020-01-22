#!/bin/bash
# Generates 16 random bytes and writes them to secret_key.py
python -c 'import os;print(f"SECRET_KEY = {os.urandom(16)}")' > secret_key.py
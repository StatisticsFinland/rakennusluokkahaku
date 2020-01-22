#!/bin/bash
python -m pytest --cov=src --cov-branch --cov-report=term --cov-report=html tests/

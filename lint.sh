#!/bin/bash
autopep8 --recursive --in-place --ignore E402 src/ tests/ app.py

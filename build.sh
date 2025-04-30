#!/bin/bash

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps

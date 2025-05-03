#!/bin/bash

echo "🔧 Pokrećem build.sh skriptu..."

pip install -r requirements.txt
playwright install chromium

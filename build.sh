#!/bin/bash
set -e

# create version timestamp
TIMESTAMP=$(date +%Y%m%d.%H%M)
APP_NAME="Static-Code-Analysis-V$TIMESTAMP"

# create new output directory
mkdir -p "dist/V$TIMESTAMP"

# build application
.venv/bin/pyinstaller --onefile --noconsole --name "$APP_NAME" --distpath "./dist/V$TIMESTAMP" ./src/main.py -y
if [ $? -ne 0 ]; then
    echo "Could not build python application."
    exit 1
fi

# copy README and assets
cp README.md "dist/V$TIMESTAMP/README.md"
cp analysis_config.json5 "dist/V$TIMESTAMP/analysis_config.json5"
cp -r assets "dist/V$TIMESTAMP/"

echo "Build completed successfully!"
#!/bin/bash

for d in */ ; do
    echo "$d"
    cp "edge_detection/output_dialog.py" "$d"/output_dialog.py && cp "edge_detection/output_dialog.ui" "$d"/output_dialog.ui
done
cmd /k
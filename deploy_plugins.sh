#!/bin/bash

for d in */ ; do
    echo "$d"
    cd "$d" && pb_tool deploy -y && cd ..
done
cmd /k

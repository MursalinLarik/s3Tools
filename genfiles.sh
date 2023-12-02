#!/bin/bash

generate_file() {
    size_mb=$1
    file_name="objects/${size_mb}MB_file.txt"
    dd if=/dev/zero of="$file_name" bs=1M count="$size_mb"
    echo "$file_name created"
}

generate_file $1
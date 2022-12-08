#!/bin/zsh

for filename in ./files/*; do
    # python3 parser.py "Morph" "WX" "Unicode" "$filename"
    python3 batch_parser.py "$filename"
done

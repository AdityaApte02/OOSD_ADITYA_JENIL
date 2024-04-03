#!/bin/bash


# Loop through all the JSON files in the directory
for file in *.json; do
    # Ignore if file has "expected" in the name
    if [[ $file == *"expected"* ]]; then
        continue
    fi
    # Print the filename
    echo Running $file file
    # Run the python3 command with the filename as an argument
    python3 ../client_implementation.py $file
done

# command to run the script
# sh script.sh
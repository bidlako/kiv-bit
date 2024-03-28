#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Please provide the folder name as an argument."
  exit 1
fi

folder_name="$1"

if [ ! -d "$folder_name" ]; then
  echo "Folder '$folder_name' does not exist."
  exit 1
fi

zip_file="A20B0055P.zip"

zip -r "$zip_file" "$folder_name"

echo "Folder '$folder_name' has been zipped as '$zip_file'."


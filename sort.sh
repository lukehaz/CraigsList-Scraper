#!/bin/bash

rm Lsorted.csv
rm top5.csv
# Input file path
input_file="listings.csv"

# Output file path for sorted data
sorted_file="Lsorted.csv"

# Output file path for top 5 entries
top5_file="top5.csv"

sort_column="4"

sort_options="-t, -k${sort_column}"

sort ${sort_options} "${input_file}" > "${sorted_file}"

head -n 5 "${sorted_file}" > "${top5_file}"

echo "Sorting complete. Top 5 entries written to ${top5_file}"
rm listings.csv

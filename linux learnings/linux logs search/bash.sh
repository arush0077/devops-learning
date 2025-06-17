#!/bin/bash

# Check if both arguments are passed: file and search term
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <log_file> <request_method>"
  exit 1
fi

LOG_FILE="$1"
SEARCH_METHOD="$2"

# Search case-insensitively for the given request method (e.g. GET, POST, DELETE)
echo "Filtering '$SEARCH_METHOD' requests from $LOG_FILE:"
grep -i "$SEARCH_METHOD" "$LOG_FILE"

#!/bin/bash
for i in {1..10}; do
    curl -X POST "http://127.0.0.1:8000/facade" \
         -H "Content-Type: application/json" \
         -d '{"msg": "msg'"$i"'"}'
done

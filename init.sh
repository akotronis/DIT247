#!/bin/bash

# Wait for CouchDB to start
while ! curl -s http://admin:admin@localhost:5984/_up; do
  sleep 1
done

# Create the default databases
curl -X PUT http://admin:admin@localhost:5984/_users
curl -X PUT http://admin:admin@localhost:5984/_replicator
curl -X PUT http://admin:admin@localhost:5984/_global_changes

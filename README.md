# Couch DB
## Docs
- https://docs.couchdb.org/en/stable/config/intro.html#configuration-files
- https://docs.couchdb.org/en/stable/setup/single-node.html#single-node-setup
- https://docs.couchdb.org/en/stable/config/auth.html#config-admins


# UIs
## Couch DB
- http://localhost:5984/_utils/#login

## Node Red
- http://localhost:1880

## MailHog
- http://localhost:8025

## Minio
- http://localhost:9000

## Openwhisk
- Web UI: http://localhost:3232
- Config Info: http://localhost:3233
- Run `>>> docker logs ctr-openwhisk | grep auth` to get the info  
  `wsk property set --apihost 'API_HOST' --auth 'AUTH_KEY'`
- Run inside the container
  - `>>> wsk property set --apihost http://ctr-openwhisk:3233 --auth AUTH_KEY` to set credentials
  - `>>> wsk namespace list` to verify `guest` namespace is set. If not
    - `>>> echo "NAMESPACE=guest" >> ~/.wskprops`
  - Verifications:
    - `>>> wsk list -v` to verify host connection and credentials
    - `>>> wsk property get` to verify configuration
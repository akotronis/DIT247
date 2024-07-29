# Docs
## Couchdb
- https://docs.couchdb.org/en/stable/config/intro.html#configuration-files
- https://docs.couchdb.org/en/stable/setup/single-node.html#single-node-setup
- https://docs.couchdb.org/en/stable/config/auth.html#config-admins
## Openwhisk
### Apache
- https://openwhisk.apache.org/documentation.html#automating_actions_from_event_sources
### Github
- [Standalone Server](https://github.com/apache/openwhisk/blob/master/core/standalone/README.md)
- [Docker compose setup](https://github.com/apache/openwhisk-devtools/blob/master/docker-compose/README.md)
- [Docker compose file](https://github.com/apache/openwhisk-devtools/blob/master/docker-compose/docker-compose.yml)
- [Actions](https://github.com/apache/openwhisk/blob/master/docs/actions.md#listing-actions)
- [Cli](https://github.com/apache/openwhisk/blob/master/docs/cli.md#openwhisk-cli)

# Process management on Windows 11
`>>> netstat -aon | findstr :3234` to check processes running on a specific port or `>>>  netstat -aon | findstr LISTEN` for all listening ports
`>>> tasklist /FI "PID eq 19812"` to identify the process
`>>> taskkill /PID 19812 /F` to kill the process
`>>> tasklist | findstr /I "VBox"` to print the processes that run under Image Name starting with `VBox`
`>>> netstat -aon | findstr /R /C:"31900" /C:"32076"` to see on which port these process ids are listening to
`>>> ForEach ($processId in (netstat -aon | Select-String ":9000" | ForEach-Object { $_.ToString().Split()[-1] })) { taskkill /PID $processId /F }` to kill processes running on port 9000

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

- `build0.gradle` is the file from the [repo](https://github.com/apache/openwhisk/blob/master/core/standalone/build.gradle)
- `build.gradle` is the file with the modifucations required in order for `>>> /gradlew --info :core:standalone:build` to run successfully

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
- [wsk cli docs](https://github.com/apache/openwhisk/blob/master/docs/cli.md#openwhisk-cli)
- [Openwhisk swagger](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/openwhisk/openwhisk/master/core/controller/src/main/resources/apiv1swagger.json#/Actions/invokeActionInPackage)

  ~/vagrant

  sudo java -Dwhisk.standalone.host.name=0.0.0.0 -Dwhisk.standalone.host.internal=0.0.0.0 -Dwhisk.standalone.host.external=0.0.0.0 -jar ~/openwhisk/bin/openwhisk-standalone.jar --couchdb --kafka --api-gw --kafka-ui

  sudo java -Dwhisk.standalone.host.name=0.0.0.0 -Dwhisk.standalone.host.internal=0.0.0.0 -Dwhisk.standalone.host.external=0.0.0.0 -jar ./bin/openwhisk-standalone.jar --couchdb --kafka --api-gw --kafka-ui

# FLOW
- Minio 

- Create a bucket `dit247` in Minio
- Inject Image -> Read Image -> Save to Minio bucket `dit247` on `/initial`
- Minio sends file info to Kafka (Producer)
- Openwhisk listens to Kafka (Consumer)
- Openwhisk gets file from Minio compresses it and sends it to a different folder on `/compressed`
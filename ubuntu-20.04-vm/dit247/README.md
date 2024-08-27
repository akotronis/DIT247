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

# Minio
## Kafka bucket notification setup
Inside the minio container: `docker exec -it ctr-minio bash`
- Set alias for minio service:  
  `>>> mc alias set minio http://127.0.0.1:9000 admin password`
- Configure kafka notiications on topic **dit247**:  
  `>>> mc admin config set minio notify_kafka:1 brokers="ctr-kafka:9992" topic="dit247" tls_skip_verify="off" queue_dir="" queue_limit="0" sasl="off" sasl_password="" sasl_username="" tls_client_auth="0" tls="off" client_tls_cert="" client_tls_key="" version="" --insecure`
- Configure kafka notiications on topic **dit247c**:  
  `>>> mc admin config set minio notify_kafka:2 brokers="ctr-kafka:9992" topic="dit247c" tls_skip_verify="off" queue_dir="" queue_limit="0" sasl="off" sasl_password="" sasl_username="" tls_client_auth="0" tls="off" client_tls_cert="" client_tls_key="" version="" --insecure`
- Restart minio service:  
  `>>> mc admin service restart minio`
- Verify configuration:  
  `>>> mc admin config get minio notify_kafka`
- Add event on bucket **dit247** for notiication coniguration 1:  
  `>>> mc event add minio/dit247 arn:minio:sqs::1:kafka --event put`
- Add event on bucket **dit247c** for notiication coniguration 2:  
  `>>> mc event add minio/dit247c arn:minio:sqs::2:kafka --event put`
- To Disable event and notification configuration:  
  `>>> mc event remove minio/dit247c arn:minio:sqs::2:kafka --event put`
  `>>> mc admin config set minio notify_kafka:2 enable=off`
  `>>> mc admin service restart minio`
[Reference](https://blog.min.io/complex-workflows-apache-kafka-minio/)

## Webhook bucket notification setup
- Configure webhook notiications on endpoint **http://ctr-nodered:1880/compressed-images**:  
  `>>> mc admin config set minio notify_webhook:1 endpoint="http://ctr-nodered:1880/compressed-images" queue_limit="10000" queue_dir="/tmp" queue_retry_interval="1s" enable="on"`
- Restart minio service:  
  `>>> mc admin service restart minio`
- Verify configuration:  
  `>>> mc admin config get minio notify_webhook`
- Add event on bucket **dit247c** for notiication coniguration:  
  `>>> mc event add minio/dit247c arn:minio:sqs::1:webhook --event put`
- To Disable event and notification configuration:  
  `>>> mc event remove minio/dit247c arn:minio:sqs::1:webhook --event put`
  `>>> mc admin config set minio notify_webhook:1 enable=off`
  `>>> mc admin service restart minio`


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

# FLOW
- Minio 

- Create a bucket `dit247` in Minio
- Inject Image -> Read Image -> Save to Minio bucket `dit247` on `/initial`
- Minio sends file info to Kafka (Producer)
- Openwhisk listens to Kafka (Consumer)
- Openwhisk gets file from Minio compresses it and sends it to a different folder on `/compressed`

# VM
If with
- `>>> vagrant up` and/or
- `>>> vagrant up --provision`

the `.vagrant/machines/virtualbox/private_key` is not generated, then `vagrnat ssh` connects to the vm and 
- `>>> vagrant ssh-config` will use the `~/.vagrant.d/insecure_private_keys` keys.

Running
- `>>> vagrant reload` may generate the `.vagrant/machines/virtualbox/private_key` so
- `>>> vagrant ssh-config` will use the `Vagrantfile folder path/.vagrant/machines/default/virtualbox/private_key` keys.

In any case, to connect with VSCode to the vm, update `~/.ssh/config` with the output of `>>> vagrant ssh-config`

## ssh issue
Generally run
- `>>> vagrant up (--provision)` (`.vagrant/machines/virtualbox/private_key` is expected to NOT be created)
- `>>> vagrant reload` (maybe more than once)
  - (`.vagrant/machines/virtualbox/private_key` is expected to BE created)
  - (is expeted to NOT be able to ssh), then  
- `>>> vagrant up (--provision)`
- `vagrant ssh` to check if it can ssh (is expected to BE able to ssh)
- `>>> vagrant ssh-config` to update with its output the `~/.ssh/config`
- Connect with VSCode to the vm

## ssh-agent
- Start: `>>> eval $(ssh-agent -s)`
- List keys: `>>> ssh-add -L`
- Add key from file: `>>> ssh-add ~/.ssh/id_rsa`

## ssh with command passing private key file
- `>>> ssh -p 2222 -i C:/ANASTASIS/HUA/SEMESTER-4/DIT247-Cloud-Services/Project/ubuntu-20.04-vm/.vagrant/machines/default/virtualbox/private_key vagrant@127.0.0.1 -o LogLevel=DEBUG`
- `>>> ssh -p 2222 -i ~/.vagrant.d/insecure_private_key vagrant@127.0.0.1 -o LogLevel=DEBUG`
- `>>> ssh -p 2222 -i ~/.vagrant.d/insecure_private_keys/vagrant.key.rsa vagrant@127.0.0.1 -o LogLevel=DEBUG`
- `>>> ssh -p 2222 -i ~/.vagrant.d/insecure_private_keys/vagrant.key.ed25519 vagrant@127.0.0.1 -o LogLevel=DEBUG`
- `>>> ssh -p 2222 -i ~/.ssh/id_rsa akotronis@127.0.0.1 -o LogLevel=DEBUG`

## ssh to vm with password
- host `config` file (for VSCode)  
  > Host DIT247  
    &emsp;HostName 127.0.0.1  
    &emsp;Port 2222  
    &emsp;User vagrant  
    &emsp;PasswordAuthentication yes  
    &emsp;PreferredAuthentications password
- Remove from `C:\Users\<User>\.ssh\known_hosts` the `[127.0.0.1]:2222` lines defining ssh keys
- `vagrant ssh` to vm and
  - change on `/etc/ssh/sshd_config` setting `PasswordAuthentication` to `yes`
  - run `>>> sudo systemctl restart sshd`
# Commands
## Process management on Windows 11
- `>>> netstat -aon | findstr :3234` to check processes running on a specific port or `>>> findstr /C:"3232" /C:"8080" ...` for multiple ports or `>>>  netstat -aon | findstr LISTEN` for all listening ports
- `>>> tasklist /FI "PID eq 19812"` to identify the process
- `>>> taskkill /PID 19812 /F` to kill the process
- `>>> tasklist | findstr /I "VBox"` to print the processes that run under Image Name starting with `VBox`
- `>>> netstat -aon | findstr /R /C:"31900" /C:"32076"` to see on which port these process ids are listening to
- `>>> ForEach ($processId in (netstat -aon | Select-String ":9000" | ForEach-Object { $_.ToString().Split()[-1] })) { taskkill /PID $processId /F }` to kill processes running on port 9000
## SSH
- **ssh-agent**
  - Start: `>>> eval $(ssh-agent -s)`
  - Kill: `>>> eval $(ssh-agent -k)`
  - List keys: `>>> ssh-add -L`
  - Add key from file: `>>> ssh-add ~/.ssh/id_rsa`
- Get public key from private key: `>>> ssh-keygen -y -f /path/to/private_key > extracted_public_key.pub`
- **ssh passing private key file or password**
  - `>>> ssh -p 2222 -i C:/ANASTASIS/HUA/SEMESTER-4/DIT247-Cloud-Services/Project/ubuntu-20.04-vm/.vagrant/machines/default/virtualbox/private_key vagrant@127.0.0.1 -o LogLevel=DEBUG`
  - `>>> ssh -p 2222 -i ~/.vagrant.d/insecure_private_key vagrant@127.0.0.1 -o LogLevel=DEBUG`
  - `>>> ssh -p 2222 -i ~/.vagrant.d/insecure_private_keys/vagrant.key.rsa vagrant@127.0.0.1 -o LogLevel=DEBUG`
  - `>>> ssh -p 2222 -i ~/.vagrant.d/insecure_private_keys/vagrant.key.ed25519 vagrant@127.0.0.1 -o LogLevel=DEBUG`
  - `>>> ssh -p 2222 vagrant@127.0.0.1 -o LogLevel=DEBUG` (vagrant)
  - `>>> ssh -p 2222 root@127.0.0.1 -o LogLevel=DEBUG` (root)

# Launch and test the flow
### Prerequisites: Synced folder
 Syncing folder with vagrant doesnt seem to work
 - Add a shared folder to the vm from VirtualBox settings
   - **Folder Path** : the path on host
   - **Folder Name** : the path on the vm
   - **Mount Point** : the path on the vm to mount the folder with the above folder name
   - Select **Auto mount** and **Make Permanent**
  - In the vm, add vagrant logged in user to `vboxsf` group (mounted folder will be of user `root` and group `vboxsf`)
    - `>>> sudo usermod -aG vboxsf $(whoami)`
    - `>>> groups` to verify logged in user is in `vboxsf` group
### Prerequisites: Configurations: Openwhisk (wsk cli)
- Verify `wsk` client installation from vagrant provisioning `>>> wsk --help`
- API host:
  - Verify if API host is set `>>> wsk property get` (This should have been done from vagrant provisioning)
  - if not, set it `>>> wsk property set --apihost http://127.0.0.1:3233`
- Credentials:
  - Verify credentials are set `>>> wsk property get --auth` (This should have been done from vagrant provisioning)
  - if not verified, set them ``>>> wsk property set --auth `cat ~/openwhisk/ansible/files/auth.guest` ``
- API host/Credentials/namespace:
  - Verify host and connection credentials `>>> wsk list -v` or by
  - `>>> cat ~/.wskprops`
  - Verify `guest` namespace exists by `>>> wsk namespace list`
### Prerequisites: Configurations: Openwhisk (python runtime/actions with dependencies)
Actions with dependencies will be inside `~/openwhisk_actions`. Each subfolder will be the name of the action.  
Work in `~/dit247/actions/dependencies/minio` which is shared and copy to `~/openwhisk_actions` afterwards (need to be separate due to VirtualBox sharing imposed permissions)  
For a **minio** named action with python runtime:
- In `~/dit247/actions/dependencies/minio` run `>>> docker build -f Dockerfile.python -t img-python-action .` to build **python3.10** image for action creation
- Create `~/openwhisk_actions/minio` if it doesn't exist
- Make sure it is clean: `>>> sudo rm -R ./*`
- Copy required content from working folder: `>>> cp ~/dit247/actions/dependencies/minio/* -R .`
- Use built image to create **python3.10** virtual environment for action creation compatible with **python 3.10** runtime:  
`>>> docker run --rm -v "$PWD:/app" img-python-action bash -c "virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"`
- Zip content: `>>> zip -r minio.zip virtualenv __main__.py`
- Create action: `>>> wsk action create minio --kind python:3.10 --main main minio.zip` (`3.10, 3.11, 3.12` are available)
- Verify created action
  - `>>> wsk action list` or
  - `>>> curl -u 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP http://localhost:3233/api/v1/namespaces/guest/actions` (This can send from postman as well)
- Invoke action `>>> wsk action invoke minio --result --blocking --param key1 value1 --param key2 value2 ...`
- (Delete action and verify deletion: `>>> wsk action delete minio && wsk action list`)
  
### Prerequisites: Configurations: Kafka
Make sure a `dit247` topic exists on kafka. If not create it from the UI
(This might be created automatically when the nodered consumer node that listens on it is up)
### Prerequisites: Configurations: Minio
Log in to the container: `>>> docker exec -it ctr-minio bash`
#### [Kafka bucket notification setup](https://blog.min.io/complex-workflows-apache-kafka-minio/)
- Set alias for minio service:  
  `>>> mc alias set minio http://127.0.0.1:9000 admin password`
- Configure kafka notiications on topic **dit247**:  
  `>>> mc admin config set minio notify_kafka:1 brokers="ctr-kafka:9992" topic="dit247" tls_skip_verify="off" queue_dir="" queue_limit="0" sasl="off" sasl_password="" sasl_username="" tls_client_auth="0" tls="off" client_tls_cert="" client_tls_key="" version="" --insecure`
<!-- - Configure kafka notiications on topic **dit247c**:  
  `>>> mc admin config set minio notify_kafka:2 brokers="ctr-kafka:9992" topic="dit247c" tls_skip_verify="off" queue_dir="" queue_limit="0" sasl="off" sasl_password="" sasl_username="" tls_client_auth="0" tls="off" client_tls_cert="" client_tls_key="" version="" --insecure` -->
- Restart minio service:  
  `>>> mc admin service restart minio`
- Verify configuration:  
  `>>> mc admin config get minio notify_kafka`
- Make sure buckets **dit247** and **dit247c** are created through the nodered flow
- Add event on bucket **dit247** for notiication coniguration 1:  
  `>>> mc event add minio/dit247 arn:minio:sqs::1:kafka --event put`
<!-- - Add event on bucket **dit247c** for notiication coniguration 2:  
  `>>> mc event add minio/dit247c arn:minio:sqs::2:kafka --event put` -->
- To Disable event and notification configuration:  
  - `>>> mc event remove minio/dit247c arn:minio:sqs::2:kafka --event put`
  - `>>> mc admin config set minio notify_kafka:2 enable=off`
  - `>>> mc admin service restart minio`  

#### Webhook bucket notification setup
Configure webhook notiications on endpoint **http://ctr-nodered:1880/compressed-images**:  
- Make sure bucket **dit247c** is created through the nodered flow
  `>>> mc admin config set minio notify_webhook:1 endpoint="http://ctr-nodered:1880/compressed-images" queue_limit="10000" queue_dir="/tmp" queue_retry_interval="1s" enable="on"`
- Restart minio service:  
  `>>> mc admin service restart minio`
- Verify configuration:  
  `>>> mc admin config get minio notify_webhook`
- Add event on bucket **dit247c** for notiication coniguration:  
  `>>> mc event add minio/dit247c arn:minio:sqs::1:webhook --event put`
- To Disable event and notification configuration:  
  - `>>> mc event remove minio/dit247c arn:minio:sqs::1:webhook --event put`
  - `>>> mc admin config set minio notify_webhook:1 enable=off`
  - `>>> mc admin service restart minio`

### VM launch and setup
- In Windows host run `>>> vagrant up` in the folder where the `Vagrantfile` is
- Connect to vm with VSCode using one of the hosts in `~/.ssh/config` file
- Forward ports from VSCode
  - 1880 (Nodered UI `http://localhost:1880` and dashboard `http://localhost:1880/ui`)
  - 9991 (Minio UI `http://localhost:9991/browser`)
  - 8080 (Kafka UI `http://localhost:8080/`)
  - 5984 (CouchDB UI `http://localhost:5984/_utils/#login`)
  - 3233 (Openwisk API `http://localhost:3233` required for postman. Can test from vm if it is available with `>>> curl http://0.0.0.0:3233`)
  - 3232 (Openwisk playground `http://localhost:3232/playground/ui/index.html`. Not required.)
  - 8025 (Mailhog UI, if used `http://localhost:8025/`)
- If VSCode has problems with ssh, then:
  - `>>> vagrant ssh -- -L 1880:localhost:1880 -L 9991:localhost:9991 -L 8080:localhost:8080 -L 5984:localhost:5984 -L 3233:localhost:3233 -L 3232:localhost:3232 -L 8025:localhost:8025` to ssh with vagrant and map required ports to local machine
  - Verify port mapping with `>>> netstat -aon | findstr /C:"1880" /C:"9991" /C:"8080" /C:"5984" /C:"3233" /C:"3232" /C:"8025"`
  - Ports should be releashed when terminating ssh session by `>>> logout` or `>>> exit`from inside the vm
  - If terminal is closed without logging out and the session is open, then  
    - `>>> Get-Process | Where-Object { $_.ProcessName -like "*ssh*" }` and `>>> taskkill /PID <Id> /F` (`Id` column number) from **powershell** or
    - `>>> ps aux | grep ssh` and `>>> kill -9 <PID>` (`PID` column number) from **gitbash**
- Run `>>> ps -eF | grep java` to see if the openwhisk launch command is running and if not run it:
  - `>>> sudo java -Dwhisk.standalone.host.name=0.0.0.0 -Dwhisk.standalone.host.internal=0.0.0.0 -Dwhisk.standalone.host.external=0.0.0.0 -jar ~/openwhisk/bin/openwhisk-standalone.jar --couchdb --kafka --api-gw --kafka-ui`
- Check if Openwhisk API is accessible: `>>> curl http:0.0.0.0:3233`

- `>>> docker-compose up -d` (or `>>> docker-compose up -d -build` if needed) in `~/dit247`
- Check the forwarded ports from browser in the above urls and
- make sure the containers are Up with `>>> docker ps -a`

### Test the flow
#### Bucket list
  Run the inject node on Bucket list section to list minio buckets (They should already be there from **Prerequisites: Configurations** stage)
#### Image upload to minio
- Make sure the node *Invoke Openwhisk action* has the vm IP on th url which can be found with `>>> ip addr | grep eth0 | head -n 2 | tail -n 1` in the vm
- Make sure a folder the folder `~/dit247/data/nodered/images` exists in the vm with files with names `file-1.jpg, file-2.jpg, ...`
- If not, run `>>> python3 -m python.rename_files` from `~/dit247` to rename them  
- Run the *Trigger file upload* inject node of the *Single image upload* section and check
  - log messages
  - Minio bucket and kafka UI from browser
- Retry pattern:
  - Stop the minio container `>>> docker stop ctr-minio`
  - Enable the *Repeatedly trigger file upload* inject node and set *Repeat* to every *5 hours or sth* in order to test retry pattern once
  - Run the *Repeatedly trigger file upload* inject node and check logs to see retries
  - Start the minio container `>>> docker start ctr-minio`
  - Reset *Repeat* to every *3 seconds* Enable the *Repeatedly trigger file upload* inject node
  - Run the *Repeatedly trigger file upload* inject node and check
    - log messages
    - Minio bucket and kafka UI from browser

# General guides
### vagrant ssh issue
Generally run
- `>>> vagrant up (--provision)` (`.vagrant/machines/virtualbox/private_key` is expected to NOT be created)
- `>>> vagrant reload` (maybe more than once)
  - (`.vagrant/machines/virtualbox/private_key` is expected to BE created)
  - (is expeted to NOT be able to ssh), then  
- `>>> vagrant up (--provision)`
- `vagrant ssh` to check if it can ssh (is expected to BE able to ssh)
- `>>> vagrant ssh-config` to update with its output the `~/.ssh/config`
- Connect with VSCode to the vm
### ssh to vm with password
- host `config` file (see committed `config` file)
- Remove from `~/.ssh/known_hosts` the `[127.0.0.1]:2222` lines defining ssh keys
- `vagrant ssh` to vm and do the below or set it in vagrantfile provision
  - change on `/etc/ssh/sshd_config` setting `PasswordAuthentication` to `yes`
  - run `>>> sudo systemctl restart sshd (or ssh)`
### Add private key to vm
If private key has to be added to `~/.ssh` (for example to work with git/github from inside the vm)
- Must do `chmod 700 ~/.ssh`
- Must do `chmod 600 ~/.ssh/id_ed25519`, `chmod 600 ~/.ssh/id_rsa`

# Troubleshooting
## VSCode ([LIFE SAVER](https://stackoverflow.com/a/66809539))
If ssh is possible from terminal but not with VSCode, then from VScode:
- `>> Ctrl Shit P`
- Remote-SSH: Kill VS Code Server on Host...
- Select host defined on config that has the problem
- Try again

## VM
If with
- `>>> vagrant up` and/or
- `>>> vagrant up --provision`

the `.vagrant/machines/virtualbox/private_key` is not generated, then `vagrnat ssh` connects to the vm and 
- `>>> vagrant ssh-config` will use the `~/.vagrant.d/insecure_private_keys` keys.

Running
- `>>> vagrant reload` may generate the `.vagrant/machines/virtualbox/private_key` so
- `>>> vagrant ssh-config` will use the `Vagrantfile folder path/.vagrant/machines/default/virtualbox/private_key` keys.

In any case, to connect with VSCode to the vm, update `~/.ssh/config` with the output of `>>> vagrant ssh-config`

# Docs
- **Vagrant**
  - [Default User Settings](https://developer.hashicorp.com/vagrant/docs/boxes/base#default-user-settings)
  - [SSH Settings](https://developer.hashicorp.com/vagrant/docs/vagrantfile/ssh_settings#available-settings)
  - [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)
  - [Vagrant ssh authentication failure](https://stackoverflow.com/questions/22922891/vagrant-ssh-authentication-failure/23554973#23554973)
  - [Vagrant hangs at "SSH auth method: Private key](https://stackoverflow.com/questions/38463579/vagrant-hangs-at-ssh-auth-method-private-key)
- **ssh/config files**
  - https://linux.die.net/man/5/ssh_config
  - https://www.ssh.com/academy/ssh/config
  - [Understanding SSH StrictHostKeyChecking Option](https://www.howtouselinux.com/post/ssh-stricthostkeychecking-option)
  - [SSH Essentials: Working with SSH Servers, Clients, and Keys](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)
- **MinIO**
  - [Introducing Webhooks for MinIO](https://blog.min.io/introducing-webhooks-for-minio/)
  - [Event-Driven Architecture: MinIO Event Notification Webhooks using Flask](https://blog.min.io/minio-webhook-event-notifications/)
  - [Publish Events to Webhook](https://min.io/docs/minio/linux/administration/monitoring/publish-events-to-webhook.html)
  - [Publish Events to Kafka](https://min.io/docs/minio/linux/administration/monitoring/publish-events-to-kafka.html)
  - [Bucket Notifications](https://min.io/docs/minio/linux/administration/monitoring/bucket-notifications.html)
  - [Orchestrate Complex Workflows Using Apache Kafka and MinIO](https://blog.min.io/complex-workflows-apache-kafka-minio/)
- **Node red**
  - [Node-RED Dashboad 2.0 - Chart `ui-chart`- 1](https://dashboard.flowfuse.com/nodes/widgets/ui-chart.html#line-charts)
  - [Node-RED Dashboad 2.0 - Chart `ui-chart`- 2](https://dashboard-demos.flowfuse.cloud/dashboard/charts-example#line-chart)
  - [Node-red in Docker](https://www.youtube.com/watch?v=jLCw5yNbr_I)
  - [Node-Red in Docker with Home Assistant](https://www.youtube.com/watch?v=fxo5-iiwZXk)
- **Couchdb**
  - https://docs.couchdb.org/en/stable/config/intro.html#configuration-files
  - https://docs.couchdb.org/en/stable/setup/single-node.html#single-node-setup
  - https://docs.couchdb.org/en/stable/config/auth.html#config-admins

- **Openwhisk**
  - [Swagger](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/openwhisk/openwhisk/master/core/controller/src/main/resources/apiv1swagger.json#/Actions/invokeActionInPackage)
  - [Standalone Server](https://github.com/apache/openwhisk/blob/master/core/standalone/README.md) (Github)
  - [Docker compose setup](https://github.com/apache/openwhisk-devtools/blob/master/docker-compose/README.md) (Github)
  - [Docker compose file](https://github.com/apache/openwhisk-devtools/blob/master/docker-compose/docker-compose.yml) (Github)
  - [How to setup OpenWhisk with Docker Compose](https://github.com/apache/openwhisk-devtools/blob/master/docker-compose/README.md) (Github)
  - [Actions](https://github.com/apache/openwhisk/blob/master/docs/actions.md#listing-actions) (Github)
  - [wsk cli](https://github.com/apache/openwhisk/blob/master/docs/cli.md#openwhisk-cli) (Github)
  - [Automating Actions from Event Sources](https://openwhisk.apache.org/documentation.html#automating_actions_from_event_sources) (Apache)
  - [Apache OpenWhisk package for communication with Kafka or IBM Message Hub](https://github.com/apache/openwhisk-package-kafka/blob/master/README.md) (Github)
  - [Apache OpenWhisk Runtimes for Python](https://github.com/apache/openwhisk-runtime-python/blob/master/README.md#using-additional-python-libraries) (Github)
  - [Creating and invoking Python actions](https://github.com/apache/openwhisk/blob/master/docs/actions-python.md) (Github) 
  - [Python Packages in OpenWhisk](https://jamesthom.as/2017/04/python-packages-in-openwhisk/) (James Thomas) 



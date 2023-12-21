1. Insert ZBX_ADDRESS and ZBX_HOST in code
2. Build Dockerfile - docker build -t awx-zabbix-webhook
3. Run docker container - docker run --name awx-zabbix-webhook -p '5000:5000' awx-zabbix-webhook
# Task_1-Microservices_Basics

## Dependencies
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Start the servers
```
chmod +x ./run.sh # make hsell script executable
./run.sh
```
It will start all services.
Or you can start each application separately.
Simply run each line of `run.sh` in different terminals and without `&` in the end.

## Testing
```
curl -X GET 0.0.0.0:8080/facade 
curl -X POST  '0.0.0.0:8080/facade?msg=yourmsg'
curl -X GET 0.0.0.0:8081/logging
curl -X POST 0.0.0.0:8081/logging?uuid=1&msg=qwerty
curl -X GET 0.0.0.0:8082/messages
```
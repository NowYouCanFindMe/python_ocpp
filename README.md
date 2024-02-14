## Python OCPP commands to emulate a EVSE


## Setup

Have Steve CMS configured and running

### Mac Setup

```

git clone https://github.com/steve-community/steve.git
cd steve
brew install docker docker-compose colima
# make coffee
colima start

docker-compose up

```

### Create ChargePoint on steve

![Create Charge Point](./pics/create%20charge%20point.png)


### Add OCPP Tag

![Add OCPP TAG](./pics/create%20ocpp%20tag.png)

#### Get Steve endpoints

If running locally use `0.0.0.0` or host ip address.

Configure `ip` and `port` in `config.toml` file.

![Get endpoints for Steve](./pics/steve%20endpoints.png)
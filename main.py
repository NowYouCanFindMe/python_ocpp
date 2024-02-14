import json
import uuid
import time
import math
import asyncio
import websockets
import toml
import datetime


async def run():
    id = str(uuid.uuid4())
    config = open_toml()
    default_utc = "2024-02-013T23:27:02.404Z"

    # setup
    ip = config['connection']['ip']
    port = config['connection']['port']
    ocpp_id = config['connection']['ocpp_id']
    chargebox_id = config['connection']['chargebox_id']
    transaction_id = 0
    connector_id = 1
    global_meter = 0
    connection_string = "ws://{}:{}/steve/websocket/CentralSystemService/{}".format(ip, port, chargebox_id)
    
    async with websockets.connect(connection_string,
                                  subprotocols=['ocpp1.6']) as websocket:
        # await websocket.send([2,"4f3755c3-b434-4284-b5fd-d4e20514ac52","BootNotification",{"chargePointVendor":"AVT-Company","chargePointModel":"AVT-Express","chargePointSerialNumber":"avt.001.13.1","chargeBoxSerialNumber":"avt.001.13.1.01","firmwareVersion":"0.9.87","iccid":"","imsi":"","meterType":"AVT NQC-ACDC","meterSerialNumber":"avt.001.13.1.01"}])

        await websocket.send(json.dumps([2, id,
                    "BootNotification",
                    {"chargePointVendor":"Example_Vendor",
                     "chargePointModel":"Example_Vendor",
                     "chargePointSerialNumber":"ev.001.01.2",
                     "chargeBoxSerialNumber":"ev.002.14.5.03",
                     "firmwareVersion":"0.0.1",
                     "iccid":"",
                     "imsi":"",
                     "meterType":"EV MEV-ACDC",
                     "meterSerialNumber":"ev.002.33.1.34"}
                     ]))
        response = await websocket.recv()

        while True:
            x = input("Enter value:\t").strip()
            if x == 'a':
                print("\nAuthorize")

                await websocket.send(json.dumps(
                    [2,id,"Authorize",{"idTag": ocpp_id}]
                ))
                response = await websocket.recv()
                print(response)

            if x == 's':
                print("\nStart charge")
                iso_time = get_utc()
                _config = open_toml()
                meter_start = _config['meter']['connector_'+str(connector_id)]
                global_meter = meter_start
                # start transaction

                await websocket.send(json.dumps(
                    [2,id,"StartTransaction",{"connectorId":connector_id,"idTag": ocpp_id,"timestamp":iso_time,"meterStart":meter_start,"reservationId":0}]
                ))
                response = await websocket.recv()
                print(response)
                output = json.loads(response)
                print("\nTransction ID: {} started".format(output[2]['transactionId']))
                transaction_id = output[2]['transactionId']

            if x == 'p':
                print("\nStop charge")
                iso_time = get_utc()
                # stop transaction
                await websocket.send(json.dumps(
                    [2, id,"StopTransaction",{"transactionId":transaction_id,"idTag": ocpp_id,"timestamp":iso_time,"meterStop":global_meter}]
                ))
                response = await websocket.recv()
                print(response)

            if x  == 'h':
                print("\nGet heartbeat")
                await websocket.send(json.dumps(
                    [2,id,"Heartbeat",{}]
                ))
                response = await websocket.recv()
                print(response)
            
            if x == 'c':
                # simulate charging for 1 minute

                charging_time = 10 # seconds
                _config = open_toml()
                running_meter = _config['meter']['connector_'+str(connector_id)]
                global_meter = running_meter
                curr = time.time()
                print("Charging for {} second(s)...".format(charging_time))
                while time.time() < curr + charging_time:

                    running_meter += round(math.pi, 4)
                    time.sleep(1)
                    iso_time = get_utc()
                    await websocket.send(json.dumps(
                        [2, id, "MeterValues",
                            {"connectorId": 1, "transactionId": transaction_id, "meterValue": [{"timestamp": iso_time, "sampledValue": [{"value": str(running_meter)}]}]
                            }
                        ]
                    ))
                    connector = 'connector_' + str(connector_id)
                    write_to_toml(connector, running_meter)
                    response = await websocket.recv()
                    #print(response)
                
                global_meter = running_meter

            if x == 'help':
                print_help()

            if x == 'q':
                print("\nClosing Application.")
                quit()

def print_help():
    """ help options """

    print('''
        This application will simulate a charge session with Steve CMS.

        Press 'a' to authorize a charge session
        Press 's' to start a transaction
        Press 'c' to automate charging
        Press 'p' to stop
        Press 'h' to get a heartbeat
        Press 'q' to quit application
    ''')

def get_utc():
    """ return utc time """

    now_utc = datetime.datetime.now()
    iso_time = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(iso_time)
    return iso_time

def open_toml():
    """ open toml configuration """

    with open('./config.toml', 'r') as f:
        config = toml.load(f)
    
    return config

def write_to_toml(param, value):
    """ write parameter to toml file """

    with open('./config.toml', 'r') as f:
        config = toml.load(f)
    
    print(config)
    
    if param == 'connector_1':
        config['meter']['connector_1'] = value
    
    if param == 'connector_2':
        config['meter']['connector_2'] = value
    
    with open('config.toml', 'w') as f:
        toml.dump(config, f)


if __name__ == '__main__':
    print_help()
    asyncio.run(run())
import requests
import json


def send_rpc_request(payload, relay_url):
    try:
        # Send the JSON-RPC request to the relay endpoint
        response = requests.post(relay_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        
        # Parse the JSON-RPC response
        if response.status_code == 200:
            data = response.json()
            # print(data)
            if 'result' in data:
                return response.text #return data['result']
            elif 'error' in data:
                raise Exception(f"JSON-RPC Error: {data['error']}")
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

    except Exception as e:
        raise Exception(f"Request error: {str(e)}")


payload_getcurrencystate = {
    'jsonrpc': '2.0',
    'method': 'getcurrencystate',
    'params': ["Bridge.vETH"],
    'id': 1
}

payload_getcurrencystate_last_hour = {
    'jsonrpc': '2.0',
    'method': 'getcurrencystate',
    'params': ["Bridge.vETH", "2758800,2758900,1"],
    'id': 1
}

relay_url = 'https://rpc.vrsc.komodefi.com/'
bridge_veth = {
    "VRSC": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV",
    "DAI.vETH": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM",
    "MKR.vETH": "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4",
    "vETH": "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"
    }

def getcurrencystate(payload):
    try:
        result = send_rpc_request(payload, relay_url)
        # print("Result:", result)
        return result
    except Exception as e:
        print(str(e))

def getcurrencystate_last_60(payload, height):
    payload['params'] = ["Bridge.vETH", f"{height-60},{height},10"]
    print(payload)
    print(height)
    try:
        result = send_rpc_request(payload, relay_url)
        # print("Result:", result)
        return result
    except Exception as e:
        print(str(e))


def fees_1():
    currentstate = json.loads(getcurrencystate(payload_getcurrencystate))['result']
    # print(currentstate)
    currencies = currentstate[0]['currencystate']['currencies']

    # print(currencies)
    save = {"currencies": []}
    save_c = []
    height = currentstate[0]['height']
    # print(height)
    save.update({"height": height})
    for currency_id, info in currencies.items():
        reserve_in = info['reservein']
        reserve_out = info['reserveout']
        currency_name = [name for name, cid in bridge_veth.items() if cid == currency_id]
        currency_name = currency_name[0] if currency_name else "Unknown"
        # print(f"Currency Name: {currency_name}, Currency ID: {currency_id}, Reserve In: {reserve_in}, Reserve Out: {reserve_out}")
        summary = {}
        summary.update({"currency": currency_name, "reservein": reserve_in, "reserveout": reserve_out})
        save_c.append(summary)

    save["currencies"] += save_c
    # print(json.dumps(save))


    last_60 = json.loads(getcurrencystate_last_60(payload_getcurrencystate_last_hour, height))['result']
    print(last_60)


def price_to_csv(base, rel):
    print("price to csv")
    currentstate = json.loads(getcurrencystate(payload_getcurrencystate))['result']
    height = currentstate[0]['height']
    last_60 = json.loads(getcurrencystate_last_60(payload_getcurrencystate_last_hour, height))['result']
    # print(last_60)
    for currency_state in last_60:
        print(currency_state['height'])
        reserves = currency_state.get("currencystate", {}).get("reservecurrencies", [])
        print(reserves)


if __name__=="__main__":
    # fees_1()
    price_to_csv("VRSC", "DAI.vETH")
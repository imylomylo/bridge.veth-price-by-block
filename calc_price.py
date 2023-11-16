import requests
import csv

def calculate_price(base, quote, height_data, lookup):
    # Extract currency IDs using the lookup dictionary.
    base_id = lookup.get(base)
    quote_id = lookup.get(quote)

    # Initialize prices for both currencies.
    price_base = None
    price_quote = None

    print(height_data)
    print(height_data['height'])
    # Iterate through the reservecurrencies in the currency state.
    for reserve_data in height_data['currencystate']['reservecurrencies']:
        if reserve_data['currencyid'] == base_id:
            price_base = reserve_data['priceinreserve']
        elif reserve_data['currencyid'] == quote_id:
            price_quote = reserve_data['priceinreserve']

    if price_base is not None and price_quote is not None:
        # Calculate the price based on the prices from both currencies.
        price = price_quote / price_base
        print(price)
        return f"{base}/{quote}", height_data['height'], price

    return None  # If either currency is not found in the response.

def price_to_csv(base_currency, quote_currency, height_range, lookup):
    # Replace with your RPC request to get the JSON response.
    url = 'https://rpc.vrsc.komodefi.com/'
    payload = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'getcurrencystate',
        "params": ["Bridge.vETH", height_range]
    }
    response = requests.post(url, json=payload).json()

    if "result" in response:
        data = response["result"]

        with open(f"{base_currency}_{quote_currency}.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Currency Pair", "Height", "Price"])

            for item in data:
                height = item["height"]
                result = calculate_price(base_currency, quote_currency, item, lookup)
                if result:
                    csv_writer.writerow(result)


def generate_csv(basket, height_range, base, quote,lookup):
    price_to_csv(base, quote, height_range, lookup)


if __name__=="__main__":
    # fees_1()
    lookup = {
        "VRSC": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV",
        "DAI.vETH": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM",
        "MKR.vETH": "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4",
        "vETH": "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"
    }
    height_range = "2757830,2775633,30"

    generate_csv("Bridge.vETH", height_range, "VRSC", "DAI.vETH", lookup)
    generate_csv("Bridge.vETH", height_range, "VRSC", "MKR.vETH", lookup)
    generate_csv("Bridge.vETH", height_range, "VRSC", "vETH", lookup)
    generate_csv("Bridge.vETH", height_range, "MKR.vETH", "DAI.vETH", lookup)
    generate_csv("Bridge.vETH", height_range, "MKR.vETH", "VRSC", lookup)
    generate_csv("Bridge.vETH", height_range, "MKR.vETH", "vETH", lookup)
    generate_csv("Bridge.vETH", height_range, "vETH", "DAI.vETH", lookup)
    generate_csv("Bridge.vETH", height_range, "vETH", "VRSC", lookup)
    generate_csv("Bridge.vETH", height_range, "vETH", "MKR.vETH", lookup)
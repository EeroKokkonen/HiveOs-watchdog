import sys
import requests
import json
from datetime import datetime
import pytz
import time
import subprocess

def main():
    iso_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    api_url = "https://api.porssisahko.net/v1/latest-prices.json"
    max_electric_price = 0
    if(len(sys.argv) == 1):
        try:
            with open('config.txt', 'r') as file:
                max_electric_price = float(file.read())
        except FileNotFoundError:
            print(f"Price not specified. Type \"{sys.argv[0]} <price (snt/kWh)>\"")
            return
        except ValueError:
            print("Price of electricity must be positive integer")
            return
        except Exception:
            print("Unkown error on opening config.txt file!")
            return

    if(len(sys.argv) > 1):
        try:
            max_electric_price = float(sys.argv[1])
            with open('config.txt', 'w') as file:
                file.write(str(max_electric_price))
        except ValueError:
            print("Price of electricity must be positive number")
            return
        except Exception:
            print("Unkown error on writing config.txt file!")
            return

    run = True
    while(run):

        today = datetime.strptime(datetime.now(pytz.timezone('UTC')).strftime(iso_format), iso_format)

        res = requests.get(api_url)
        response = json.loads(res.text)

        expensive_hours = []

        for data in reversed(response["prices"]):
            endDate = datetime.strptime(data["endDate"], iso_format)
            startDate = datetime.strptime(data["startDate"], iso_format)
            if data["price"] > max_electric_price and endDate > today:
                expensive_hours.append({
                        "price": data["price"],
                        "endDate": endDate,
                        "startDate": startDate
                    })
        # If there is no expensive hours, sleeps 12 hours and checks prices again
        if len(expensive_hours) == 0:
            time.sleep(12 * 60 * 60)
            print("Electricity is cheap, cheking new prices after 12 hours...")
            continue

        expensive_hours = get_chained_expensive_hours(expensive_hours)

        print(f"Next scheduled shutdown will be at {expensive_hours[0]['startDate']} - {expensive_hours[0]['endDate']}")

        time_to_shutdown = (expensive_hours[0]["startDate"] - today).total_seconds()

        if time_to_shutdown <= 0:
            time_to_shutdown = 0

        time.sleep(time_to_shutdown)

        print("Electricity price is high, shuttingdown..")
        shutdown_time = expensive_hours[0]["gapInSeconds"]

        subprocess.run(["sreboot", "wakealarm", str(shutdown_time)])
        time.sleep(shutdown_time)

        run = False



def get_chained_expensive_hours(expensive_hours):
    startDate = expensive_hours[0]["startDate"]
    endDate = startDate
    chained_expensive_hours = []
    # make chain from expensive hours
    for hours in expensive_hours:
        if endDate.date() != hours["startDate"].date() and endDate.time() != hours["startDate"].time():
            chained_expensive_hours.append({"startDate":startDate, "endDate": endDate, "gapInSeconds": (endDate - startDate).total_seconds()})
            print()
            startDate = hours["startDate"]

        endDate = hours["endDate"]

    chained_expensive_hours.append({"startDate":startDate, "endDate": endDate, "gapInSeconds": (endDate - startDate).total_seconds()})

    return chained_expensive_hours



if __name__ == "__main__":
    main()
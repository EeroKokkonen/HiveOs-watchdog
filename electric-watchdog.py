#!/usr/bin/env python3

import requests
import json
from datetime import datetime
import pytz
import time
import subprocess
import logging
import os

def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(message)s",
                        datefmt="%Y.%m-%d %H:%M:%S",
                        filename="electric-watchdog.log",
                        filemode="a")
    
    logger = logging.getLogger("watchdog-logger")
    logger.propagate = int(os.getenv('LOGGING', default=True))

        
        
    iso_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    api_url = "https://api.porssisahko.net/v1/latest-prices.json"
    max_electric_price = 0

    try:
        max_electric_price = float(os.getenv("PRICE"))
    except FileNotFoundError:
        logger.error(f"Price not specified. Set value to PRICE in .env file.")
        return
    except ValueError:
        logger.error("Price of electricity must be number")
        return
    except Exception as e:
        print("Unkown error!")
        logger.error(f"Error! {e}")
        return


    run = True
    while(run):

        today = datetime.strptime(datetime.now(pytz.timezone('UTC')).strftime(iso_format), iso_format)
        try:
            res = requests.get(api_url)
            response = json.loads(res.text)
        except Exception as e:
            logging.error(f"Error on fething data. {e}")

        expensive_hours = []

        for data in reversed(response["prices"]):
            endDate = datetime.strptime(data["endDate"], iso_format)
            startDate = datetime.strptime(data["startDate"], iso_format)

            if float(data["price"]) > max_electric_price and endDate > today:
                print(data)
                expensive_hours.append({
                        "price": data["price"],
                        "endDate": endDate,
                        "startDate": startDate
                    })

        # If there is no expensive hours, sleeps 12 hours and checks prices again
        if len(expensive_hours) == 0:
            logger.info(f"Electricity price is under {max_electric_price}, cheking new prices after 8 hours...")
            time.sleep(8 * 60 * 60)
            continue

        expensive_hours = get_chained_expensive_hours(expensive_hours)

        logger.info(f"Next scheduled shutdown will be at {expensive_hours[0]['startDate']} - {expensive_hours[0]['endDate']}")

        time_to_shutdown = (expensive_hours[0]["startDate"] - today).total_seconds()

        if time_to_shutdown <= 0:
            time_to_shutdown = 0

        time.sleep(time_to_shutdown)

        logger.info(f"Electricity price is over {max_electric_price}, shuttingdown..")
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
        if endDate.date() != hours["startDate"].date() or endDate.time() != hours["startDate"].time():
            chained_expensive_hours.append({"startDate":startDate, "endDate": endDate, "gapInSeconds": (endDate - startDate).total_seconds()})
            startDate = hours["startDate"]

        endDate = hours["endDate"]

    chained_expensive_hours.append({"startDate":startDate, "endDate": endDate, "gapInSeconds": (endDate - startDate).total_seconds()})

    return chained_expensive_hours



if __name__ == "__main__":
    main()
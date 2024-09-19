import json
import logging
import os
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

api_key = os.environ.get("api_key")
base_url = "https://calendarific.com/api/v2"
holiday_url = "/holidays"

countries_list = ["ua", "us", "gb"]
start_time = datetime(year=1992, month=7, day=7)
end_time = datetime(year=1992, month=9, day=18)


def convert_to_datetime(holiday_datetime: dict):
    try:

        return datetime(
            year=holiday_datetime["year"],
            month=holiday_datetime["month"],
            day=holiday_datetime["day"],
        )
    except Exception as e:
        logger.error(f"error: can not convert to datetime, details: {e}")


def send_request(url: str):
    try:
        result = requests.get(url=url)
        holidays = result.json()

        return holidays["response"]["holidays"]

    except Exception as e:
        logger.error(f"error: request without response, details: {e}")

    return


def save_data(country: str, holidays: list):
    start_date = start_time.strftime("%d-%m-%Y")
    end_date = end_time.strftime("%d-%m-%Y")
    file_name = f"{country}_{start_date}_{end_date}.txt"

    try:
        for holiday in holidays:
            with open(
                os.path.join("/test_task/expected_result", file_name),
                "a+",
            ) as f:
                f.write(json.dumps(holiday))
    except Exception as e:
        logger.error(f"error: can not write into file, details: {e}")


def collect_date():
    for country in countries_list:
        for year in range(start_time.year, end_time.year + 1):
            params = f"&country={country}&year={year}"
            url = f"{base_url}{holiday_url}?api_key={api_key}"

            if holidays := send_request(url=url + params):
                for holiday in holidays[:]:
                    holiday_datetime = holiday.get("date", {}).get("datetime")

                    if holiday_date := convert_to_datetime(holiday_datetime):
                        if (holiday_date < start_time) or (holiday_date > end_time):
                            holidays.remove(holiday)

                    else:
                        logger.info(f"error: api request has new scheme")

                save_data(country, holidays)


collect_date()

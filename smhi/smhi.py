import json
from builtins import NotImplemented
from pprint import pprint

import aiohttp
import asyncio
import async_timeout
from aiohttp.client import _RequestContextManager
from logging import getLogger

from exceptions.SmhiExceptions import SmhiConnectionException

BASE_URL = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{}/lat/{}/data.json'

logger = getLogger()


@asyncio.coroutine
def get_forecast(longitude: str, latitude: str) -> dict:
    with aiohttp.ClientSession() as session:
        url = BASE_URL.format(longitude, latitude)
        print(url)
        with async_timeout.timeout(10):
            try:
                response = yield from session.get(url)
                text = (yield from response.json())
            except Exception as e:
                text = yield from response.text()
                logger.exception("Could not fetch data from SMHI.")
                raise SmhiConnectionException("Could not fetch data from SMHI.")
            finally:
                yield from response.release()
            pprint(text)


def __check_response_for_error(response: aiohttp.ClientResponse):
    if 200 <= response.status < 300:
        raise Exception


def __format_response(response: json) -> json:
    NotImplemented()


loop = asyncio.get_event_loop()
loop.run_until_complete(get_forecast("18.176879", "59.237234"))

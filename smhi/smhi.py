from pprint import pprint

import aiohttp
import asyncio
import async_timeout

BASE_URL = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{}/lat/{}/data.json'


@asyncio.coroutine
def get_forecast(longitude: str, latitude: str) -> dict:
    with aiohttp.ClientSession() as session:
        url = BASE_URL.format(longitude, latitude)
        print(url)
        with async_timeout.timeout(10):
            response = yield from session.get(url)
            try:
                text = (yield from response.json())
            except Exception as e:
                text = yield from response.text()
            finally:
                yield from response.release()
            pprint(text)


loop = asyncio.get_event_loop()
loop.run_until_complete(get_forecast("18.176879", "59.237234"))

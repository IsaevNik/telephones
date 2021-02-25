import argparse
import asyncio
import csv
import re
from collections.abc import Iterable
from typing import List

import aiohttp
import logging


REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=2.0)


telephone_regexp = re.compile(
    r'[8|+7]\s?\(?\s?\d{3}\s?\)?\s?\d{3}\s?-?\s?\d{2}\s?-?\s?\d{2}|\d{3}\s?-\s?\d{2}\s?-\s?\d{2}'
)


def clear_number(raw_number: str) -> str:
    cleared_number = re.sub(r'\D', '', raw_number)
    if len(cleared_number) == 7:
        # for moscow number without code
        return f'8495{cleared_number}'
    return cleared_number


def get_result_by_regexp(regexp: re.Pattern, text: str) -> List[str]:
    result = regexp.findall(text)
    return [clear_number(i) for i in result]


async def get_html(url: str) -> str:
    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_telephone_number_from_site(url: str) -> List[str]:
    try:
        html = await get_html(url)
    except aiohttp.ClientError as err:
        logging.error('%s request error %s', url, err)
        return []

    result = get_result_by_regexp(telephone_regexp, html)
    return list(set(result))


async def parse_telephone_numbers(urls):
    results = await asyncio.gather(*[
        parse_telephone_number_from_site(url) for url in urls
    ], return_exceptions=True)

    for i, phones in enumerate(results):
        if not isinstance(phones, Iterable):
            phones = []
        print(f'{urls[i]}: {phones}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='csv file with site urls')
    parser.add_argument('urls', nargs='*', default=[])
    args = parser.parse_args()

    if args.file and not args.urls:
        reader = csv.reader(args.file, delimiter=';')
        urls = [row[0] for row in reader]
    else:
        urls = args.urls
    asyncio.run(parse_telephone_numbers(urls))

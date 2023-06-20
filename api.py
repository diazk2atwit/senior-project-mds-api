import httpx
import asyncio
import hashlib
from decouple import config

API_KEY = config('API_KEY')


async def scan_url(url):
    api_url = "https://www.virustotal.com/api/v3/urls"

    payload = f"url={url}"
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY,
        "content-type": "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, data=payload, headers=headers)

        response_id = response.json()['data']['id'].split("-")[1]
        api_url = f"https://www.virustotal.com/api/v3/urls/{response_id}"

        headers = {
            "accept": "application/json",
            "x-apikey": API_KEY
        }

        response = await client.get(api_url, headers=headers)

        while response.status_code != 200:
            await asyncio.sleep(5)
            response = await client.get(api_url, headers=headers)

        return response.json()['data']['attributes']['last_analysis_stats']


async def scan_file(file_name):
    api_url = "https://www.virustotal.com/api/v3/files"

    files = {"file": (file_name, open(file_name, "rb"))}

    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, files=files, headers=headers)

        file_hash = hash_file(file_name)
        api_url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

        headers = {
            "accept": "application/json",
            "x-apikey": API_KEY
        }

        response = await client.get(api_url, headers=headers)

        while response.status_code != 200:
            await asyncio.sleep(5)
            response = await client.get(api_url, headers=headers)

        return response.json()['data']['attributes']['last_analysis_stats']

        # First instance of a new file returns all zeros because your parsing the json for last submission,
        # which would be all zeros if it's the first time scanning


def hash_file(file_name):
    hash_object = hashlib.md5()

    with open(file_name, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            hash_object.update(chunk)

    return hash_object.hexdigest()

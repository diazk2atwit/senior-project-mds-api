from fastapi import *
from api import *
from test import *
from database import *
from mangum import Mangum
import asyncio

app = FastAPI()
handler = Mangum(app)


#############
# Functions #
#############
def hash_file(file_name):
    hash_object = hashlib.sha256()

    with open(file_name, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            hash_object.update(chunk)

    print(hash_object.hexdigest())
    return hash_object.hexdigest()


@app.get('/', status_code=200)  # use http://127.0.0.1:8000/get_url_report?url= within search bar
async def home():
    return {'Malware Detection System (MDS) API'}


# @app.get('/get_url_report', status_code=200)  # use http://127.0.0.1:8000/get_url_report?url= within search bar
# async def get_url_report(url: str):
#     result = await scan_url(url)
#     # print(result)
#     return result


# @app.post('/send_url', status_code=201)
# def send_url():
#     return {"Success": "URL Sent"}


# @app.get('/get_file_report', status_code=200)
# async def get_file_report(file_name):
#     result = await scan_file(file_name)
#     # print(result)
#     return result


# @app.post("/get_file_report", status_code=201)
# async def get_file_report(file: UploadFile = File(...)):
#     try:
#         contents = file.file.read()
#         with open("file", 'wb') as f:
#             f.write(contents)
#             f.close()
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()
#
#     # print(file.filename)
#     result = await scan_file("file")
#
#     return result


@app.post("/TEST_post_file_report", status_code=201)
async def get_file_report(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open("file", 'wb') as f:
            f.write(contents)
            f.close()
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    hash_of_file = hash_file("file")

    # Checks Database and Returns if Found
    temp = get_file_doc(hash_of_file)
    if temp is not None:
        print("Found in Database")
        return temp

    print(file.filename)
    result = await test_scan_file("file")

    return result


@app.get("/TEST_get_file_report", status_code=200)
async def get_file_report():
    hash_of_file = hash_file("file")
    await asyncio.sleep(5)
    result = await test_retrieve_file("file")
    print(result)

    insert_file_doc(hash_of_file, result)

    return result


@app.get("/TEST_get_url_report", status_code=200)
async def test_get_url_report(url: str):

    # Checks Database and Returns if Found
    temp = get_url_doc(url)
    if temp is not None:
        print("Found in Database")
        return temp

    # Scans URL and returns the report in json
    result = await test_scan_url(url)

    insert_url_doc(url, result)

    print("URL Added to Database")
    return result

from fastapi import *
from api import *
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)


@app.get('/', status_code=200)  # use http://127.0.0.1:8000/get_url_report?url= within search bar
async def get_url_report(url: str):
    return {'Malware Detection System (MDS) API'}


@app.get('/get_url_report', status_code=200)  # use http://127.0.0.1:8000/get_url_report?url= within search bar
async def get_url_report(url: str):
    result = await scan_url(url)
    # print(result)
    return result


# @app.post('/send_url', status_code=201)
# def send_url():
#     return {"Success": "URL Sent"}


# @app.get('/get_file_report', status_code=200)
# async def get_file_report(file_name):
#     result = await scan_file(file_name)
#     # print(result)
#     return result


@app.post("/upload", status_code=201)
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open("file", 'wb') as f:
            f.write(contents)
            f.close()
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    # print(file.filename)
    result = await scan_file("file")

    return result

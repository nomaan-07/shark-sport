from fastapi import APIRouter, File
from fastapi import UploadFile
from urllib.parse import quote
from dotenv import load_dotenv
from datetime import datetime
import uuid, os, boto3

from middleware.auth_middleware import user_auth_middleware, decode_token, admin_auth_middleware

load_dotenv()

LIARA_ENDPOINT = os.getenv("LIARA_ENDPOINT")
LIARA_ACCESS_KEY = os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY = os.getenv("LIARA_SECRET_KEY")
LIARA_BUCKET_NAME = os.getenv("LIARA_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    endpoint_url=LIARA_ENDPOINT,
    aws_access_key_id=LIARA_ACCESS_KEY,
    aws_secret_access_key=LIARA_SECRET_KEY,
)


def current_time() -> datetime: 
    time = datetime.now().replace(second=0, microsecond=0)
    
    return time


class BucketObj():
    def __init__(self, file: UploadFile | None, save_name, destination, format_ = "jpg") -> None:
        self.file = file
        self.destination = destination
        self.save_name = save_name
        self.format_ = format_


    def upload_image(self):
        upload_resp = s3.upload_fileobj(self.file, 
                                        LIARA_BUCKET_NAME, 
                                      f'{self.destination}/{self.save_name}.{self.format_}')
        return upload_resp
    

    def perma_link(self):
        obj_filename_encoded = quote(f'{self.destination}/{self.save_name}.{self.format_}')
        obj_perma_link = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{obj_filename_encoded}"
        return obj_perma_link
    


router = APIRouter(
    prefix="/tools"
)

@router.post("/avatar", status_code=201)
def upload_avatar(avatar: UploadFile=File(...)):
    result = BucketObj(avatar.file, "maow","/images", format_="png")
    result.upload_image()
    link = result.perma_link()
    return link

    


@router.post("/user_middleware", status_code=200)
def test_user_middleware(token: str):
    return {"token":user_auth_middleware(token),
            "decode": decode_token(token)}


@router.post("/admin_middle", status_code=200)
def test_admin_token(toke:str):
    return {"decode": decode_token(toke)}
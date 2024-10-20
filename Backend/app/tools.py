from fastapi import APIRouter, File
from fastapi import UploadFile
from urllib.parse import quote
from dotenv import load_dotenv
from datetime import datetime
import uuid, os, boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from typing import List, Optional
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
    return datetime.now().replace(second=0, microsecond=0)
    



class BucketObj:
    """Version1 support multiple image uploading and permalink method"""
    def __init__(self, files: list[Optional[UploadFile]], save_names: list[str], destination: str, format_: str = "jpg") -> None:
        self.files = files
        self.save_names = save_names
        self.destination = destination
        self.format_ = format_

    def upload_images(self) -> None:
        for file, save_name in zip(self.files, self.save_names):
            try:
                if not file:
                    raise ValueError(f"File for {save_name} is None")
                s3.upload_fileobj(
                    file.file,
                    LIARA_BUCKET_NAME,
                    f'{self.destination}/{save_name}.{self.format_}'
                )
            except (NoCredentialsError, PartialCredentialsError) as e:
                raise RuntimeError(f"Credential error for file {save_name}: {str(e)}")
            except ValueError as e:
                raise ValueError(f"Error with file {save_name}: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Failed to upload {save_name}: {str(e)}")

    def perma_links(self) -> list[str]:
        links = []
        for save_name in self.save_names:
            obj_filename_encoded = quote(f'{self.destination}/{save_name}.{self.format_}')
            obj_perma_link = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{obj_filename_encoded}"
            links.append(obj_perma_link)
        return links


class BucketObj_2:
    """Version2 support multiple image uploading. permalink works as attribute and returns links
    as a list"""

    def __init__(self, files: List[Optional[UploadFile]], save_names: List[str], destination: str, format_: str = "jpg") -> None:
        self.files = files
        self.save_names = save_names
        self.destination = destination
        self.format_ = format_
        self.perma_links = self.generate_perma_links()

    def upload_images(self) -> None:
        for file, save_name in zip(self.files, self.save_names):
            try:
                if not file:
                    raise ValueError(f"File for {save_name} is None")
                s3.upload_fileobj(
                    file.file,
                    LIARA_BUCKET_NAME,
                    f'{self.destination}/{save_name}.{self.format_}'
                )
            except (NoCredentialsError, PartialCredentialsError) as e:
                raise RuntimeError(f"Credential error for file {save_name}: {str(e)}")
            except ValueError as e:
                raise ValueError(f"Error with file {save_name}: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Failed to upload {save_name}: {str(e)}")

    def generate_perma_links(self) -> List[str]:
        links = []
        for save_name in self.save_names:
            obj_filename_encoded = quote(f'{self.destination}/{save_name}.{self.format_}')
            obj_perma_link = f"https://{LIARA_BUCKET_NAME}.{LIARA_ENDPOINT.replace('https://', '')}/{obj_filename_encoded}"
            links.append(obj_perma_link)
        print("Generated perma_links: ", links)  # Debug print statement
        return links





router = APIRouter(prefix="/tools")

@router.post("/avatar", status_code=201)
def upload_avatar(avatar: List[UploadFile] = File(...)):
    """Test Image Uploading. Note: image links will not save on DB and only image objs will be
    save into the bucket
    """
    return BucketObj_2(avatar, ["save_name_1", "save_name_2", "save_name_3"], "/images", format_="png").perma_links


@router.post("/user_middleware", status_code=200)
def test_user_middleware(token: str):
    return {"token":user_auth_middleware(token),
            "decode": decode_token(token)}


@router.post("/admin_middle", status_code=200)
def test_admin_token(toke:str):
    return {"decode": decode_token(toke)}
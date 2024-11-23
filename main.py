from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from concurrent.futures import ThreadPoolExecutor
from convert import Doc2Pdf
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DIRNAME = "../output"

converter = Doc2Pdf(DIRNAME)

@app.post("/convert")
async def convert(file: UploadFile, password: Optional[str] = Form()):
    try:
        if not file or not file.filename or not file.file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        name = file.filename
        print(file, password)
        if converter.is_valid_file(name) is False:
            raise HTTPException(status_code=400, detail="Invalid file format")
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, name)
            with open(input_path, "wb") as f:
                f.write(file.file.read())
            file_hash = converter.generate_file_hash(input_path)
            output_name = (name.replace(".docx","").replace(".doc","")+"-"+file_hash[:8]+".pdf")
            with ThreadPoolExecutor() as executor:
                output = executor.submit(converter.convert_single, input_path, output_name).result()
                if password is not None and password != "":
                    print("Password Protecting")
                    executor.submit(converter.password_protect, output, password)

        return {"path":output_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e} ")

class FileMetadata(BaseModel):
    name: str
    size: str
    type: str
    passwordProtected: bool

@app.post("/convert-bulk")
async def convert_bulk(files: List[UploadFile], passwordProtect: str = Form(),  password: Optional[str] = Form()):
    """
    files: is a list of files
    passwordProtect: is a string of 0 and 1, where 1 means the file on that index should be password protected
    password: is a string of password to be used for password protection
    """
    try:
        names = []
        for file in files:
            names.append(file.filename)
            if converter.is_valid_file(file.filename) is False:
                raise HTTPException(status_code=400, detail="No file uploaded")
        with tempfile.TemporaryDirectory() as temp_dir:
            input_paths = []
            for file in files:
                name = file.filename
                if not name:
                    raise HTTPException(status_code=400, detail="No file uploaded")
                input_path = os.path.join(temp_dir, name)
                with open(input_path, "wb") as f:
                    f.write(file.file.read())
                input_paths.append(input_path)
            outputs = []
            for path, name, pp in zip(input_paths, names, passwordProtect):
                file_hash = converter.generate_file_hash(path)
                output_name = (name.replace(".docx","").replace(".doc","")+"-"+file_hash[:8]+".pdf")
                with ThreadPoolExecutor() as executor:
                    opt = executor.submit(converter.convert_single, path, output_name).result()
                    outputs.append(output_name)
                    if password is not None and password != "" and pp == "1":
                        executor.submit(converter.password_protect, opt, password)
        return {"files":outputs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e} ")

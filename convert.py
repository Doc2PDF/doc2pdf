from PyPDF2 import PdfReader, PdfWriter
import subprocess
import os
import hashlib

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

class Doc2Pdf():
    def __init__(self, output_dir):
        self.output_dir = os.path.join(os.getcwd(), output_dir)

    def convert_single(self, file_path: str, output_name: str):
        output = os.path.join(self.output_dir, output_name)
        try:
            if not HOST or not PORT:
                raise RuntimeError("HOST or PORT not set")
            subprocess.run(["unoconvert", "--host", HOST, "--port", PORT ,"--host-location", "remote", file_path, output], check=True)
            return output
        except:
            raise RuntimeError("Failed to convert the file")

    def password_protect(self, output: str, password:str):
        reader = PdfReader(output)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        with open(output, "wb") as f:
            writer.write(f)

    def is_valid_file(self, file_path):
        return file_path.endswith(".docx") or file_path.endswith(".doc")

    def generate_file_hash(self, file_path):
        try:
            hash_func = getattr(hashlib, 'sha256')()
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)

            return str(hash_func.hexdigest())
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {e}"

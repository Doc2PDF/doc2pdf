# Doc2Pdf

The is the main service which utilizes the `unoserver` to convert the doc files to pdf files.

There are 2 routes:
- /convert - which takes a doc file and converts it to pdf
- /convert-bulk - it is used to bulk convert files

Additionally, **password** can be passed to these two endpoints to encrypt the pdf files.

Other repositories:
- [Storage Service](https://github.com/Doc2PDF/storage)
- [Platform](https://github.com/Doc2PDF/platform)
- [Deployment Scripts](https://github.com/Doc2PDF/deployments)

## Running the app
#### Steps to run the app:

- `python3 -m venv venv` to create the virtual env.
- `source venv/bin/activate` to activate the virtual env.
- `pip install -r requirements.txt` to install the dependencies
- `make` to run the server
- `make docker` to build and run the docker image

## Running the stack

To run the whole stack, use this [Dockerfile](https://github.com/Doc2PDF/deployments/blob/main/docker-compose.yaml).
`docker compose up -d --build`

## Technologies/Libraries Used
- Python
- FastAPI
- PyPDF2
- unoconv

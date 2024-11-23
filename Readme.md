# Doc2Pdf

The is the main service which utilizes the `unoserver` to convert the doc files to word files.

There are 2 routes:
- /convert - which takes a doc file and converts it to pdf
- /convert-bulk - it is used to bulk convert files

Additionally, password can be passed to these two endpoints to encrypt the pdf files.

Other repositories:
- [Storage Service](https://github.com/Doc2PDF/storage)
- [Platform](https://github.com/Doc2PDF/platform)
- [Deployment Scripts](https://github.com/Doc2PDF/deployments)

## Running the app

- `pip install -r requirements.txt` to install the dependencies
- `make` to run the server
- `make docker` to build and run the docker image

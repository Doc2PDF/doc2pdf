all: run

run:
	uvicorn main:app --host 0.0.0.0 --reload

docker:
	docker build . -t doc2pdf && docker run -p 8000:11010 -d --name doc2pdf doc2pdf

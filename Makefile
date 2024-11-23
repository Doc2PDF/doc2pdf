all: run

run:
	uvicorn main:app --host 0.0.0.0 --reload

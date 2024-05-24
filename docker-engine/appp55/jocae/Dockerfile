FROM arm32v7/python:3.11-slim-buster

WORKDIR /appp55

COPY ./appp55/requirements-appp55.txt /appp55/

RUN pip install -r requirements-appp55.txt

COPY ./appp55/jocae/jocae.py /appp55/jocae/

CMD ["python", "jocae.py"]
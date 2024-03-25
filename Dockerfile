
FROM python:3.8-slim-buster

WORKDIR c:\Users\hessc\Desktop\Dockerize attempt\JumpCutGenius-main\app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

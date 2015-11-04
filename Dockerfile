FROM python
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "parse.py"]

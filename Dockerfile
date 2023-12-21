FROM python

WORKDIR /api

COPY requirements.txt .
COPY main.py .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]
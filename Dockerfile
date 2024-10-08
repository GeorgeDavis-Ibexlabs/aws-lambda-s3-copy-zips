FROM python:3-slim

COPY . /action/workspace

WORKDIR /action/workspace

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/action/workspace/handler.py"]
ENTRYPOINT ["python3", "-u"]
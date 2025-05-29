FROM python:3.12 AS prod

RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install ffmpeg libsm6 libxext6  -y && \
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR app/
COPY src /app/src
COPY config /app/config
COPY app.py /app/

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
COPY Makefile /app
RUN make download_weights
CMD python -m uvicorn app:create_app --host='0.0.0.0' --port=80


FROM prod AS dev

COPY requirements.dev.txt /app/
RUN pip install --no-cache-dir -r requirements.dev.txt

COPY tests /app/tests
COPY setup.cfg Makefile /app/

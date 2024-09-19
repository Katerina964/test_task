FROM python:3.9
WORKDIR /test_task
COPY requirments.txt .
RUN pip install --upgrade pip && pip install -r requirments.txt
COPY . /test_task

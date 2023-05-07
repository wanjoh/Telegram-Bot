FROM python:3.10

ENV TOKEN ${TOKEN}

EXPOSE 5000

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /code
COPY *.py /code
RUN chmod +x /code/bot.py

CMD python3 /code/bot.py
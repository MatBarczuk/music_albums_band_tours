FROM python:3.9

ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src/app

COPY requirements.txt /src/app
RUN pip install -r requirements.txt

ENV FLASK_APP=setup.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=development

COPY . /src/app



EXPOSE $FLASK_RUN_PORT

CMD ["flask", "run"]
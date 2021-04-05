FROM python:3.8

COPY . /opt/services/star-wars/
COPY requirements.txt /opt/services/starwars/
WORKDIR /opt/services/star-wars/starwars
RUN pip install -r ../requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
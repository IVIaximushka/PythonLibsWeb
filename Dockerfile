FROM joyzoursky/python-chromedriver:3.9
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install -r requirements.txt
CMD python manage.py migrate
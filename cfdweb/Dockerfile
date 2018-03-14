FROM python:3.6

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install django
RUN pip install gensim
EXPOSE 8000
CMD ["python","/code/manage.py","runserver","0.0.0.0:8000"]

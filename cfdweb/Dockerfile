FROM python:3.6

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install django
RUN pip install gensim
RUN pip install sklearn
RUN pip install nltk
RUN pip install requests
EXPOSE 8000
CMD ["python","/code/manage.py","runserver","0.0.0.0:8000"]

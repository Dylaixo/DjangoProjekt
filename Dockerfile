FROM ubuntu
RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils 
RUN apt-get -y install python3 libapache2-mod-wsgi-py3 
RUN apt-get -y install python3-pip 
RUN pip install --upgrade pip 
RUN pip install django ptvsd 
RUN mkdir /home/django/DjangoProjekt -p
WORKDIR /home/django/DjangoProjekt
COPY ./django.conf /etc/apache2/sites-available/django.conf
COPY ./config.json /etc/config.json
ADD ./requirements.txt /home/django/DjangoProjekt/
RUN pip install -r requirements.txt
COPY . /home/django/DjangoProjekt/
RUN chmod 664 /home/django/DjangoProjekt/db.sqlite3
RUN chmod 775 /home/django/DjangoProjekt/*
RUN chown :www-data /home/django/DjangoProjekt/*
RUN a2ensite django
RUN a2dissite 000-default.conf
RUN python3 manage.py makemigrations main
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput
EXPOSE 80 3500
CMD ["apache2ctl", "-D", "FOREGROUND"]

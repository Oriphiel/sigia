#!/usr/bin/env sh
source /home/dariov/Trabajo/virtualenvs/sigia/bin/activate
./manage.py sqlflush | ./manage.py dbshell
./manage.py syncdb --noinput
./manage.py createsuperuser --username=dariov --email=dvazquez@aitec.edu.ec
./manage.py populate_db

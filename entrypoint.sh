#!/bin/sh
python shop_project/manage.py makemigrations
python shop_project/manage.py migrate
sh ./wait-for.sh
exec "$@" 

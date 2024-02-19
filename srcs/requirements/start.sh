#!/bin/bash

#if [ ! "$1" ]; then
#  echo -e "\e[31mError: parameter not found\e[0m"
#  exit 1
#fi

# For running docker compose
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python3 main/manage.py createcachetable
    python3 main/manage.py makemigrations --noinput
    python3 main/manage.py migrate --noinput
    python3 main/manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL"
    #python3 main/manage.py runserver_plus --cert-file key/cert.pem --key-file key/key.pem
    if [ "$1" ]; then
      python3 main/manage.py runserver "$1"
    fi

# Just to run the script
elif [ -f ".env" ]; then
    str="$(sed 's/#.*//g' < ".env" | xargs | envsubst)"
    if [ -z "$str" ]; then
      echo -e "\e[31mError: str='$str' file is empty or an error occurred while processing.\e[0m"
      exit 1
    fi
    IFS=' ' read -ra elements <<< "$str"
    for element in "${elements[@]}"; do
        if [[ "$element" =~ '=' && "$element" =~ =.*$ ]]; then
            if [ -z "${element#*=}" ]; then
                echo -e "\e[31mError: '$element' is not in the expected format or is blank.\e[0m"
                exit 1
            fi
        else
            echo -e "\e[31mError: '$element' is not in the expected format or is blank.\e[0m"
            exit 1
        fi
    done
    username="$(echo "$str" | awk -F '=' '{print $2}' | awk '{print $1}')"
    mail="$(echo "$str" | awk -F '=' '{print $3}'| awk '{print $1}')"
    echo -e "username='$username' mail ='$mail'"
    python3 main/manage.py createcachetable
    python3 main/manage.py migrate --noinput
    python3 main/manage.py makemigrations --noinput
    python3 main/manage.py createsuperuser \
        --noinput \
        --username "$username" \
        --email "$mail"
    #python3 main/manage.py runserver_plus --cert-file key/cert.pem --key-file key/key.pem
    python3 main/manage.py runserver "$1"
else
    echo -e "\e[31mUsername not found\e[0m"
    exit 1
fi

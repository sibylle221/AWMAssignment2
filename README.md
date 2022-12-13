# AWMAssignment2

Advanced Web Mapping CA Assignment 2

Site is at http://www.propelhealth.online/

Had a few issues.

Had an issue with the Django container running on digitalocean and fixed this with sudo apt install qemu-user-static.
This is because M1 chips have issues running containers and images on DigitalOcean. (the architecture is not fully compatible).

Web app works locally and online and stores information about the users including the form info, date the user was created and the last location.

Tested and it has responsive design on phone screens (used fn key and f12 in the browser to test for responsive design.

nginx, certbot, digitalocean and dockerhub all up and running.

ssh keys working fine .

Project deployed and displays petrol stations in ireland, along with the street they're on and the city they're in.

I used the domain name propelhealth.online because since i was paying for the domain name, I was going to use it for my FYP :)

## Deployment

I created a droplet on DigitalOcean with docker installed on an ubuntu OS.
In the dommain settings, I copied the nameservers from digital ocean to my settings for DNS on NameCheap, then added an A record to my DigitalOcean domain settings. This would redirect people to my droplet's ip when they searched for the domain name propelhealth.online.

I went onto the console within the droplet and created a docker network on the VM using:

    "docker network create awm_network"

nginx was also installed on the droplet.

A Dockerfile was created after cding into the snap directory.
The Dockerfile container the following:

FROM nginx
MAINTAINER Mark Foley
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install software-properties-common certbot python3-certbot-nginx

The nginx image was then created with:

"docker build -t awm_certbot ."

Then the container was created:

"docker create --name awm_certbot --network awm_network --network-alias awm-certbot -p 80:80 -p 443:443 -t -v wmap_web_data:/usr/share/nginx/html -v $HOME/awm_certbot/conf:/etc/nginx/conf.d -v /etc/letsencrypt:/etc/letsencrypt -v /var/www/certbot awm_certbot"

The container was started and ran with:

"docker start awm_certbot"

I SSH into the new container using:

"docker exec -it awm_certbot /bin/bash"

And then created a cert using

"certbot certonly --nginx"

PgAdmin and PostGIS docker containers were created next:

"docker create --name wmap_pgadmin4 --network awm_network --network-alias wmap-pgadmin4 -t -v wmap_pgadmin_data:/var/lib/pgadmin -e 'PGADMIN_DEFAULT_EMAIL=C19305471@mytudublin.ie' -e 'PGADMIN_DEFAULT_PASSWORD=admin' dpage/pgadmin4"

"docker create --name wmap_postgis --network awm_network --network-alias awm-postgis -t -v wmap_postgis_data:/var/lib/postgresql -e 'POSTGRES_USER=docker' -e 'POSTGRES_PASS=docker' kartoza/postgis"

Each container was started with the docker start command:

"docker start container_name"

Docker ps was ran to check the containers were running correctly and docker logs container_name was ran to ensure they were correct.

An image was built on my laptop using:

"docker build --platform linux/amd64 -t sibylle221/awm ."

It was necessary to add in the additional specifications as my laptop is a macbook and defaulted to the incorrect architecture for deployment.

The image was then pushed to dockerhub using:

"docker push sibylle221/awm:latest"

I used docker login on the console of the droplet on DigitalOcean to login to my docker account and pulled the image to the droplet using:

"docker pull sibylle221/awm"

A container was made with this image using:

"docker create --name geodjango_tutorial --network awm_network --network-alias wmap-django -t sibylle221/awm"

Next step was to SSH back into the nginx container using:

"docker exec -it awm_certbot /bin/bash"

And installed nano using:

"apt-get install nano"

I then created a headers.conf file and a server.conf file within the conf directory.

The container was started using:

"docker start geodjango_tutorial"

I then SSH into my container with the django application installed on it

"docker exec -it geodjango_tutorial /bin/bash"

I ran make migrations:

"python manage.py makemigrations"

I ran migrate:

"python manage.py migrate"

I ran the collect static command:

"python manage.py collectstatic --no-input"

These commands ran successfully.

The container and the database container were able to communicate and were working.

# Additions

Done through overpass

I put the geojson file in the pycharm project, then from script.js I fetched it and added it as a layer and added it to the map.

I looked at custom markers however I ultimately preferred the default. I used this as a guide:

https://www.youtube.com/watch?v=EkBEJ59Ak1I

I also added in additional information to be displayed when a marker is clicked such as city, streetname and brand of the petrol station.

I made the app a PWA using:

https://www.geeksforgeeks.org/make-pwa-of-a-django-project/
and
https://github.com/silviolleite/django-pwa/commit/ab3e7fa62a97ebf121b0c96344f107f18243aabd

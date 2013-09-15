#!/bin/bash
dropdb newdjangosite_staging
createdb --locale en_US.UTF-8 --encoding UTF8 --template template0 newdjangosite_staging
pg_dump --format=custom newdjangosite_prod > newdjangosite_prod.dump
pg_restore --dbname=newdjangosite_staging newdjangosite_prod.dump
rm newdjangosite_prod.dump
echo newdjangosite_prod copied to newdjangosite_staging!


#!/bin/sh
# check_postgres.sh
pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER

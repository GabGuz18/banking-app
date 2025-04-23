#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

python << END
import sys
import time
import psycopg2
suggest_unrecoverable_after = 30
start = time.time()
while True:
    try:
        psycopg2.connect(
          dbname="${POSTGRES_DB}",
          user="${POSTGRES_USER}",
          password="${POSTGRES_PASSWORD}",
          host="${POSTGRES_HOST}",
          port="${POSTGRES_PORT}",
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Waiting for PostgreSQL to become available...\n")
        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write("PostgreSQL is taking too long to become available. '{}'\n".format(error))
        time.sleep(3)
END

echo >&2 "PostrgeSQL is available. Starting Django server..."

exec "$@"

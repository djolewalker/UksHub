#!/bin/bash

# wait for MySql to start
function mysql_ready() {
    python << END
import sys
import mysql.connector
try:
    conn = mysql.connector.connect(user='root',password='1234',host='db')
except mysql.connector.Error as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}

until mysql_ready; do
    >&2 echo "MySql is unavailable - sleeping"
    sleep 1
done

# Start app
>&2 echo "MySql is up - executing command"

./scripts/create-public-key.sh
./scripts/start-django.sh
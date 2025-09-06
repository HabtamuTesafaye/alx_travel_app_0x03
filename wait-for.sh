#!/bin/sh
# wait-for.sh

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 5672; do
  echo "RabbitMQ is unavailable - sleeping"
  sleep 1
done

echo "RabbitMQ is up - executing command"
exec $cmd
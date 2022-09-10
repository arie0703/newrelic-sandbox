# !bin/bash
source ../.env

gzip -c twitter.json | curl --data-binary @- -X POST \
-H "Content-Type: application/json" \
-H "X-Insert-Key: $NEWRELIC_KEY" \
-H "Content-Encoding: gzip" \
$NEWRELIC_ENDPOINT
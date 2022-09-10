# !bin/bash
source .env

json="{ \
\"eventType\": \"test\",
\"category\": \"hogehoge\",
\"count\": 300
}"

echo $json > example.json

gzip -c example.json | curl --data-binary @- -X POST \
-H "Content-Type: application/json" \
-H "X-Insert-Key: $NEWRELIC_KEY" \
-H "Content-Encoding: gzip" \
$NEWRELIC_ENDPOINT

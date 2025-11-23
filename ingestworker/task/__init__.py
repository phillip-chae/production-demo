QUEUE = "ingestworker"
INGEST_SUFFIX = ".ingest"

INGEST_TASK = QUEUE + INGEST_SUFFIX

task_routes = { QUEUE + ".*": { "queue": QUEUE } }
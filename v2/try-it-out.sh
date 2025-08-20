#!/usr/bin/env bash

set -eou pipefail

docker exec -it spark-master spark-sql \
    --packages org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.9.2 \
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
    --conf spark.sql.catalog.lake=org.apache.iceberg.spark.SparkCatalog \
    --conf spark.sql.catalog.lake.type=rest \
    --conf spark.sql.catalog.lake.uri=http://nessie:19120/iceberg \
    --conf spark.sql.defaultCatalog=lake


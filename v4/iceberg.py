from pyspark.sql import SparkSession

# Create SparkSession directly (no Spark Connect)
spark = (
    SparkSession.builder.appName("IcebergTest")
    .config(
        "spark.sql.extensions",
        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
    )
    .config("spark.sql.catalog.nessie", "org.apache.iceberg.spark.SparkCatalog")
    .config(
        "spark.sql.catalog.nessie.catalog-impl",
        "org.apache.iceberg.nessie.NessieCatalog",
    )
    .config("spark.sql.catalog.nessie.uri", "http://nessie:19120/api/v1")
    .config("spark.sql.catalog.nessie.ref", "main")
    .config("spark.sql.catalog.nessie.warehouse", "s3a://warehouse/")
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .config("spark.hadoop.fs.s3a.access.key", "minio")
    .config("spark.hadoop.fs.s3a.secret.key", "minio123")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .getOrCreate()
)

# Switch to Iceberg catalog
spark.sql("USE CATALOG nessie")

# Create table with absolute S3A path
spark.sql("""
CREATE TABLE IF NOT EXISTS test_table (
    id BIGINT,
    name STRING
)
USING ICEBERG
LOCATION 's3a://warehouse/test_table'
""")

# Insert sample data
spark.sql("""
INSERT INTO test_table VALUES
(1, 'Alice'),
(2, 'Bob'),
(3, 'Charlie')
""")

# Query the table
df = spark.sql("SELECT * FROM test_table")
df.show()

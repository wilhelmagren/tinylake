from pyspark.sql import SparkSession

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

df = spark.sql("SELECT * FROM nessie.test_table")
df.show()

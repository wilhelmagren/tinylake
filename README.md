# tinylake

Tiny lakehouse setup.


## Components

- **MinIO** object storage (S3)
- **Apache Iceberg** data table format
- **Project Nessie**
- **Apache Spark**
 - both worker and master


 1️⃣ Spark + Comet

Spark: Your main distributed processing engine.

Comet: A Spark plugin that accelerates execution using DataFusion vectorized engine and optimized shuffle.

Works on top of Spark, so Spark must be installed and configured with Comet JARs.

2️⃣ Kyuubi

Kyuubi is a multi-tenant SQL server for Spark (like HiveServer2 for Spark).

Lets you run SQL queries against Spark without managing separate Spark sessions manually.

Plays nicely with Spark + Comet:

You just make sure Kyuubi launches Spark sessions with the Comet plugin enabled (via spark-defaults.conf or session configs).

3️⃣ Nessie + Iceberg

Iceberg: Open table format for big data (like Delta Lake). Supports schema evolution, ACID, and snapshots.

Nessie: Git-like catalog for Iceberg tables (branches, commits).

Interaction:

Spark can read/write Iceberg tables via Nessie as the catalog.

Comet doesn’t care about the table format; it just accelerates Spark’s execution.

4️⃣ Doris

Apache Doris: OLAP analytic database.

You can use Spark to read from/write to Doris via connectors.

Comet accelerates Spark queries, but Doris is just another data source or sink.

5️⃣ MinIO

S3-compatible object store (like AWS S3).

Spark + Iceberg can store tables on MinIO.

Comet can read/write Parquet/Arrow files from MinIO just like any S3 endpoint.

```
           +-----------------+
           |     Kyuubi      |  <-- SQL endpoint for users
           +-----------------+
                   |
                   v
          +-----------------+
          |     Spark +     |
          |     Comet       |
          +-----------------+
           |       |       |
           |       |       |
           v       v       v
       +-------+  +-------+  +-------+
       | Iceberg|  | Doris |  | MinIO |
       +-------+  +-------+  +-------+
          ^
          |
        Nessie

```

Spark + Comet = engine + acceleration

Kyuubi = SQL multi-tenant access

Iceberg + Nessie = table storage and versioned catalog

Doris = analytic OLAP DB

MinIO = object storage

from cassandra.cqlengine.models import Model
from cassandra.cluster import Cluster, SimpleStatement, BatchStatement


casandra_db_addr = [('internal-aa192f871e59a4ac7ad1d7d479922bb2-304939937.us-east-1.elb.amazonaws.com','9042')]
cluster = Cluster(casandra_db_addr)
session = cluster.connect()
rows=session.execute("SELECT * FROM batch_translation.flask_data")

for user_row in rows:
    print (user_row)

class Base(Model):
    __abstract__ = True
    __keyspace__ = "batch_translation"
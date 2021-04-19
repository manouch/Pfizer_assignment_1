from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from models.user import Files

connection.setup(['internal-aa192f871e59a4ac7ad1d7d479922bb2-304939937.us-east-1.elb.amazonaws.com'], "cqlengine", protocol_version=3)

sync_table(Files)
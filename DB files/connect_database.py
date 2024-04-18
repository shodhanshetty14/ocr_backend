import json

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster


class DB:
    def __init__(self):
        self.session = ''
    def connect(self):
        # This secure connect bundle is autogenerated when you download your SCB,
        # if yours is different update the file name below
        cloud_config= {
          'secure_connect_bundle': 'secure-connect-testdb.zip'
        }
        astra_json_api_url = " on"

        # This token JSON file is autogenerated when you download your token,
        # if yours is different update the file name below
        with open("db-token.json") as f:
            secrets = json.load(f)

        CLIENT_ID = secrets["clientId"]
        CLIENT_SECRET = secrets["secret"]

        auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.session = cluster.connect()

        self.session.execute("CREATE KEYSPACE IF NOT EXISTS OCR WITH replication = {'class':'SimpleStrategy', 'replication_factor':3}")
        self.session.set_keyspace('OCR')

        row = self.session.execute("select release_version from system.local").one()
        if row:
          print(row[0])
        else:
          print("An error occurred.")
    def store(self,data):
        self.session.execute

    # rows = session.execute("select * from aliens")
    # for row in rows:
    #   print(row)
    # else:
    #   print("An error occurred.")
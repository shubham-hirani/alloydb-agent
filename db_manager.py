import os
import sqlalchemy
from google.cloud.alloydb.connector import Connector
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def get_connection():
    # Initialize the Connector
    connector = Connector()

    def getconn():
        conn = connector.connect(
            "projects/YOUR_PROJECT/locations/YOUR_REGION/clusters/YOUR_CLUSTER/instances/YOUR_INSTANCE",
            "pg8000",
            user="YOUR_SERVICE_ACCOUNT_EMAIL", # No password needed with IAM
            db="postgres",
            enable_iam_auth=True,
        )
        return conn

    pool = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return pool
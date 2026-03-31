import os
import sqlalchemy
from sqlalchemy import create_engine
from google.cloud.alloydb.connector import Connector

# Initialize the Connector as a global object to reuse across connections
connector = Connector()


def get_connection():
    """
    Creates a SQLAlchemy engine using IAM authentication and environment variables.
    No password is required as the Cloud Run Service Account handles identity.
    """

    def getconn():
        # Retrieve variables from environment
        instance_uri = os.getenv("ALLOYDB_INSTANCE_URI")
        db_user = os.getenv("DB_USER")
        db_name = os.getenv("DB_NAME", "postgres")  # Default to postgres if not set

        # Validation to prevent silent failures
        if not instance_uri or not db_user:
            raise ValueError("Missing ALLOYDB_INSTANCE_URI or DB_USER environment variables.")

        conn = connector.connect(
            instance_uri=instance_uri,
            driver="pg8000",
            user=db_user,
            db=db_name,
            enable_iam_auth=True,
        )
        return conn

    # Create the engine using the pg8000 dialect
    # pool_size and overflow can be adjusted based on Cloud Run scaling
    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )

    return engine
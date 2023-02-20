import os
import asyncpg
from google.cloud.sql.connector import create_async_connector, IPTypes
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

cloud_sql_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
cloud_sql_db = os.environ.get('CLOUD_SQL_DB')
cloud_sql_user = os.environ.get('CLOUD_SQL_USER')
cloud_sql_host = os.environ.get('CLOUD_SQL_HOST')
cloud_sql_password = os.environ.get('CLOUD_SQL_PASSWORD')

async def getconn():
    # intialize Connector object using 'create_async_connector'
    connector = await create_async_connector()
    conn: asyncpg.Connection = await connector.connect_async(
            cloud_sql_connection_name,
            "asyncpg",
            user=cloud_sql_user,
            db=cloud_sql_db,
            enable_iam_auth=True,
            ip_type=IPTypes.PRIVATE
        )
    return conn

connection_string = f"postgresql+asyncpg://{cloud_sql_user}:{cloud_sql_password}@{cloud_sql_host}/{cloud_sql_db}"

engine = create_async_engine(connection_string, future=True, echo=True)

session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


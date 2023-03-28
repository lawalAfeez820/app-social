
from sqlalchemy.ext.asyncio import create_async_engine
from tests.test_config.config import setting


db_connection_str = setting.database_test_name


async_engine = create_async_engine(
   db_connection_str,
   echo=True,
   future=True
)
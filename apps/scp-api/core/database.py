from .configuration import settings
from sqlalchemy import create_engine, orm, Engine
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

__engine__: Engine = create_engine(url=settings.database.uri)
Session = orm.sessionmaker(__engine__)

async def engine() -> Engine:
    return __engine__

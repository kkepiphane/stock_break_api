import time
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.database import engine
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_postgres():
    """Attendre que PostgreSQL soit disponible"""
    max_retries = 10
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✅ Connected to PostgreSQL successfully!")
            return True
        except OperationalError as e:
            logger.warning(f"⚠️ PostgreSQL not ready yet (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    
    logger.error("❌ Could not connect to PostgreSQL after multiple attempts")
    return False

def init_db():
    """Créer les tables si elles n'existent pas"""
    try:
        from app.models.base import Base
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
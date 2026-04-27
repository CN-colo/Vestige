from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    # Import all models to ensure they are registered
    from .models.user import User
    from .models.article import Article
    from .models.project import Project
    from .models.api_key import ApiKey
    from .models.media import Media
    from .models.comment import Comment
    from .models.favorite import Favorite
    from .models.follow import Follow
    from .models.tag_subscription import TagSubscription
    from .models.like import Like
    
    Base.metadata.create_all(bind=engine)
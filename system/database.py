from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session, declarative_base
from typing import Callable, Optional

SessionFactory = Callable[[], Session]
SessionLocal: Optional[SessionFactory] = None
Base = declarative_base()


def init_engine(database_url: str, echo: bool = False):
    global SessionLocal
    engine = create_engine(database_url, echo=echo)
    SessionLocal = scoped_session(sessionmaker(bind=engine))
    return engine


class DatabaseSession:
    def __init__(self):
        if SessionLocal is None:
            raise RuntimeError("Database engine not initialized. Call init_engine() before using DatabaseSession.")
        # Create a session from the scoped_session factory
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.db.rollback()
                return False  # do not suppress exceptions
            else:
                self.db.commit()
        except Exception as ex:
            self.db.rollback()
            raise ex
        finally:
            # With scoped_session, remove() is the correct way to dispose of the current Session
            try:
                SessionLocal.remove()  # type: ignore[arg-type]
            except Exception:
                # Fallback to close if remove is not available for any reason
                try:
                    self.db.close()
                except Exception:
                    pass

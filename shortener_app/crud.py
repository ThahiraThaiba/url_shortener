# this file will contain functions that perform actions
# to Create, Read, Update, and Delete (CRUD) items in your database

from sqlalchemy.orm import Session

from . import keygen, models, schemas


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """to get a unique string for your shortened URL’s key"""
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


# inorder to avoid generating same key

def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """tells you if a key already exists in your database"""
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """Your get_db_url_by_secret_key() function checks your database for an active database entry
     with the provided secret_key. If a database entry is found, then you return the entry.
     Otherwise, you return None."""
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """One data point of the response body is how often your shortened URL was clicked.
    in order to count the no of clicks"""
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """deactivated URLs won’t get returned in your database calls.
     it’ll look like the URL was deleted, but only you as a super admin
     can actually complete the deletion action"""
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url

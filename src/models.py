"""
Postgresql database models.
"""
from peewee import Model, PostgresqlDatabase, CharField, DateTimeField
import datetime

from os import environ

db = PostgresqlDatabase(host=environ.get('PG_HOST'),
                        database=environ.get('PG_DBNAME'),
                        user=environ.get('PG_USER'),
                        password=environ.get('PG_PASS'),
                        autorollback=True)

# NOTE: peewee unfortunately does not support automatic schema migrations, so we have to handle this manually if we change a model.
# Fortunately the data we're storing is pretty simple, so this shouldn't happen a lot.
# If this does become an issue there are modules to handle this automatically, but I haven't been able to find one that is actively developed.


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db


class WebID(BaseModel):
    """
    The model for linking the web ID uri to the lblod ID uri.

    "uri"           -- The web ID uri of the entry.
    "lblod_id"      -- The lblod ID uri of the entry.
    ""date_created" -- The date on which the entyr was created.
    """
    uri = CharField(unique=True)
    lblod_id = CharField(unique=True)
    date_created = DateTimeField(default=datetime.datetime.now)

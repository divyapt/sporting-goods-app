from sqlalchemy import create_engine
from catalog_database_setup import Base, Catalog, CatalogItem, User
import contextlib
from sqlalchemy import MetaData

engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine
meta = Base.metadata
print "********* Entering with ********* {}".format(Base.metadata.sorted_tables)
with contextlib.closing(engine.connect()) as con:
    trans = con.begin()
    print "********* Entering trans ********* {}".format(meta.sorted_tables)
    for table in reversed(meta.sorted_tables):
        print "TABLE****** {} *****TABLE".format(table)
        con.execute(table.delete())
    trans.commit()

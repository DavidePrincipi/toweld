
import os
from nethserver.toweld.esdb.EsdbInstance import EsdbInstance

db_path_prefix = '/var/lib/nethserver/db/'

for dbfile in os.listdir(db_path_prefix):
    toweld.register_plugin(EsdbInstance(dbus_conn, dbus_path + '/' + dbfile, db_path_prefix + dbfile))



from nethserver.toweld.esdb.EsdbPlugin import EsdbPlugin
import os

p = EsdbPlugin(conn, path_prefix + 'Esdb')

for dbfile in os.listdir(p.db_path_prefix):
    p.Open(dbfile)

plugins.append(p)

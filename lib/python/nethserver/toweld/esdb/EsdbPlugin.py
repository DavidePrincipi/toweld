#
# Copyright (C) 2017 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#

import dbus.service
from nethserver.toweld import ToweldPlugin
from nethserver.toweld.esdb.EsdbInstance import EsdbInstance

class EsdbPlugin(dbus.service.Object, ToweldPlugin):

    db_path_prefix = '/var/lib/nethserver/db/'

    def __init__(self, conn, object_path):
        self.db = {}
        super(EsdbPlugin, self).__init__(conn = conn, object_path = object_path)
    
    def unload_plugin(self):
        for db in self.db.keys():
            self.close(db)

    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='s', out_signature='')
    def Open(self, database):
        parts = database.split('/')
        if parts[0] == '':
            database_name = parts[-1]
            database_path = '/'.join(parts[:-1])
        else:
            database_name = parts[0] 
            database_path = self.db_path_prefix + database_name
        self.db[database] = EsdbInstance(database_path, self.connection, self.__dbus_object_path__ + '/' + database_name)
    
    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='s', out_signature='')
    def Close(self, database):
        self.db[database].remove_from_connection()
        del self.db[database]

    @dbus.service.method('org.nethserver.toweld1.Esdb', out_signature='as')
    def List(self):
        return self.db.keys()

    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='', out_signature='')
    def Commit(self):
        for db in self.db:
            # persist database changes to disk
            pass
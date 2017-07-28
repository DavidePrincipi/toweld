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

import dbus
import dbus.service
from nethserver.toweld.esdb.EsdbStorage import EsdbFileStorage

class EsdbInstance(dbus.service.Object, EsdbFileStorage):
    def __init__(self, filepath, conn, object_path):
        self.name = object_path.split('/')[-1]
        self.filepath = filepath
        self.changes = 0
        self.SUPPORTS_MULTIPLE_OBJECT_PATHS = True
        self.SUPPORTS_MULTIPLE_CONNECTIONS = False
        super(EsdbInstance, self).__init__(conn = conn, object_path = object_path)
        self.data = self.load(filepath)
        self.dbus_props = {'databaseName': dbus.String(self.name, variant_level=1), 'fileSystemPath': dbus.String(self.filepath, variant_level=1)}

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ss', out_signature='v')
    def Get(self, iname, pname):
        return self.dbus_props[pname]

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv', out_signature='')
    def Set(self, iname, pname, value):
        self.dbus_props[pname] = dbus.String(value)

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s', out_signature='a{sv}')
    def GetAll(self, iname):
        if iname == 'org.nethserver.toweld1.Esdb':
            return dbus.Dictionary(self.dbus_props, "sv", variant_level=1)
        else:
            return dbus.Dictionary({}, "sv", variant_level=1)

    @dbus.service.signal(dbus.PROPERTIES_IFACE, signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties, invalidated_properties):
        pass

    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='s', out_signature='s')
    def GetValue(self, key):
        if not key in self.data:
            return False

        return self.data[key]['type']

    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='s', out_signature='v')
    def GetRaw(self, key):
        if not key in self.data:
            return False

        record = self.data[key]
        value = record['type']
        if 'props' in record:
            for p, v in record['props'].iteritems():
                value += '|' + p + '|' + v 
        return value


    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='', out_signature='as')
    def Keys(self):
        return self.data.keys()
    
    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='ss', out_signature='s')
    def GetProp(self, key, prop):
        try:
            return self.data[key]['props'][prop]
        except:
            return ""

    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='ssa{ss}', out_signature='')
    def SetRecord(self, key, type, props={}):
        self.data[key] = {'type': type, 'props': props}
        self.changes += 1

    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='ss', out_signature='')
    def SetType(self, key, type):
        try:
            self.data[key]['type'] = type
            self.changes += 1
        except:
            pass

    @dbus.service.method('org.nethserver.toweld1.Esdb', in_signature='sa{ss}', out_signature='')
    def SetProp(self, key, props={}):
        try:
            self.data[key]['props'].update(props)
            self.changes += 1
        except:
            pass

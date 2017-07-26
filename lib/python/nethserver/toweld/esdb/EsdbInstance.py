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
from EsdbStorage import EsdbFileStorage
from nethserver.toweld import ServiceObject, ToweldPlugin
import json
import logging

TYPE = 0
PROPS = 1

class EsdbInstance(ServiceObject, EsdbFileStorage, ToweldPlugin):
    """Instances of this class represent a NethServer database"""

    def __init__(self, conn, object_path, filepath):
        self.name = object_path.split('/')[-1]
        self.filepath = filepath
        self.changes = 0
        super(EsdbInstance, self).__init__(conn = conn, object_path = object_path)
        self.data = self.parse_db(filepath)


    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='', out_signature='s')
    def DbAsJson(self):
        json.dumps(self.data)

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='', out_signature='as')
    def DbKeys(self):
        return self.data.keys()

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='s', out_signature='s')
    def DbGet(self, key):
        return self.DbGetType(key)

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='s', out_signature='s')
    def DbGetType(self, key):
        if not key in self.data:
            return ""
        return self.data[key][TYPE]

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='ss', out_signature='s')
    def DbGetProp(self, key, prop):
        try:
            return self.data[key][PROPS][prop]
        except:
            return ""

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='ssa{ss}', out_signature='')
    def DbSet(self, key, type, props={}):
        try:
            self.data[key] = (type, props)
            self.changes += 1
        except:
            pass

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='s', out_signature='')
    def DbDelete(self, key):
        try:
            del self.data[key]
            self.changes += 1
        except:
            pass

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='ss', out_signature='')
    def DbSetType(self, key, type):
        try:
            self.data[key][TYPE] = type
            self.changes += 1
        except:
            pass

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='sss', out_signature='')
    def DbSetProp(self, key, prop, value):
        try:
            self.data[key][PROPS][prop] = value
            self.changes += 1
        except:
            pass

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='ss', out_signature='')
    def DbDelProp(self, key, prop):
        try:
            del self.data[key][PROPS][prop]
            self.changes += 1
        except:
            pass

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='sa{ss}', out_signature='')
    def DbSetProps(self, key, props={}):
        try:
            self.data[key][PROPS].update(props)
            self.changes += 1
        except:
            pass

    @dbus.service.method('org.nethserver.Toweld1.Esdb', in_signature='', out_signature='')
    def DbSave(self):
        self.save()

    @dbus.service.method('org.nethserver.Toweld1.EsdbLegacy', in_signature='', out_signature='s')
    def DbAsLegacyFormat(self):
        out = {}
        for key in self.data:
            out[key] = self.DbGetLegacy(key)
        return json.dumps(out)


    @dbus.service.method('org.nethserver.Toweld1.EsdbLegacy', in_signature='s', out_signature='s')
    def DbGetLegacy(self, key):
        if not key in self.data:
            return ""

        record = self.data[key]
        value = record[TYPE]

        for p, v in record[PROPS].iteritems():
            value += '|' + p + '|' + v

        return value

    @dbus.service.method('org.nethserver.Toweld1.EsdbLegacy', in_signature='ss', out_signature='')
    def DbSetLegacy(self, key, value):
        logging.debug('%s: OLD %s=%s' % (self.name, key, self.DbGetLegacy(key)))
        logging.debug('%s: NEW %s=%s' % (self.name, key, value))
        self.data[key] = self.parse_value(value)
        self.changes += 1

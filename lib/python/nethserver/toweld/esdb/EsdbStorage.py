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

import os

# states:
# O initial state
# E error
# C comment
# K key
# T type
# P prop
# V value
# ?e escape sequence

class EsdbFileStorage:

    dfa1 = {
        ('O', '#'): 'C',
        ('O', 0): 'K',

        ('C', 0): 'C',
        ('C', '\n'): 'O',

        ('E', 0): 'E',

        ('K', 0): 'K',
        ('K', '\\'): 'Ke',
        ('Ke', 0): 'K',
        ('K', '='): 'T',
        ('K', '\n'): 'E',

        ('T', 0): 'T',
        ('T', '\\'): 'Te',
        ('Te', 0): 'T',
        ('T', '|'): 'P',
        ('T', '\n'): 'O',

        ('P', 0): 'P',
        ('P', '\\'): 'Pe',
        ('Pe', 0): 'P',
        ('P', '|'): 'V',
        ('P', '\n'): 'E',

        ('V', 0): 'V',
        ('V', '\\'): 'Ve',
        ('Ve', 0): 'V',
        ('V', '|'): 'P',
        ('V', '\n'): 'O',
    }

    def parse_value(self, value):
        if not value.endswith("\n"):
            value += "\n"
        tokens = self.parse_record(value, 'T')
        if len(tokens) < 1:
            raise EsdbStorageLoadError('Cannot parse value "%s"' % value)
        elif len(tokens) == 1:
            return (tokens[0], {})
        elif len(tokens) > 1:
            return (tokens[0], dict(zip(tokens[1::2], tokens[2::2])))

    def parse_record(self, line, sc, nbrow=0):
        dfa = self.dfa1
        tok = ''
        tokens = []
        nbcol = 0
        escape = lambda c: '\n' if c == 'n' else c

        for c in line:
            nbcol += 1

            # state-next
            if (sc, c) in dfa:
                # state transition is defined explicitly
                sn = dfa[(sc, c)]
            else:
                # apply default state transition
                sn = dfa[(sc, 0)]

            if sc == sn or sc == 'O':
                tok += c
            elif sc.endswith('e') and sc[0] == sn[0]:
                tok += escape(c)
            else:
                tokens.append(tok)
                tok = ''

            sc = sn

        if sc != 'O':
            raise EsdbStorageLoadError('In file %s: error at line %d, column %d, near "%s"' % (filepath, nbrow, nbcol, tok))

        return tokens

    def parse_db(self, filepath):
        db = {}
        with open(filepath) as f:
            nbrow = 0
            for line in f:
                nbrow += 1
                tokens = self.parse_record(line, 'O', nbrow)
                if len(tokens) < 2:
                    pass
                elif len(tokens) == 2:
                    db[tokens[0]] = (tokens[1], {})
                elif len(tokens) > 2:
                    db[tokens[0]] = (tokens[1], dict(zip(tokens[2::2], tokens[3::2])))
        return db

    def save(filepath, data):
        pass

class EsdbStorageLoadError(Exception):
    pass

if __name__ == '__main__':
    import json, sys
    d = EsdbFileStorage().load('/dev/stdin')
    json.dump(d, sys.stdout)
    
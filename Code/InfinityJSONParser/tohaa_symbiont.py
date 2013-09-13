__author__ = 'u0064666'

import json
SymbiontArmors = {}


def parseTohaa(rootDirectory):
    f = open(rootDirectory + 'Code\\InfinityJSONParser\Data\\tohaa.json', "r")
    units = json.load(f)['Tohaa']

    for unit in units:
        if 'altp' in unit and 'spec' in unit and 'Symbiont Armour' in unit['spec']:
            name = unit.get('name', '')
            if name != '':
                profile = unit.get('altp', [{}])[0]
                global SymbiontArmors
                if SymbiontArmors.get(name, None) is None:
                    SymbiontArmors[name] = profile
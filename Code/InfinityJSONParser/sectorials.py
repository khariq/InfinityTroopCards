__author__ = 'u0064666'

import json


##
# Sectorial['Metros'] = [icon, ava, linkable]
Sectorials = {}


def parseSectorials(rootDirectory):
    f = open(rootDirectory + 'Code\InfinityJSONParser\Data\Other\\sectorials.json', 'r')
    d = json.load(f)

    for sectorial in d:
        name = sectorial.get('name', '').replace(' ', '_')

        img = rootDirectory + 'ImagesFromCB\Sectorials\\' + name + '_logo.png'
        for unit in sectorial.get('units', []):
            linkable = unit.get('linkable', False)
            ava = unit.get('ava', '0')
            Sectorials[unit['isc']] = [img, linkable, ava]

    return

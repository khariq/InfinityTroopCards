import os
import decoder
__author__ = 'u0064666'

import json

rootOutputPath = "C:\Users\u0064666\Pictures\Cards\Data\\"
pathToIcons = "C:\\Users\\u0064666\\Pictures\\Cards\\ImagesFromCB\\"
pathToRegularIcon = "C:\\Users\\u0064666\\Pictures\\Cards\\ImagesFromCB\\Regular.png"
pathToIrregularIcon = "C:\\Users\\u0064666\\Pictures\\Cards\\ImagesFromCB\\Irregular.png"
pathToImpetuousIcon = "C:\\Users\\u0064666\\Pictures\\Cards\\ImagesFromCB\\Impetuous.png"
iconDirectoryMap = {
    "Panoceania": "PanO",
    "Yu Jing": "YuJing",
    "Ariadna": "Ariadna",
    "Haqqislam": "Haqqis",
    "Combined Army": "CA",
    "Nomads": "Nomads",
    "Tohaa": "Tohaa",
    "Mercs": "Mercs",
    "Aleph": "Aleph"
}

rules = {}

weaponData = {}
blankWeaponString = '\t'
weaponHeader = 'W1SValue\tW1MValue\tW1LValue\tW1MaxValue\tW1DmgValue\tW1BValue\tW1AmmoValue\tW1SpecialValue'
header= 'UnitNameValue\tUnitIcon\tUnitPortrait\tTrainingIcon\tImpIcon\tMOVValue\tCCValue\tBSValue\tPHValue\tWIPValue\tARMValue\tBTSValue\tWValue\tAVAValue\tSWCCost\tUnitCost\tUnitNotesValue\tAbility1Title\tAbility1Text\tAbility2Title\tAbility2Text\tWeapon1Value\tWeapon2Value\tWeapon3Value\tWeapon4Value\tWeapon5Value'
currentISC = 'null'
fout = None


def getUnitIcons(dict):
    unitIcon = ''
    unitPortrait = ''

    if dict.get('cbcode', None) is not None:
        directory = dict['army']
        directory = iconDirectoryMap.get(directory, '')
        if directory != '':
            directory = pathToIcons + directory
            for item in dict['cbcode']:
                if item + '.png' in os.listdir(directory):
                    unitPortrait = directory + '\\' + item + '.png'
                    unitIcon = directory + '\\' +item + '-Icon.png'
        else:
            unitIcon = 'NotFound'

    return unitIcon, unitPortrait


def writeImagePaths(dict):
    unitIcon, unitPortrait = getUnitIcons(dict)
    line = ''
    line += unitIcon + '\t'
    line += unitPortrait + '\t'
    if dict.get('irr', '') == 'X':
        line += pathToIrregularIcon + "\t"
    else:
        line += pathToRegularIcon + "\t"

    if dict.get('imp', '') == 'X':
        line += pathToImpetuousIcon + "\t"
    else:
        line += "\t"

    return line


def writeStatLine(dict):
    line = ''
    line += dict['mov'] + '\t'
    line += dict['cc'] + '\t'
    line += dict['bs'] + '\t'
    line += dict['ph'] + '\t'
    line += dict['wip'] + '\t'
    line += dict['arm'] + '\t'
    line += dict['bts'] + '\t'
    line += dict['w'] + '\t'
    line += dict['ava'] + '\t'

    return line


def writeAbilities(dict, loadout):
    count = 0
    abilities = ""
    line = ''
    for spec in loadout['spec']:
        count += 1
        abilities = abilities + spec + ", "

    for spec in dict['spec']:
        count += 1
        abilities = abilities + spec + ", "

    # trim the trailing [, ] off
    if count > 0:
        printLine = line + abilities[:-2] + '\t'
    else:
        printLine = line + '\t'

    ability1 = ''
    ability2 = ''
    ability1_frequency = 99999
    ability2_frequency = 99999
    count = 0
    for ability in abilities.split(','):
        if ability.strip() in rules:
            freq = 99999
            for a in decoder.rules_frequency:
                if a[0] == ability.strip():
                    freq = a[1]
                    break

            if freq < ability1_frequency:
                ability1 = ability
                ability1_frequency = freq
            elif freq < ability2_frequency:
                ability2 = ability
                ability2_frequency = freq

    if len(ability1) > 0:
        printLine += ability1 + '\t' + rules.get(ability1.strip(), '') + '\t'
    else:
        printLine += '\t\t'
    if len(ability2) > 0:
        printLine += ability2 + '\t' + rules.get(ability2.strip(), '') + '\t'
    else:
        printLine += '\t\t'

    return printLine


def writeWeapons(dict, loadout):
    line = ''
    count = 0
    for weapon in dict['bsw']:
        count += 1
        if count > 5:
            break
        line += weapon + '\t'

    for weapon in loadout['bsw']:
        count += 1
        if count > 5:
            break
        line += weapon + '\t'

    for weapon in dict['ccw']:
        count += 1
        if count > 5:
            break
        line += weapon + '\t'

    for weapon in loadout['ccw']:
        count += 1
        if count > 5:
            break
        line += weapon + '\t'

    while count < 5:
        line += blankWeaponString
        count += 1

    return line


def writeName(dict, loadout):
    name = ""
    if loadout['code'] == 'Default':
        name = dict['isc']
    else:
        name = dict['isc'] + ' - ' + loadout['code']

    return name.replace('/', '-').replace('"', '') + '\t'


def unit(dict):
    if 'name' in dict and 'cbcode' in dict and 'army' in dict:
        line = ""
        global fout

        if 'childs' in dict:
            types = dict['childs']

            line += writeImagePaths(dict)

            line += writeStatLine(dict)

            for t in types:
                printLine = line

                # Write Costs
                printLine += t['swc'] + '\t'
                printLine += t['cost'] + '\t'

                # insert the name to the front of the line
                printLine = writeName(dict, t) + printLine
        
                printLine += writeAbilities(dict, t)

                printLine += writeWeapons(dict, t)

                printLine += "\r\n"

                print printLine
                fout.write(unicode(printLine))

    if 'code' in dict:
        return dict

def weapon(dict):
    line = ""
    #Weapon5Value W5SValue W5MValue W5LValue W5MaxValue W5DmgValue W5BValue W5AmmoValue W5SpecialValue
    line = dict['name'] + '\t'
    line +=  dict['short_dist'] + '/' + dict['short_mod'] + '\t'
    line += dict['medium_dist'] + '/' + dict['medium_mod'] + '\t'
    line += dict['long_dist'] + '/' + dict['long_mod'] + '\t'
    line += dict['max_dist'] + '/' + dict['max_mod'] + '\t'
    line += dict['damage'] + '\t'
    line += dict['burst'] + '\t'
    line += dict['ammo'] + '\t'
    notes = ""
    if dict['cc'] == 'Yes':
        notes = notes + 'CC '
    if dict['template'] != 'No':
        notes = notes + dict['template'] + ' '
    if dict['em_vul'] == 'Yes':
        notes = notes + 'EM '

    notes = notes + dict.get('note', '')
    line += notes + '\t'

    weaponData[dict['name']] = line
    weaponData[dict['name'] + ' (2)'] = line

def rulesAndEquipment(dict):

    if dict.get('data', '') != '':
        rules[dict.get('name', '')] = dict.get('data', '')


def runFile(name, army):
    global fout
    fout = open(rootOutputPath + army + ".dat", "w")
    fout.write(header + "\r\n")
    f = open("C:\\Python Projects\\InfinityJSONParser\\Data\\" + name, "r")
    data = json.load(f, object_hook=unit)

f = open("C:\\Python Projects\\InfinityJSONParser\\Data\\Other\\weapons.json", "r")
json.load(f, object_hook=weapon)

f = open("C:\\Python Projects\\InfinityJSONParser\\Data\\Other\\rules.json", "r")
json.load(f, object_hook=rulesAndEquipment)

decoder.count_rules_frequency()

runFile("aleph.json", "aleph")
runFile("ariadna.json", "ariadna")
runFile("combined.json", "ca")
runFile("haqq.json", "haqq")
runFile("merc.json", "merc")
runFile("nomads.json", "nomads")
runFile("other.json", "other")
runFile("pano.json", "pano")
runFile("tohaa.json", "tohaa")
runFile("yujing.json", "yujing")



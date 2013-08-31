import os

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

def unit(dict):
    if 'name' in dict and 'cbcode' in dict and 'army' in dict:
        line = ""
        # global currentISC
        global fout
        #
        # if dict['isc'] != currentISC:
        #     # close the current file stream
        #     if fout != None:
        #         fout.close()
        #     # open a file stream for the new ISC
        #     if not os.path.exists(rootOutputPath + dict.get('army', '')):
        #         os.makedirs(rootOutputPath + dict.get('army', ''))
        #     fout = open(rootOutputPath + dict.get('army', '') + '\\' + dict['isc'].replace('"', '').replace('/', '-') + '.dat', 'w')
        #     fout.write(header + "\r\n")
        #     currentISC = dict['isc']

        unitIcon = ''
        unitPortrait = ''
        if dict.get('cbcode', None) != None:
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

        if 'childs' in dict:
            types = dict['childs']

            #line = '"' + dict['type'] + '" '
            line = line +  unitIcon + '\t'
            line = line +  unitPortrait + '\t'
            if dict.get('irr', '') == 'X':
                line = line + pathToIrregularIcon + "\t"
            else:
                line = line + pathToRegularIcon + "\t"

            if dict.get('imp', '') == 'X':
                line = line + pathToImpetuousIcon + "\t"
            else:
                line = line + "\t"

            line = line +  dict['mov'] + '\t'
            line = line +  dict['cc'] + '\t'
            line = line +  dict['bs'] + '\t'
            line = line + dict['ph'] + '\t'
            line = line + dict['wip'] + '\t'
            line = line + dict['arm'] + '\t'
            line = line + dict['bts'] + '\t'
            line = line + dict['w'] + '\t'
            line = line + dict['ava'] + '\t'

            for t in types:
                printLine = line

                printLine = printLine + t['swc'] + '\t'
                printLine = printLine + t['cost'] + '\t'
                
                name = ""
                if t['code'] == 'Default':
                    name = dict['isc']
                else:
                    name = dict['isc'] + ' - ' + t['code']

                printLine = name.replace('/', '-').replace('"', '') + '\t' + printLine
        
                count = 0
                abilities = ""
                for spec in t['spec']:
                    count = count + 1
                    abilities = abilities + spec + ", "

                for spec in dict['spec']:
                    count = count + 1
                    abilities = abilities + spec + ", "


                # trim the trailing [, ] off
                if (count > 0):
                    printLine = printLine + abilities[:-2] + '\t'
                else:
                    printLine = printLine + '\t'

                count = 0
                for ability in abilities.split(','):
                    if ability.strip() == 'V: Dogged':
                        stopHere = True
                    if ability.strip() in rules:
                        printLine = printLine + ability +'\t' + rules.get(ability.strip(), '') + '\t'
                        count = count + 1
                    if count == 2:
                        break
                while count < 2:
                    printLine = printLine + "\t\t"
                    count = count + 1

                count = 0
                for weapon in dict['bsw']:
                    count = count + 1
                    if count > 5:
                        break
                    txt = ""
                    printLine = printLine + weapon + '\t'# weaponData.get(weapon, blankWeaponString)

                for weapon in t['bsw']:
                    count = count + 1
                    if count > 5:
                        break
                    printLine = printLine + weapon + '\t'#weaponData.get(weapon, blankWeaponString)

                for weapon in dict['ccw']:
                    count = count + 1
                    if count > 5:
                        break
                    printLine = printLine + weapon + '\t'#weaponData.get(weapon, blankWeaponString)

                for weapon in t['ccw']:
                    count = count + 1
                    if count > 5:
                        break
                    printLine = printLine + weapon + '\t'#weaponData.get(weapon, blankWeaponString)

                while count < 5:
                    printLine = printLine + blankWeaponString
                    count = count + 1

                printLine =  printLine + "\r\n"
                print printLine
                fout.write(unicode(printLine))

    if 'code' in dict:
        return dict

def weapon(dict):
    line = ""
    #Weapon5Value W5SValue W5MValue W5LValue W5MaxValue W5DmgValue W5BValue W5AmmoValue W5SpecialValue
    line = dict['name'] + '\t'
    line = line +  dict['short_dist'] + '/' + dict['short_mod'] + '\t'
    line = line + dict['medium_dist'] + '/' + dict['medium_mod'] + '\t'
    line = line + dict['long_dist'] + '/' + dict['long_mod'] + '\t'
    line = line + dict['max_dist'] + '/' + dict['max_mod'] + '\t'
    line = line + dict['damage'] + '\t'
    line = line + dict['burst'] + '\t'
    line = line + dict['ammo'] + '\t'
    notes = ""
    if dict['cc'] == 'Yes':
        notes = notes + 'CC '
    if dict['template'] != 'No':
        notes = notes + dict['template'] + ' '
    if dict['em_vul'] == 'Yes':
        notes = notes + 'EM '

    notes = notes + dict.get('note', '')
    line = line + notes + '\t'

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



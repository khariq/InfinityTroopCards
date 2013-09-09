import json

rules_frequency = []
rule_dict = {}

def count_rules_frequency():
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

    for rule in rule_dict:
        rules_frequency.append((rule, rule_dict[rule]))

    rules_frequency.sort(key=lambda x: x[1])


def runFile(name, key):
    f = open("C:\\Python Projects\\InfinityJSONParser\\Data\\" + name, "r")
    json.load(f, object_hook=rules_parse)


def rules_parse(dict):
    global rule_dict

    if 'spec' in dict:
        for rule in dict['spec']:
            if rule in rule_dict:
                rule_dict[rule] += 1
            else:
                rule_dict[rule] = 1
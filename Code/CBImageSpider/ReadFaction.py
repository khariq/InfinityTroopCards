import urllib2
from urllib import urlretrieve
import os

def ReadFaction(outFolder, href):
    catalog = urllib2.urlopen(href).read()
    i = catalog.find('<div id="catalogo" >')
    j = catalog.find('</div><!-- #catalogo -->', i)
    catalog = catalog[i:j]

    end = 0
    i = catalog.find('<a')
    while i != -1:
        j = catalog.find('</a>', i)
        end = j
        unit = catalog[i:j]

        i = unit.find('href="') + 6
        j = unit.find('">', i)
        href = unit[i:j]

        i = unit.find('background:url(')+15
        j = unit.find(')', i)
        imgUrl = unit[i:j]

        i = imgUrl.rfind('/') +1
        j = imgUrl.rfind('-', i)
        name = imgUrl[i:j]

        print name
        print imgUrl

        fileName = outFolder + '\\' + name + imgUrl[imgUrl.rfind('.'):]
        urlretrieve(imgUrl, fileName)

        troopProfile = urllib2.urlopen(href).read()
        i = troopProfile.find('iconoTropa')
        i = troopProfile.find('url(', i) + 4
        j = troopProfile.find(')', i)
        imgUrl = troopProfile[i:j]

        print imgUrl
        fileName = outFolder + '\\' + name + '-Icon' + imgUrl[imgUrl.rfind('.'):]
        urlretrieve(imgUrl, fileName)

        i = catalog.find('<a', end)

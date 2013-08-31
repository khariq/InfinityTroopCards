import urllib2
from urllib import urlretrieve
import os

from ReadFaction import ReadFaction
outputFolder = 'C:\\Users\\u0064666\\Pictures\\Cards\\ImagesFromCB\\'
rootPage = urllib2.urlopen( "http://www.infinitythegame.com/infinity/en/facciones/").read()

##
# find '<ul id="facciones">', read to </ul>
index = rootPage.find('<ul id="facciones">')
end = rootPage.find('</ul>', index)

factionList = rootPage[index:end]

# for each <li in the page
i = 0
index = factionList.find('<li')
while index != -1:

    end = factionList.find('</li>', index)
    faction = factionList[index:end]
    index = factionList.find('<li', end)
    if 'holo' in faction:
        continue

    i = faction.find('href=')+6
    j = faction.find('">', i)
    href = faction[i:j]

    i = faction.find('<li id="icon') + 12
    j = faction.find('"', i)
    name = faction[i:j]

    #print name + ": " + href

    i = faction.find('<img src="')+10
    j = faction.find('"/>', i)
    imgUrl = faction[i:j]

    print imgUrl
    outFolder = outputFolder + name
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)

    fileName = outFolder + '\\' + imgUrl[imgUrl.rfind('/')+1:]
    urlretrieve(imgUrl, fileName)

    ReadFaction(outFolder, href)
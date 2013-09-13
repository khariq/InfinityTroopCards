#!/usr/bin/env python
from gimpfu import *
import json
import os
errOut = None
logOut = None


class Page:

    width = 3.66
    height = 2.196
    frontPage = None
    backPage = None
    position = 0
    pageNumber = 0
    resolution = (500, 500)
    frontFileName = ''
    backFileName = ''
    def __init__(self, pageNumber, outDirectory):

        logProcessing(str(pageNumber), 'Creating pages')
        self.position = 1
        self.frontPage = gimp.Image(5500, 4250, RGB)
        pdb.gimp_image_set_resolution(self.frontPage, 500, 500)

        self.backPage =  gimp.Image(5500, 4250, RGB)
        pdb.gimp_image_set_resolution(self.backPage, 500, 500)

        self.pageNumber = pageNumber
        self.frontFileName = os.path.join(outDirectory, 'Page' + str(self.pageNumber) + '.png')
        self.backFileName = os.path.join(outDirectory, 'Page' + str(self.pageNumber+1) + '.png')
        logProcessing(str(self.pageNumber), 'Pages started')


        return

    def addCard(self, pathToCard):
        logProcessing(pathToCard, 'Adding Card ' + str(self.position))
        column = 0
        row = 0
        if self.position in (1,2,3):
            row = 0
        elif self.position in (4, 5, 6):
            row = 1
        else:
            row = 2

        if self.position in (1, 4, 7):
            column = 0
        elif self.position in (2, 5, 8):
            column = 1
        elif self.position in (3, 6, 9):
            column = 2

        x = column * self.width * 500
        y = row * self.height * 500
        logProcessing(pathToCard, 'Position: ' + str(self.position) + ': (' + str(x) + ', ' + str(y) + ')')
        card = pdb.gimp_file_load_layer(self.frontPage, pathToCard)
        pdb.gimp_image_insert_layer(self.frontPage, card, None, 0)
        pdb.gimp_layer_set_offsets(card, x, y)

        if column == 2:
            column = 0
        elif column == 0:
            column = 2

        x = column * self.width * 500
        pathToCard = pathToCard[:len(pathToCard) - 4] + '-Back.png'
        card = pdb.gimp_file_load_layer(self.backPage, pathToCard)
        pdb.gimp_image_insert_layer(self.backPage, card, None, 0)
        pdb.gimp_item_transform_rotate_simple(card, ROTATE_270, 1, 0, 0)
        pdb.gimp_layer_set_offsets(card, x, y)

        self.position += 1


    def mergeAndWriteImageToFile(self, img, _file):
        logProcessing(str(self.pageNumber), 'Writing ' + _file)
        merged = pdb.gimp_image_merge_visible_layers(img, CLIP_TO_IMAGE)
        pdb.file_png_save2(img, merged, _file, _file, FALSE, 9, FALSE, pdb.gimp_drawable_has_alpha(merged), FALSE, TRUE, FALSE, TRUE, FALSE )

    def writePage(self):
        if self.position > 1:
            self.mergeAndWriteImageToFile(self.frontPage, self.frontFileName)
            self.mergeAndWriteImageToFile(self.backPage, self.backFileName)

        logProcessing(str(self.pageNumber), 'Cleaning up')
        pdb.gimp_image_delete(self.frontPage)
        pdb.gimp_image_delete(self.backPage)
        logProcessing(str(self.pageNumber), 'Clean')


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def logError(exception, record_name):
    global errOut
    if errOut is None:
        errOut = open("C:\Users\u0064666\Pictures\Cards\\renderLog_errors.txt", "w")
    errOut.write("[" + record_name +"]: " + str(exception))


def logProcessing(record_name, msg):
    global logOut
    if logOut is None:
        logOut = open("C:\Users\u0064666\Pictures\Cards\\renderLog.txt", "w")
    logOut.write("[" + record_name + "]: " + msg + "\r\n")
    logOut.flush()
    os.fsync(logOut.fileno())

def make_card_grid(image, drawable, inDirectory, outdirectory):
    # Group the operations of this script
    # load the weapon dictionary

    logProcessing("Make Card Grid Program", "Processing Starting")

    if not os.path.exists(outdirectory):
        os.makedirs(outdirectory)


    cardCount = 0
    pageCount = 1
    page = Page(pageCount, outdirectory)
    for card in listdir_fullpath(inDirectory):
            if card[len(card) - 3:] != 'png' or card.find('-Back') > 0:
                continue
            page.addCard(card)
            cardCount += 1
            if cardCount > 9:
                page.writePage()
                pageCount += 2
                page = Page(pageCount, outdirectory)
                cardCount = 0

    if page is not None:
        page.writePage()



register(
        "make_card_grid",
        "t",
        "t",
        "Michael Pickens",
        "Michael Pickens",
        "2013",
        "<Image>/_Infinity/_Generate Card Grid",
        "RGB*, GRAY*",
        [
                (PF_STRING, "inDirectory", "Source File", ""),
                (PF_STRING, "outdirectory", "Destination directory", ""),
        ],
        [],
        make_card_grid)

main()

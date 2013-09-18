#!/usr/bin/env python
from gimpfu import *
import sys
import os

__author__ = 'Michael'
#rootPath = "F:\Users\Michael\Documents\GitHub\InfinityTroopCards"
rootPath = "C:\Users\u0064666\Documents\GitHub\InfinityTroopCards"

page = None


class Page:

    logOut = None
    outdir = ''
    pageId = 0
    frontPage = None
    backPage = None

    def __init__(self, pageId, outdir, logObj):
        self.frontPage = pdb.gimp_image_new(4250, 5500, 0)
        self.backPage = pdb.gimp_image_new(4250, 5500, 0)
        self.outdir = outdir
        self.pageId = pageId
        self.logOut = logObj

        pdb.gimp_image_set_resolution(self.frontPage, 500, 500)
        pdb.gimp_image_set_resolution(self.backPage, 500, 500)


    def save(self):
        outfile = self.outdir + '\\Page' + str(self.pageId) + ".png"
        merged = pdb.gimp_image_merge_visible_layers(self.frontPage, CLIP_TO_IMAGE)
        pdb.file_png_save2(self.frontPage, merged, outfile, outfile, FALSE, 9, FALSE, pdb.gimp_drawable_has_alpha(merged), FALSE, TRUE, FALSE, TRUE, FALSE )
        pdb.gimp_image_delete(self.frontPage)

        outfile = self.outdir + '\\Page' + str(self.pageId+1) + ".png"
        merged = pdb.gimp_image_merge_visible_layers(self.backPage, CLIP_TO_IMAGE)
        pdb.file_png_save2(self.backPage, merged, outfile, outfile, FALSE, 9, FALSE, pdb.gimp_drawable_has_alpha(merged), FALSE, TRUE, FALSE, TRUE, FALSE )
        pdb.gimp_image_delete(self.backPage)

        return

    def addCard(self, filename, layerName, cardIndex):
        self.logOut.write('[Page ' + str(self.pageId) + ']: Adding [' + filename.strip() + ']\tLayer: ' + layerName + '\r\n')
        if len(filename) <= 0:
            self.logOut.write('[Page ' + str(self.pageId) + ']: Attempting to add blank file name [' + filename.strip() + '] Bailing.\r\n')
            return
        ## Front of card
        imgFromDisk = pdb.gimp_file_load_layer(self.frontPage, filename)
        # copy the image from disk to the image
        pdb.gimp_image_insert_layer(self.frontPage, imgFromDisk, None, 0)
        # resize the image to the layer size
        pdb.gimp_layer_scale(imgFromDisk, 2500, 1500, FALSE)
        #rotate the layers if card index is 1 or 2
        if cardIndex < 3:
            imgFromDisk = pdb.gimp_item_transform_rotate_simple(imgFromDisk, 0, TRUE, 2125.00, 2750.00)
        # pick the x,y offsets
        x, y = 0,0
        if cardIndex == 2:
            y = 2500
        if cardIndex >= 3:
            x = 1500
            if cardIndex == 4:
                y = 1500
            if cardIndex == 5:
                y = 3000
        self.logOut.write('[Page ' + str(self.pageId) + ']: X ' + str(x) + ', Y: ' + str(y) + '\r\n')
        # set the new layer's position to overlay the positional layer
        pdb.gimp_layer_set_offsets(imgFromDisk, x, y)

        ## Back of card
        i = filename.rfind('.')
        filename = filename[:i] + '-Back' + filename[i:]
        self.logOut.write('[Back Page ' + str(self.pageId ) + ']: Adding ' + filename + '\tLayer: ' + layerName + '\r\n')
        imgFromDisk = pdb.gimp_file_load_layer(self.backPage, filename)
        # copy the image from disk to the image
        pdb.gimp_image_insert_layer(self.backPage, imgFromDisk, None, 0)
        # resize the image to the layer size
        pdb.gimp_layer_scale(imgFromDisk, 1500, 2500, FALSE)
        #rotate the layers if card index is 1 or 2
        if cardIndex >= 3:
            imgFromDisk = pdb.gimp_item_transform_rotate_simple(imgFromDisk, 2, TRUE, 2125.00, 2750.00)
        # pick the x,y offsets
        x, y = 0, 0
        if cardIndex == 1:
            x = 2750
        if cardIndex == 2:
            x = 2750
            y = 2500
        if cardIndex >= 3:
            x = 250
            if cardIndex == 4:
                y = 1500
            if cardIndex == 5:
                y = 3000

        # set the new layer's position to overlay the positional layer
        pdb.gimp_layer_set_offsets(imgFromDisk, x, y)
        self.logOut.write('[Back Page ' + str(self.pageId) + ']: X ' + str(x) + ', Y: ' + str(y) + '\r\n')

def make_pdf_image_from_render_directory(image, drawable, sourceDirectory, outDirectory):
    logOut = open(os.path.join(rootPath, 'renderLog.txt'), 'w')
    cardsOnPage = 0
    pageCount = 0

    for renderDirectory in os.listdir(sourceDirectory):
        outDirectory = sourceDirectory + '\\' + renderDirectory + '\Merged'
        if not os.path.exists(outDirectory):
            os.makedirs(outDirectory)

        dirname = sourceDirectory + '\\' + renderDirectory
        filenames = os.listdir(dirname)

        if cardsOnPage > 0:
            cardsOnPage = 0
            page.save()
            pageCount += 2
            logOut.flush()


        logOut.write('[Source Directory]:' + sourceDirectory  + '\r\n')
        logOut.write('[Render Directory]:' + renderDirectory + '\r\n')
        logOut.write('[Output Directory]:' + outDirectory + '\r\n')

        for filename in filenames:
            logOut.write('[' + renderDirectory + ']:' + filename + '\r\n')

            if len(filename.strip()) <= 0 or filename == 'Merged':
                logOut.write('Blank filename\r\n')
                continue

            if cardsOnPage > 5:
                cardsOnPage = 0
                page.save()
                pageCount += 2
                logOut.flush()


            if cardsOnPage == 0:
                page = Page(pageCount, outDirectory, logOut)

            if filename.find('-Back') != -1:
                continue

            cardsOnPage += 1
            if cardsOnPage == 1:
                page.addCard(os.path.join(dirname, filename), 'Left-One', 1)
            if cardsOnPage == 2:
                page.addCard(os.path.join(dirname, filename), 'Left-Two', 2)
            if cardsOnPage == 3:
                page.addCard(os.path.join(dirname, filename), 'Right-One', 3)
            if cardsOnPage == 4:
                page.addCard(os.path.join(dirname, filename), 'Right-Two', 4)
            if cardsOnPage == 5:
                page.addCard(os.path.join(dirname, filename), 'Right-Three', 5)

    logOut.flush()
    logOut.close()

register(
        "make_pdf_image_from_render_directory",
        "t",
        "t",
        "Michael Pickens",
        "Michael Pickens",
        "2013",
        "<Image>/_Infinity/_Compile PDF Pages From Directory",
        "RGB*, GRAY*",
        [
                (PF_STRING, "sourceDirectory", "Source Directory", rootPath + "\\Renders"),
                (PF_STRING, "outDirectory", "Destination directory", rootPath + "\\Renders"),
        ],
        [],
        make_pdf_image_from_render_directory)

main()

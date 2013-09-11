#!/usr/bin/env python
from gimpfu import *
import json

errOut = None
logOut = None

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

def calculate_font_size(text, font, width, height):
    fontsize = 6
    last_extents = None
    last_fontsize = 3
    adjust = 1
    if len(text) > 100:
        pdb.gimp_message(text)
    lineLength = 100
    i = lineLength
    go = True
    while i < len(text):

        i = text.find(' ', i)
        if i < 0:
            break
        text = text[:i].strip() + '\r\n' + text[i:].strip()
        i = i + lineLength
    if len(text) > 100:
        pdb.gimp_message(text)
    while fontsize < 100:
        extents = pdb.gimp_text_get_extents_fontname(text, fontsize, PIXELS, font)
        if extents[0] > width or extents[1] > height:
            return last_fontsize
        last_fontsize = fontsize
        fontsize = fontsize + adjust

    return fontsize

def setTextLayerValue(layer, value):
    font = pdb.gimp_text_layer_get_font(layer)
    size = pdb.gimp_text_layer_get_font_size(layer)
    extents = pdb.gimp_text_get_extents_fontname(value, size[0], PIXELS, font)
    pdb.gimp_text_layer_set_text(layer, value)

def drawRangeBand(template, bs, modifier, bandMin, bandMax):
    fillcolor = None

    fillcolor_positive = '#589900'
    fillcolor_equal = '#b8c800'
    fillcolor_negative = '#fab800'
    fillcolor_realbad = '#fa7a00'
    if modifier > 0:
        fillcolor = fillcolor_positive
    elif modifier == 0:
        fillcolor = fillcolor_equal
    elif modifier == -3:
        fillcolor = fillcolor_negative
    elif modifier <= -6:
        fillcolor = fillcolor_realbad

    for i in range(bandMin, bandMax+1):
        layer = pdb.gimp_image_get_layer_by_name(template, 'RangeBand' + str(i))
        pdb.gimp_context_set_foreground(fillcolor)
        pdb.gimp_edit_bucket_fill(layer, FG_BUCKET_FILL, NORMAL_MODE, 100, 255, FALSE, 0, 0)
        pdb.gimp_context_set_foreground("black")
        text = pdb.gimp_text_layer_new(template, str(bs + modifier), "Orbitron Medium", 30, PIXELS)
        draw_x = layer.offsets[0] + layer.width / 2 - text.width / 2
        draw_y = layer.offsets[1] + layer.height / 2 - text.height / 2
        pdb.gimp_image_insert_layer(template, text, None, 0)
        pdb.gimp_layer_set_offsets(text, draw_x, draw_y)

def addRulesText(template, title, text, background_y):

    title_text_fontsize = 50
    title_text_font = 'Orbitron Medium'

    rules_text_fontsize = 30
    rules_text_font = 'Verdana'

    rules_vertical_offset_padding = 10
    rules_horizontal_offset_padding = 20

    logProcessing(title + ': ' + str(background_y), text)
    temp_image = pdb.gimp_image_new(template.width, template.height, RGB)

    # create a new text layer and set the font to the title font
    title_text_layer = pdb.gimp_text_layer_new(temp_image, 'Title', title_text_font, title_text_fontsize, PIXELS)
    # create a new text layer and set the font to the rules font
    rules_text_layer = pdb.gimp_text_layer_new(temp_image, 'Text', rules_text_font, rules_text_fontsize, PIXELS)
    # set the title text to 0,0 on the new layer
    pdb.gimp_layer_set_offsets(title_text_layer, 0 , 0)
    # insert both layers
    pdb.gimp_image_insert_layer(temp_image, title_text_layer, None, 0)
    pdb.gimp_image_insert_layer(temp_image, rules_text_layer, None, 1)

    pdb.gimp_text_layer_set_text(title_text_layer, title)
    pdb.gimp_text_layer_set_text(rules_text_layer, text)
    # set the rules x to 20 and the y to to the height of the title layer + 10 [magic numbers, adjust manually]
    # calculate the vertical extents of the title
    extents = pdb.gimp_text_get_extents_fontname(title, title_text_fontsize, PIXELS, title_text_font)
    pdb.gimp_text_layer_resize(title_text_layer, 1200, extents[1])

    pdb.gimp_layer_set_offsets(rules_text_layer, rules_horizontal_offset_padding , extents[1] + rules_vertical_offset_padding )
    extents = pdb.gimp_text_get_extents_fontname(text, rules_text_fontsize, PIXELS, rules_text_font)
    line_height = extents[1]
    num_lines = len(text) / 90 + 2
    pdb.gimp_text_layer_resize(rules_text_layer, 1200, line_height * num_lines)
    pdb.gimp_text_layer_set_text(rules_text_layer, text)
    # remove the background layer
    # merge text layers together
    pdb.gimp_image_merge_visible_layers(temp_image, CLIP_TO_IMAGE)
    # autocrop the back ground layer
    pdb.plug_in_autocrop(temp_image, temp_image.layers[0])

    background_x = 140
    # copy the entire layer into the tempalte
    item_copy = pdb.gimp_layer_new_from_drawable(temp_image.layers[0], template)
    # save the height of the layer to be returned later
    height = item_copy.height
    # insert the new layer into the template
    pdb.gimp_image_insert_layer(template, item_copy, None, 0)
    # set the offsets
    pdb.gimp_layer_set_offsets(item_copy, background_x, background_y)
    # merge the new layer down into the template
    pdb.gimp_image_merge_down(template, item_copy, CLIP_TO_IMAGE)
    # clean up the temp image we created
    pdb.gimp_image_delete(temp_image)
    # return height for later layers
    logProcessing('Complete! ' + title + ': ' + str(background_y + height), text)
    return height

def generate_images_from_template(image, drawable, filename, append, outdirectory):
    # Group the operations of this script
    # load the weapon dictionary

    logProcessing("Program", "Processing Starting")
    rangeBands = {
        "4": 1,
        "8": 2,
        "12": 3,
        "16": 4,
        "24": 5,
        "32": 6,
        "36": 7,
        "48": 8,
        "52": 9,
        "60": 10,
        "96": 11,
        "104": 12
    }

    logProcessing("Program", "Processing Reading Weapons dictionary")
    f = open("C:\\Python Projects\\InfinityJSONParser\\Data\\Other\\weapons.json", "r")
    weapons = json.load(f)
    f.close()

    weapon_y_offset = 0
    maxCards = 0
    cardCount = 0
    # open the input
    with open(filename, "r") as f:
        logProcessing(filename, "Reading input file")
        # read the header line to get the names of the layers
        headerLine = f.readline()
        #(UnitNameValue UnitIcon UnitPortrait MOVValue CCValue BSValue PHValue WIPValue ARMValue BTSValue WValue AVAValue SWCCost UnitCost UnitNotesValue Ability1Title Ability1Text Ability2Title Ability2Text Weapon1Value W1SValue W1MValue W1LValue W1MaxValue W1DmgValue W1BValue W1AmmoValue W1SpecialValue Weapon2Value W2SValue W2MValue W2LValue W2MaxValue W2DmgValue W2BValue W2AmmoValue W2SpecialValue Weapon3Value W3SValue W3MValue W3LValue W3MaxValue W3DmgValue W3BValue W3AmmoValue W3SpecialValue Weapon4Value W4SValue W4MValue W4LValue W4MaxValue W4DmgValue W4BValue W4AmmoValue W4SpecialValue Weapon5Value W5SValue W5MValue W5LValue W5MaxValue W5DmgValue W5BValue W5AmmoValue W5SpecialValue)
        bs = 0
        # for each record past the header line
        record = f.readline()
        while record != '':
            cardCount += 1
            if cardCount > int(maxCards) and maxCards > 0:
                break
            try:
                values = record.split('\t')
                # duplicate the template image
                duplicate = pdb.gimp_image_duplicate(image)
                # for each layer name in the header
                index = 0
                outfile = outdirectory + '\\' + values[0]+ append + ".png"
                logProcessing(values[0], "Processing started")
                x = 115
                y = 604
                abilityTitle = ''
                current_y = 118

                for layerName in headerLine.split('\t'):
                    # find the matching layer
                    layerName = layerName.strip()

                    layer = pdb.gimp_image_get_layer_by_name(duplicate, layerName)
                    value = values[index]
                    # if it's a text layer
                    #if layerName[0] == 'W' or layerName[0] == 'w':
    #                    pdb.gimp_message(layerName + ' - ' + value)
                    if append == '-Back':
                        if layerName == 'Ability1Title':
                            abilityTitle = value
                        elif layerName == 'Ability2Title':
                            abilityTitle = value
                        elif layerName == 'Ability1Text' or layerName == 'Ability2Text':
                            current_y += addRulesText(duplicate,abilityTitle, value, current_y) + 20
                    else:
                        if layerName.strip()[:6] == 'Weapon' and append != '-Back':

                            template = pdb.gimp_xcf_load(0, 'C:\Users\u0064666\Pictures\Cards\Templates\\WeaponTemplate.xcf', 'C:\Users\u0064666\Pictures\Cards\Templates\\WeaponTemplate.xcf')
                            weapon = None

                            for w in weapons:
                               if w.get('name', '') == value:
                                    weapon = w
                                    break

                            if weapon != None:
                                ## build weapon template
                                layer = pdb.gimp_image_get_layer_by_name(template, 'Name')
                                setTextLayerValue(layer, weapon.get('name', ''))

                                layer = pdb.gimp_image_get_layer_by_name(template, 'Burst')
                                setTextLayerValue(layer, weapon.get('burst', ''))

                                layer = pdb.gimp_image_get_layer_by_name(template, 'Damage')
                                setTextLayerValue(layer, weapon.get('damage', ''))

                                layer = pdb.gimp_image_get_layer_by_name(template, 'Ammo')
                                setTextLayerValue(layer, weapon.get('ammo', ''))

                                layer = pdb.gimp_image_get_layer_by_name(template, 'Rules')
                                notes = ''
                                if weapon['cc'] == 'Yes':
                                    notes = notes + 'CC '
                                if weapon['template'] != 'No':
                                    notes = notes + weapon['template'] + ' '
                                if weapon['em_vul'] == 'Yes':
                                    notes = notes + 'EM '

                                notes = notes + weapon.get('note', '')
                                setTextLayerValue(layer, notes)

                                ##range bands

                                dist = weapon['short_dist']
                                if dist != '--':
                                    mod = weapon['short_mod']
                                    bandMin = 1
                                    bandMax = rangeBands[dist]
                                    modValue = int(mod)
                                    drawRangeBand(template, bs, modValue, bandMin, bandMax)

                                dist = weapon['medium_dist']
                                if dist != '--':
                                    mod = weapon['medium_mod']
                                    bandMin = bandMax + 1
                                    bandMax = rangeBands[dist]
                                    modValue = int(mod)
                                    drawRangeBand(template, bs, modValue, bandMin, bandMax)

                                dist = weapon['long_dist']
                                if dist != '--':
                                    mod = weapon['long_mod']
                                    bandMin = bandMax + 1
                                    bandMax = rangeBands[dist]
                                    modValue = int(mod)
                                    drawRangeBand(template, bs, modValue, bandMin, bandMax)

                                dist = weapon['max_dist']
                                if dist != '--':
                                    mod = weapon['max_mod']
                                    bandMin = bandMax + 1
                                    bandMax = rangeBands[dist]
                                    modValue = int(mod)
                                    drawRangeBand(template, bs, modValue, bandMin, bandMax)


                                layer = pdb.gimp_image_merge_visible_layers(template, CLIP_TO_IMAGE)

                                item_copy = pdb.gimp_layer_new_from_drawable(layer, duplicate)
                                pdb.gimp_image_insert_layer(duplicate, item_copy, None, 0)
                                pdb.gimp_layer_set_offsets(item_copy, x, y)
                                y = y + item_copy.height

                                pdb.gimp_image_merge_down(duplicate, item_copy, CLIP_TO_IMAGE)

                            pdb.gimp_image_delete(template)
                        elif layer == None:
                            #pdb.gimp_message("[" + layerName + "] could not be found")
                            badlayer = 0
                        elif pdb.gimp_drawable_is_text_layer(layer) == 1:
                            # replace the text of the text layer with the matching value in the current record
                            font = pdb.gimp_text_layer_get_font(layer)
                            size = pdb.gimp_text_layer_get_font_size(layer)
                            extents = pdb.gimp_text_get_extents_fontname(value, size[0], PIXELS, font)
                            #if extents[0] > layer.width or extents[1] > layer.height:
                             #   fontsize = calculate_font_size(value, font, layer.width, layer.height)
                              #  pdb.gimp_text_layer_set_font_size(layer, fontsize, PIXELS)
                            pdb.gimp_text_layer_set_text(layer, value)
                        elif len(value) > 0:
                            # if not a text layer
                            try:
                                imgFromDisk = pdb.gimp_file_load_layer(duplicate, value)
                                # copy the image from disk to the image
                                pdb.gimp_image_insert_layer(duplicate, imgFromDisk, None, 0)
                                # resize the image to the layer size
                                pdb.gimp_layer_scale(imgFromDisk, layer.width, layer.height, FALSE)
                                # set the new layer's position to overlay the positional layer
                                pdb.gimp_layer_set_offsets(imgFromDisk, layer.offsets[0], layer.offsets[1])
                            except:
                                logError(None, "Failed to process image data for " + value)
                                pass

                        if layerName == 'BSValue':
                            try:
                                bs = int(value)
                            except Exception as e:
                                logError(e, values[0])
                                pass

                    index = index + 1
                # write the duplicate to disk
                # width = 4.25" * 500 pixels per inch
                scaled_width = 3.66
                width = scaled_width * 500
                # height =  3" *
                height = 3 * ( scaled_width / 5) * 500
                pdb.gimp_image_scale(duplicate, width, height)
                merged = pdb.gimp_image_merge_visible_layers(duplicate, CLIP_TO_IMAGE)
                logProcessing(values[0], "Writing PNG")
                #pdb.gimp_image_set_resolution(duplicate, 500, 500)
                pdb.file_png_save2(duplicate, merged, outfile, outfile, FALSE, 9, FALSE, pdb.gimp_drawable_has_alpha(merged), FALSE, TRUE, FALSE, TRUE, FALSE )
                pdb.gimp_image_delete(duplicate)
            except Exception as e:
                logError(e, values[0])
                pass
            record = f.readline()
            logProcessing("Program", "Processing Completed")

register(
        "generate_images_from_template",
        "t",
        "t",
        "Michael Pickens",
        "Michael Pickens",
        "2013",
        "<Image>/_Infinity/_Generate Images from Template",
        "RGB*, GRAY*",
        [
                (PF_STRING, "filename", "Source File", "exmaple.dat"),
                (PF_STRING, "append", "Append To FileName", ""),
                (PF_STRING, "outdirectory", "Destination directory", ""),

        ],
        [],
        generate_images_from_template)

main()

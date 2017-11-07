#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python 3 script to recover xmltv from http://xmltv.dtdns.net
# Author : Aymeric LAMBRECHT

import xml.etree.ElementTree as etree
import uuid, subprocess, os.path, argparse

ZIP_LINK ='http://xmltv.dtdns.net/download/tnt.zip'
ZIP_PATH = os.path.join('/tmp',str(uuid.uuid4())+'.zip')
XMLTV_PATH = os.path.join('/tmp','cloud21.xml')
TVGUIDE_PATH = os.path.join('/tmp','tvguide.xml')

DESCRIPTION = "Script to install xml grabber for TVHeadend"

parser = argparse.ArgumentParser(description = DESCRIPTION)
parser.add_argument('-v', dest = 'verbose', help = 'enable verbose mode', action='store_true', default=False)
parser.add_argument('--list_categories', dest="xmltv_path_to_list", help = 'XMLTV PATHFILE to list categories', action="store", type=str, default='')
args = parser.parse_args()


def send_command(command, blocking = True, stdin = None, stdout = None):

    if stdin is None:
        stdin = subprocess.PIPE
    if stdout is None:
        stdout = subprocess.PIPE

    process = subprocess.Popen(command, stdin = stdin, stdout = stdout)

    result = None
    output = ""
    if(blocking):
        if(stdout != True):
            result = process.wait()
            output = process.stdout.read()
    return result, output

def download_xmltv():
    download_command = ['wget', '-q', ZIP_LINK, '-O', ZIP_PATH]
    if(args.verbose):
        print('[INFO] Téléchargement du zip : ')
        download_command.append('--show-progress')
    result, _ = send_command(download_command)
    if(result == 0):
        if(args.verbose):
            print('[INFO] Téléchargement réussi ')
        return True
    else:
        if(args.verbose):
            print('[ERR] Téléchargement échoué : ')
        return False

def unzip_xmltv():
    unzip_command = ['unzip', '-q', '-o', ZIP_PATH, '-d', '/tmp']
    rm_command = ["rm", "-fr", ZIP_PATH]
    result, _ = send_command(unzip_command)
    if(result == 0):
        if(args.verbose):
            print("[INFO] Décompression OK")
        send_command(rm_command)
        return True
    else:
        if(args.verbose):
            print("[ERR] Decompression failed")
        send_command(rm_command)
        return False

def list_categories():
    print("[INFO] List categories in progress ...")
    print(args.xmltv_path_to_list)
    tree = etree.parse(args.xmltv_path_to_list)
    root = tree.getroot()
    list_categories = []

    for programme in root.iter('programme'):

        # get category subelemnt's for each programme
        category = programme.find('category')
        if category is not None:
            # get category name's for each programme
            category_name = category.text
            # detect unrecognized category
            if category_name not in list_categories:
                list_categories.append(category_name)

    list_categories.sort()
    print("[INFO] List categories finished")
    print("[INFO] List of categories : ")
    for category_name in list_categories:
        print(category_name)
    print("[INFO] Number of categories")
    print(len(list_categories))

def try_match_category( value, match_category ):
    # print("[INFO] try_match_category with", value)
    subString = value.split(' ')
    length = len(subString)
    i = 0
    while(i < length):
        for frCat, tvhCat in match_category.items():
            # print("[INFO] frCat", frCat)
            # print("[INFO] tvhCat", tvhCat)
            if subString[i] in frCat:
                print("match found:", subString[i], ">>", tvhCat)
                return subString[i], tvhCat
        i = i+1
    return None


def update_category_generator():
    print("[INFO] Update category generator in progress ...")
    print(args.xmltv_path_to_list)
    tree = etree.parse(args.xmltv_path_to_list)
    root = tree.getroot()
    unrecognized_category = []
    match_category = {}

    # Correspondance chaines
    match_category['clips'] = 'Music / Ballet / Dance'
    match_category['concert'] = 'Music / Ballet / Dance'
    match_category['ballet'] = 'Music / Ballet / Dance'
    match_category['débat'] = 'Social / Political issues / Economics'
    match_category['dessin animé'] = 'Social / Political issues / Economics'
    match_category['divertissement'] = 'Show / Game show'
    match_category['divers'] = 'Variety show'
    match_category['documentaire'] = 'Education / Science / Factual topics'
    match_category['Émission'] = 'Show / Game show'
    match_category['feuilleton'] = 'Movie / Drama'
    match_category['film'] = 'Movie / Drama'
    match_category['fitness'] = 'Fitness and health'
    match_category['fin'] = 'fin'
    match_category['jeu'] = 'News / Current affairs'
    match_category['jeunesse'] = 'Children\'s / Youth programmes'
    match_category['journal'] = 'News / Current affairs'
    match_category['loterie'] = 'Show / Game show'
    match_category['météo'] = 'News / Current affairs'
    match_category['magazine'] = 'Education / Science / Factual topics'
    match_category['opéra'] = 'Arts / Culture (without music)'
    match_category['politique'] = 'Social / Political issues / Economics'
    match_category['série'] = 'Movie / Drama'
    match_category['spectacle'] = 'Arts / Culture (without music)'
    match_category['sport'] = 'Sports'
    match_category['talk show'] = 'Show / Game show'
    match_category['téléfilm'] = 'Movie / Drama'
    match_category['téléréalité'] = 'Show / Game show'
    match_category['théâtre'] = 'Arts / Culture (without music)'
    match_category['variétés'] = 'Arts / Culture (without music)'

    if not root:
        print("Root is null")
        return

    for programme in root.iter('programme'):
        # get category subelemnt's for each programme
        category_subelt = programme.find('category')
        if category_subelt is not None:
            # get category name's for each programme
            category_name = category_subelt.text
            print(category_name)
            # detect unrecognized category
            if category_name not in match_category:
                new_category = try_match_category(category_name, match_category)
                if new_category is None:
                    if category_name not in unrecognized_category:
                        unrecognized_category.append(category_name)
        else:
            print("programme is null")

    # build the new xml file with correct category names
    print("[INFO] Migration OK")
    print("[INFO] List of unrecognized category")
    for category in unrecognized_category:
        print(category)
    print("[INFO] Number of unrecognized category")
    print(len(unrecognized_category))
    print("[INFO] List of recognized category")
    for match in match_category:
        print(match)

def update_category():
    if(args.verbose):
        print("[INFO] Migrate category in progress ...")
    tree = etree.parse(XMLTV_PATH)
    root = tree.getroot()
    unrecognized_category = []
    match_category = {}

    # Correspondance chaines
    match_category['clips'] = 'Music / Ballet / Dance'
    match_category['concert'] = 'Music / Ballet / Dance'
    match_category['ballet'] = 'Music / Ballet / Dance'
    match_category['débat'] = 'Social / Political issues / Economics'
    match_category['dessin animé'] = 'Social / Political issues / Economics'
    match_category['divertissement'] = 'Show / Game show'
    match_category['divers'] = 'Variety show'
    match_category['documentaire'] = 'Education / Science / Factual topics'
    match_category['Émission'] = 'Show / Game show'
    match_category['feuilleton'] = 'Movie / Drama'
    match_category['film'] = 'Movie / Drama'
    match_category['fitness'] = 'Fitness and health'
    match_category['fin'] = 'fin'
    match_category['jeu'] = 'News / Current affairs'
    match_category['jeunesse'] = 'Children\'s / Youth programmes'
    match_category['journal'] = 'News / Current affairs'
    match_category['loterie'] = 'Show / Game show'
    match_category['météo'] = 'News / Current affairs'
    match_category['magazine'] = 'Education / Science / Factual topics'
    match_category['opéra'] = 'Arts / Culture (without music)'
    match_category['politique'] = 'Social / Political issues / Economics'
    match_category['série'] = 'Movie / Drama'
    match_category['spectacle'] = 'Arts / Culture (without music)'
    match_category['sport'] = 'Sports'
    match_category['talk show'] = 'Show / Game show'
    match_category['téléfilm'] = 'Movie / Drama'
    match_category['téléréalité'] = 'Show / Game show'
    match_category['théâtre'] = 'Arts / Culture (without music)'
    match_category['variétés'] = 'Arts / Culture (without music)'

    for programme in root.iter('programme'):
        # get category subelemnt's for each programme
        category_subelt = programme.find('category[1]')
        # get category name's for each programme
        category_name = category_subelt.text
        # we must get extra category subelemnt's to delete after
        extra_category = programme.find('category[2]')
        # detect unrecognized category
        if category_name not in match_category:
            if category_name not in unrecognized_category:
                unrecognized_category.append(category_name)
        else:
            # update category name's
            category_subelt.text = match_category[category_name]
        # remove extra category useless for TVHeadend
        programme.remove(extra_category)

    # build the new xml file with correct category names
    if(args.verbose):
        print("[INFO] Migration OK")
        print("[INFO] Update file tnt.xml")
        print("[INFO] List of unrecognized category")
        for category in unrecognized_category:
            print(category)
        print("[INFO] Number of unrecognized category")
        print(len(unrecognized_category))
        print("[INFO] List of recognized category")
        for match in match_category:
            print(match)
    tree.write(TVGUIDE_PATH, encoding="utf-8")
    # rm_command = ["rm", "-fr", XMLTV_PATH]
    # send_command(rm_command)

def print_xmltv():
    file = open(TVGUIDE_PATH, 'r')
    print(file.read())

def main():
    if(args.xmltv_path_to_list):
        #list_categories()
        update_category_generator()
    else:
        if(download_xmltv()):
            unzip_xmltv()
            update_category()
        if(args.verbose):
            send_command(['tail','-n', '100', TVGUIDE_PATH], True, True, True)
        else:
            print_xmltv()

main()

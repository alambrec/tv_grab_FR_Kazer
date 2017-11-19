#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python 3 script
# Author : Aymeric LAMBRECHT

import xml.etree.ElementTree as etree
import uuid, subprocess, os.path, argparse, sys, logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(funcName)s: %(message)s', datefmt='%H:%M:%S')

DESCRIPTION = "Script to update categories of xmltv files for TVHeadend"

parser = argparse.ArgumentParser(description = DESCRIPTION)

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('--xmltv', dest="XMLTV_PATH", help='Path of XMLTV File to list categories', action="store", type=str, default='', required=True)

args = parser.parse_args()

match_category = {}

def init_categories():
    # Correspondance chaines
    match_category['autre'] = 'Others'
    match_category['clips'] = 'Music / Ballet / Dance'
    match_category['classique'] = 'Serious / Classical / Religious / Historical movie / Drama'
    match_category['cérémonie'] = 'News / Current affairs'
    match_category['cirque'] = 'Sports'
    match_category['chorégraphique'] = 'Music / Ballet / Dance'
    match_category['concert'] = 'Music / Ballet / Dance'
    match_category['cyclisme'] = 'Sports'
    match_category['ballet'] = 'Music / Ballet / Dance'
    match_category['débat'] = 'Social / Political issues / Economics'
    match_category['dessin animé'] = 'Social / Political issues / Economics'
    match_category['divertissement'] = 'Show / Game show'
    match_category['divertissement-humour'] = 'Show / Game show'
    match_category['divers'] = 'Variety show'
    match_category['documentaire'] = 'Education / Science / Factual topics'
    match_category['Émission'] = 'Show / Game show'
    match_category['feuilleton'] = 'Movie / Drama'
    match_category['humour'] = 'Comedy'
    match_category['film'] = 'Movie / Drama'
    match_category['fitness'] = 'Fitness and health'
    match_category['fin'] = 'fin'
    match_category['hippisme'] = 'Sports'
    match_category['interview'] = 'Show / Game show'
    match_category['jazz'] = 'Jazz'
    match_category['jeu'] = 'News / Current affairs'
    match_category['jeunesse'] = 'Children\'s / Youth programmes'
    match_category['journal'] = 'News / Current affairs'
    match_category['kick-boxing'] = 'Sports'
    match_category['loterie'] = 'Show / Game show'
    match_category['météo'] = 'News / Current affairs'
    match_category['magazine'] = 'Education / Science / Factual topics'
    match_category['marathon'] = 'Sports'
    match_category['opéra'] = 'Arts / Culture (without music)'
    match_category['oratorio'] = 'Arts / Culture (without music)'
    match_category['politique'] = 'Social / Political issues / Economics'
    match_category['programme indéterminé'] = 'Others'
    match_category['pop'] = 'Rock / Pop'
    match_category['rap'] = 'Music / Ballet / Dance'
    match_category['reggae'] = 'Folk / Traditional music'
    match_category['rock'] = 'Rock / Pop'
    match_category['série'] = 'Movie / Drama'
    match_category['spectacle'] = 'Arts / Culture (without music)'
    match_category['sport'] = 'Sports'
    match_category['talk show'] = 'Show / Game show'
    match_category['téléfilm'] = 'Movie / Drama'
    match_category['téléfilm érotique'] = 'Adult movie / Drama'
    match_category['téléréalité'] = 'Show / Game show'
    match_category['théâtre'] = 'Arts / Culture (without music)'
    match_category['triathlon'] = 'Sports'
    match_category['variétés'] = 'Arts / Culture (without music)'
    match_category['vtt'] = 'Sports'

def list_categories():
    logging.debug("Entry Point")
    logging.debug("File: %s", args.XMLTV_PATH)
    tree = etree.parse(args.XMLTV_PATH)
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
    logging.debug("List categories finished")
    logging.debug("List of categories")
    for category_name in list_categories:
        logging.debug("> %s", category_name)
    logging.debug("TOTAL: %i categories", len(list_categories))

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
                logging.debug("match found: %s >> %s", subString[i], tvhCat)
                return tvhCat
        i = i+1
    return None

def match_categories():
    logging.debug("Entry Point")
    logging.debug("File: %s", args.XMLTV_PATH)
    tree = etree.parse(args.XMLTV_PATH)
    root = tree.getroot()
    unrecognized_category = []

    if not root:
        logging.error("Root is null")
        return

    for programme in root.iter('programme'):
        # get category subelemnt's for each programme
        category_subelt = programme.find('category')
        if category_subelt is not None:
            # get category name's for each programme
            category_name = category_subelt.text
            # detect unrecognized category
            if category_name not in match_category:
                hts_category_identified = try_match_category(category_name, match_category)
                if hts_category_identified is None:
                    if category_name not in unrecognized_category:
                        unrecognized_category.append(category_name)
                else:
                    match_category[category_name] = hts_category_identified
                    logging.debug(">> UPDATE %40s -> %s", category_name, hts_category_identified)
        else:
            logging.debug("No category found")

    # build the new xml file with correct category names
    logging.debug("Migration OK")
    logging.debug("List of unrecognized category")
    for category in unrecognized_category:
        logging.debug("> %s", category)
    logging.debug("TOTAL: %i unrecognized category", len(unrecognized_category))
    logging.debug("List of recognized category")
    for match in match_category:
        logging.debug("> %s", match)

def generate_categories_sed():
    for key, value in match_category.items():
        #safestr = value.replace('/', '\/').replace('\'', '\'"\'"\'')
        safestr = value.replace("\"", "\\\"")
        #safekey = key.replace('\'', '\'"\'"\'')
        safekey = key.replace("\"", "\\\"")
        # safestr = value
        # logging.debug("sed -ri 's/<category lang=\"fr\">%s/<category lang=\"fr\">%s/g' \"$XMLTV_PATH\"", key, safestr)
        # print("sed -ri \"s/<category lang=\\\"fr\\\">{}/<category lang=\\\"fr\\\">{}/g\" \"$XMLTV_PATH\"".format(key, safestr))
        # print("$SED_COMMAND \'s/<category lang=\\\"fr\\\">{}/<category lang=\\\"fr\\\">{}/g\' \"$XMLTV_PATH\"".format(key, safestr))
        #print("echo \"{} -> {}\"".format(safekey, safestr))
        #print("$SED_COMMAND \"s|<category lang=\\\"fr\\\">{}</category>|<category lang=\\\"fr\\\">{}</category>|g\" \"$XMLTV_PATH\"".format(safekey, safestr))
        print("s|<category lang=\\\"fr\\\">{}</category>|<category lang=\\\"fr\\\">{}</category>|g;\\".format(safekey, safestr))


def main():
    init_categories()
    list_categories()
    match_categories()
    generate_categories_sed()


main()

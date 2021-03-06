# -*- coding: utf-8 -*-
# pylint: disable=locally-disabled, multiple-statements
# pylint: disable=fixme, line-too-long, invalid-name
# pylint: disable=W0703

"""
GeoNames converter from tabbed TXT to JSON

This microservice captures the GeoNames / Gazzetteer list of cities with over 1000 population and
creates a JSON than can be later used with other objectives.

"""

__author__ = 'ea1het'
__date__ = "5 July 2019"
__version__ = "1.0"

import os
import sys
import csv
import json
import glob
import zipfile
import wget


CITIES_URL = 'http://download.geonames.org/export/dump/cities1000.zip'
JSON_FILE = 'cities.json'
TEMP_DIR = './tmp'


def do_getfile(url, f_local='cities.zip'):
    """
     This block downloads the original compressed (Zip) file generated by GeoNames / Gazzeteer and uncompress it in
     the local directory for further treatment

    :param url: a HTTP link
    :param f_local: the locally assigned name of the downloaded file
    :return: f_local: local name once uncompressed of the downloaded file
    """
    try:
        wget.download(url, f_local)
    except Exception as e:
        print('File not found on remote server. More info follows:')
        print(e)
        sys.exit(1)

    return f_local


def do_unzipfile(f_zip):
    """
    This block opens the original TXT file, crafted with tab delimiters, and generates a temporal file with ';'
    (semicolon) field separators

    :param f_zip: a filename in the local disk to open an uncompress
    :return: f_tmp: name of the temporal file used to utterly generate the json file
    """
    with zipfile.ZipFile(f_zip, 'r') as z:
        z.extractall('.')

    f_mine = glob.glob('cities*.txt')

    with open(f_mine[0], 'r') as fich, open('temp.csv', 'w') as f_tmp:
        for line in fich:
            f_tmp.write(line.replace('\t', ';'))

        os.remove(f_mine[0])
        os.remove(f_zip)

    return 'temp.csv'


def do_generatejson(f_in, f_out):
    """
    This block generates, finally, a JSON file from a temporal CSV (semicolon delimited)

    :param f_in: a CSV file with field delimiter set to semicolon (';')
    :param f_out: a JSON file    :return:
    """
    allfieldnames = ['geonameid', 'name', 'ascii_name', 'alter_names', 'latitude', 'longitude',
                     'feature_class', 'feature_code', 'country_code', 'cc2',
                     'admin1_code', 'admin2_code', 'admin3_code', 'admin4_code',
                     'population', 'elevation', 'dig_elevation', 'timezone', 'last_update']

    with open(f_in, 'r') as f_csv, open(f_out, 'w') as f_json:
        reader = csv.DictReader(f_csv, delimiter=';', fieldnames=allfieldnames)
        out = json.dumps([row for row in reader], indent=4)
        f_json.write(out)
        os.remove(f_in)


if __name__ == '__main__':
    f = do_getfile(CITIES_URL)
    f = do_unzipfile(f)
    do_generatejson(f, JSON_FILE)

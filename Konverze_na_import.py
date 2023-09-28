#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from exiftool import ExifToolHelper
import argparse

# Vytvoření parseru pro zpracování argumentů z příkazové řádky
parser = argparse.ArgumentParser(description="Provede konverzi transformovaných dat na import do Reality Capture.")

parser.add_argument("konvertovane_data", help="Cesta k dokumentu s konvertovanými daty z ČUZK")
parser.add_argument("fotky_adresar", help="Cesta k adresáři s fotkami")

# Zpracování argumentů z příkazové řádky
args = parser.parse_args()

# Získání hodnoty zadaného adresáře
konvertovane_data = args.konvertovane_data
fotky_adresar = args.fotky_adresar

# Kontrola, zda zadaný adresář existuje
if not os.path.exists(konvertovane_data):
    print(f"Adresář '{konvertovane_data}' neexistuje.")
else:
    print(f"Zadali jste adresář s konvertovanymi daty: {konvertovane_data}")

if not os.path.exists(fotky_adresar):
    print(f"Adresář '{fotky_adresar}' neexistuje.")
else:
    print(f"Zadali jste adresář s fotkami: {fotky_adresar}")  
    
 
relativni_cesta_exiftool = "./exiftool(-k).exe"

# Seznam všech fotografií v adresáři
fotky = [os.path.join(fotky_adresar, soubor) for soubor in os.listdir(fotky_adresar) if soubor.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Funkce pro extrakci EXIF dat z jedné fotografie
def extrahovat_exif(foto):
    tags = {}
    with ExifToolHelper(executable = relativni_cesta_exiftool) as et:
        for d in et.get_metadata(foto):
            for tag, hodnota in d.items():
                tags[tag] = hodnota
    return tags

exif_data = []

for foto in fotky:
    exif_data.append(extrahovat_exif(foto))
    

#tvorba finalniho txt


with open(konvertovane_data) as transformovane_sour:
  transformovane_sour_radky = transformovane_sour.readlines()

vystupni_soubor = 'finalni_vystup.txt'

# Name GpsLatitude GpsLongitude GpsAltitude RtkStdLat RtkStdLon GimbalYawDegree GimbalPitchDegree GimbalRollDegree
#pozadovane_tagy = ['XMP:RtkStdLat', 'XMP:RtkStdLon', 'XMP:GimbalYawDegree', 'XMP:GimbalPitchDegree', 'XMP:GimbalRollDegree']


with open(vystupni_soubor, 'w') as soubor:
    for i in range(0, len(transformovane_sour_radky)):
        radek = f"{transformovane_sour_radky[i]} {exif_data[i].get('XMP:RtkStdLat')} {exif_data[i].get('XMP:RtkStdLon')} {exif_data[i].get('XMP:GimbalYawDegree')} {exif_data[i].get('XMP:GimbalPitchDegree')} {exif_data[i].get('XMP:GimbalRollDegree')}"
        radek = radek.replace('\t', ' ').replace('\n', ' ').replace('   ', '')
        soubor.write(f"{radek}\n")

print(f"Data byla uložena do souboru {vystupni_soubor}")


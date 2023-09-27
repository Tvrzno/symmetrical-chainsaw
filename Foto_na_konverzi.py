#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from exiftool import ExifToolHelper
import argparse

# Vytvoření parseru pro zpracování argumentů z příkazové řádky
parser = argparse.ArgumentParser(description="Extrahuje EXIF data z fotek v daném adresáři.")

# Přidání argumentu pro zadání adresáře s fotkami
parser.add_argument("fotky_adresar", help="Cesta k adresáři s fotkami")

# Zpracování argumentů z příkazové řádky
args = parser.parse_args()

# Získání hodnoty zadaného adresáře
fotky_adresar = args.fotky_adresar

# Kontrola, zda zadaný adresář existuje
if not os.path.exists(fotky_adresar):
    print(f"Adresář '{fotky_adresar}' neexistuje.")
else:
    print(f"Zadali jste adresář s fotkami: {fotky_adresar}")
    # Zde můžete pokračovat ve zpracování adresáře a extrakci EXIF dat

relativni_cesta_exiftool = "./exiftool(-k).exe"

# Seznam všech fotografií v adresáři
fotky = [os.path.join(fotky_adresar, soubor) for soubor in os.listdir(fotky_adresar) if soubor.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Seznam požadovaných tagů
pozadovane_tagy = ['EXIF:GPSLatitude', 'EXIF:GPSLongitude', 'EXIF:GPSAltitude']

#Funkce na výpis jen daných tagů 
def extrahovat_exif_castecne(foto, tagy):
    tags = ''
    with ExifToolHelper(executable = "C:\\Users\\mates\\CodeCademy\\symmetrical-chainsaw\\exiftool(-k).exe") as et:
        for d in et.get_metadata(foto):
            for tag, hodnota in d.items():
                if tag in tagy:                 
                    tags += f"{hodnota} "
    return tags

# Název výstupního textového souboru
vystupni_soubor = 'exif_gps_data.txt'

# Otevřít textový soubor pro zápis všeho
with open(vystupni_soubor, 'w') as soubor:
    for foto in fotky:
        exif_data = extrahovat_exif_castecne(foto, pozadovane_tagy)
        soubor.write(f"{foto} ")
        for tag_hodnota in exif_data:
            soubor.write(f"{tag_hodnota}")
        soubor.write("\n")

print(f"EXIF data byla uložena do souboru {vystupni_soubor}")


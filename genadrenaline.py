# coding=utf-8
__author__ = 'Drew'
import csv

adrensave = open('adrenalineitemssave.csv')
weapons = csv.reader(adrensave)
conditions = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
writer = ""

for weapon in weapons:
    for condition in conditions:
        writer += weapon[0] + " (" + condition + ")\n"
        writer += "StatTrak%e2%84%a2 " + weapon[0] + " (" + condition + ")\n"

print writer

adren = open('adrenalineitems.csv', "w+")
adren.write(writer)
adren.close()
adrensave.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:24:38 2024

@author: erin
"""
import re

def kwd_string(de,id):
    de_list=de.replace('/',';').split(";")
    id_list=id.replace('/',';').split(";")
    words=[]
    for phrase in de_list:
        word='_'.join(phrase.lstrip().lower().split(' '))
        words.append(word)
    for phrase in id_list:
        word='_'.join(phrase.lstrip().lower().split(' '))
        words.append(word)

    kwds=' '.join(words)+'.'
    
   
    if len(kwds)>2:
        return kwds
    else:
        return ''
    

DE="Mental health; Postnatal depression; Mother; Pregnant; Continuum   supports; Pregnancy periods; Multidisciplinary"
ID="POSTPARTUM DEPRESSIVE SYMPTOMS; RANDOMIZED CONTROLLED-TRIAL; POSTNATAL   DEPRESSION; VULNERABLE FAMILIES; ATTEMPTED-SUICIDE; LOW-INCOME;   INTERVENTION; WOMEN; MANAGEMENT; EFFICACY"

ret=kwd_string(DE,ID)
print(ret)
print(len(ret))

DE=""
ID=""

ret=kwd_string(DE,ID)
print(ret)
print(len(ret))

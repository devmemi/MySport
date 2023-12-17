# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 11:08:45 2023

@author: USUARIO
"""

import math
import time

import sys
import os
import locale

from hashlib import sha256


def ReadConfig():
    basepath = os.path.dirname(os.path.realpath(__file__)) + "\\"
    with open(basepath + 'config.txt') as f:
        lines = f.readlines()
        ConfigData=[]
        for line in lines:
            ConfigData.append(line.replace('\n',''))
    return ConfigData

def DetectLanguage():
    aux=locale.getdefaultlocale()[0]
    if aux=='es_ES':
        Idioma=1
    else:
        Idioma=2
    return Idioma

def Language(Spanish="",English="",Idioma=0):
    Idioma=int(Idioma)
    if  Idioma==1:   #Spanish
        return Spanish
    elif Idioma==2:   #English
        return English
    else:               #Default: Spanish
        return Spanish
    
def Text2SHA256(text = ""):
    return sha256(text.encode('utf-8')).hexdigest()
    
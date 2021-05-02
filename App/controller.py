﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import datetime


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    catalog = model.newCatalog()
    return catalog

def newCharList():
    charList = model.newCharList()
    return charList

def newGenreList():
    genreList = model.newGenreList()
    return genreList

# Funciones para la carga de datos

def loadEvents(catalog):
    eventsfile1 = cf.data_dir + "subsamples-small/context_content_features-small.csv"
    eventsDict1 = csv.DictReader(open(eventsfile1, encoding='utf-8'))
    eventsfile2 = cf.data_dir + "subsamples-small/user_track_hashtag_timestamp-small.csv"
    eventsDict2 = csv.DictReader(open(eventsfile2, encoding='utf-8'))
    eventsfile3 = cf.data_dir + "subsamples-small/sentiment_values.csv"
    eventsDict3 = csv.DictReader(open(eventsfile2, encoding='utf-8'))

    for feeling in eventsDict3:
        model.addFeelings(catalog, feeling)
    for rep2 in eventsDict2:
        model.addRep2(catalog, rep2)
    for rep in eventsDict1:
        position = model.getPosition(catalog)
        model.addReps(catalog, rep, position)
        


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def getChar(charList, charPos):
    bestChar = model.getChar(charList, charPos)
    return bestChar

def getGenre(genreList, genrePos):
    tempoRange = model.getGenre(genreList, genrePos)
    return tempoRange

def repSize(catalog):
   return model.repSize(catalog)

def indexHeight(catalogIndex):
   return model.indexHeight(catalogIndex)

def numArtists(catalog):
    return model.numArtists(catalog)

# Primer requerimiento

def getCharByRange(catalog,bestChar, minchar, maxchar):
    answers = model.getCharByRange(catalog, bestChar, minchar, maxchar)
    return answers

# Segundo requerimiento

def req2(catalog, minCharE, maxCharE, minCharD, maxCharD):
    result = model.req2(catalog, minCharE, maxCharE, minCharD, maxCharD)
    return result


def req5(catalog, initialTime, finalTime):
    initialTi = datetime.datetime.strptime(initialTime, '%H:%M:%S')
    finalTi = datetime.datetime.strptime(finalTime, '%H:%M:%S')
    result = model.req51(catalog, initialTi, finalTi)
    return result

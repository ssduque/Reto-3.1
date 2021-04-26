"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():

    catalog = {"reps":None,
                "instrumentalness":None,
                "liveness":None,
                "speechiness":None,
                "danceability":None,
                "valence":None,
                "loudness":None,
                "tempo":None,
                "acousticness":None}

    catalog["reps"] = lt.newList("SINGLE_LINKED")
    catalog["instrumentalness"]= om.newMap(omaptype='RBT')
    catalog["liveness"] = om.newMap(omaptype='RBT')
    catalog["speechiness"] = om.newMap(omaptype='RBT')
    catalog["danceability"] = om.newMap(omaptype='RBT')
    catalog["valence"] = om.newMap(omaptype='RBT')
    catalog["loudness"] = om.newMap(omaptype='RBT')
    catalog["tempo"] = om.newMap(omaptype='RBT')
    catalog["acousticness"] = om.newMap(omaptype='RBT')
    
    return catalog

def newCharList():
    charList = mp.newMap(numelements = 18, loadfactor = 0.5, prime = 19, maptype="PROBING")
    mp.put(charList, 1, "instrumentalness")
    mp.put(charList, 2, "liveness")
    mp.put(charList, 3, "speechiness")

    mp.put(charList, 4, "danceability")
    mp.put(charList, 5, "valence")
    mp.put(charList, 6, "loudness")

    mp.put(charList, 7, "tempo")
    mp.put(charList, 8, "acousticness")
    mp.put(charList, 9, "energy")
    return charList


# Funciones para agregar informacion al catalogo

def addRep(catalog, rep):
    lt.addLast(catalog["reps"], rep)
    updateInstrumentalness(catalog["instrumentalness"],rep)
    updateLiveness(catalog["liveness"],rep)
    updateSpeechiness(catalog["speechiness"],rep)
    updateDanceability(catalog["danceability"],rep)
    updateValence(catalog["valence"],rep)
    updateLoudness(catalog["loudness"],rep)
    updateTempo(catalog["tempo"],rep)
    updateAcousticness(catalog["acousticness"],rep)
    

def addEntry(dataentry, rep):
    lt.addLast(dataentry,rep)
    return dataentry

def newDataEntry(rep):
    entry = lt.newList("SINGLE_LINKED")
    return entry


def updateAcousticness(map, rep):
    repAcousticness = float(rep['acousticness'])
    entry = om.get(map,repAcousticness)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repAcousticness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, rep)
    return map

def updateDanceability(map, rep):
    repDanceability = float(rep['danceability'])
    entry = om.get(map,repDanceability)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repDanceability, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, rep)
    return map

def updateInstrumentalness(map, rep):
    repInstrumentalness = float(rep['instrumentalness'])
    entry = om.get(map,repInstrumentalness)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repInstrumentalness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, rep)
    return map

def updateLiveness(map, rep):
    repLiveness = float(rep['liveness'])
    entry = om.get(map,repLiveness)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repLiveness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, rep)
    return map

def updateLoudness(map, rep):
    repLoudness = float(rep['loudness'])
    entry = om.get(map,repLoudness)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repLoudness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, rep)
    return map

def updateSpeechiness(map, rep):
    repSpeechiness = float(rep['speechiness'])
    entry = om.get(map,repSpeechiness)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repSpeechiness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, rep)
    return map

def updateTempo(map, rep):
    repTempo = float(rep['tempo'])
    entry = om.get(map,repTempo)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repTempo, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, rep)
    return map

def updateValence(map, rep):
    repValence = float(rep['valence'])
    entry = om.get(map,repValence)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repValence, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, rep)
    return map

# Funciones para creacion de datos



# Funciones de consulta

def repSize(catalog):
    return lt.size(catalog["reps"])

def indexHeight(catalogIndex):
    return om.height(catalogIndex)

def getChar(charList, charPos):
    bestChar = mp.get(charList, charPos)
    return me.getValue(bestChar)

def getCharByRange(catalog, bestChar, minIns, maxIns):
    lst = om.values(catalog[bestChar], minIns, maxIns)
    totreps = 0
    for lstrep in lt.iterator(lst):
        totreps += lt.size(lstrep)
    return totreps

# Funciones utilizadas para comparar elementos dentro de una lista


# Funciones de ordenamiento

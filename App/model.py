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
                "acousticness":None,
                "trackMap":None,
                "artists":None,
                "reps2": None}

    catalog["reps"] = lt.newList(datastructure="ARRAY_LIST")
    catalog["instrumentalness"]= om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["liveness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["speechiness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["danceability"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["valence"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["loudness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["tempo"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["acousticness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["artists"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0, comparefunction=cmpArtistId)
    catalog["reps2"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0, comparefunction=cmpUserId)

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

def newGenreList():
    genreList = lt.newList(datastructure="ARRAY_LIST", cmpfunction= cmpTempoRange)
    reggae = (60.0,90.0,"Reggae")
    downTempo = (70.0,100.0,"Down-Tempo")
    chillOut = (90.0,120.0,"Chill-out")

    hipHop = (85.0,115.0,"Hip-hop")
    JazzAndFunk = (120.0,125.0,"Jazz and Funk")
    pop = (100.0,130.0,"Pop")

    RnB = (60.0,80.0,"R&B")
    rock = (110.0,140.0,"Rock")
    metal = (100.0,160.0,"Metal")

    lt.addLast(genreList, reggae )
    lt.addLast(genreList, downTempo)
    lt.addLast(genreList, chillOut)
    lt.addLast(genreList, hipHop)
    lt.addLast(genreList, JazzAndFunk)
    lt.addLast(genreList, pop)
    lt.addLast(genreList, RnB)
    lt.addLast(genreList, rock)
    lt.addLast(genreList, metal)
    return genreList

# Funciones para agregar informacion al catalogo

def addRep2(catalog, rep2):
    addToMap(catalog,rep2)

def addRep1(catalog,rep):
    existsRep = mp.get(catalog["reps2"], rep["user_id"])
    if existsRep != None:
        repList = me.getValue(existsRep)
        for rep2 in lt.iterator(repList):
            if rep2["track_id"]==rep["track_id"] and rep["created_at"]==rep2["created_at"]:
                lt.addLast(catalog["reps"], rep)
                break
    else:
        return -1

def addReps(catalog, rep, position):
    ans = addRep1(catalog,rep)
    addArtist(catalog, rep, position)
    if ans == -1:
        return None
    else:
        updateInstrumentalness(catalog["instrumentalness"],rep, position)
        updateLiveness(catalog["liveness"],rep, position)
        updateSpeechiness(catalog["speechiness"],rep, position)
        updateDanceability(catalog["danceability"],rep, position)
        updateValence(catalog["valence"],rep, position)
        updateLoudness(catalog["loudness"],rep, position)
        updateTempo(catalog["tempo"],rep, position)
        updateAcousticness(catalog["acousticness"],rep, position)
    

def addEntry(dataentry, rep):
    lt.addLast(dataentry,rep)
    return dataentry

def newDataEntry():
    entry = lt.newList("ARRAY_LIST")
    return entry

def addToMap(catalog,rep2):
    existsEntry = mp.get(catalog["reps2"], rep2["user_id"])
    if existsEntry == None:
        dataentry = newDataEntry()
        mp.put(catalog["reps2"],rep2["user_id"],dataentry)
    else:
        dataentry = me.getValue(existsEntry)
    addEntry(dataentry, rep2)

def addArtist(catalog, rep, position):
    existsArtist = mp.get(catalog["artists"], rep["artist_id"])
    if existsArtist == None:
        dataentry = newDataEntry()
        mp.put(catalog["artists"], rep["artist_id"],dataentry)
    else:
        dataentry = me.getValue(existsArtist)
    addEntry(dataentry,position)

# Funciones para la carga de las caracteristicas

def updateAcousticness(map, rep, position):
    repAcousticness = float(rep['acousticness'])
    entry = om.get(map,repAcousticness)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repAcousticness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map

def updateDanceability(map, rep, position):
    repDanceability = float(rep['danceability'])
    entry = om.get(map,repDanceability)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repDanceability, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map

def updateInstrumentalness(map, rep, position):
    repInstrumentalness = float(rep['instrumentalness'])
    entry = om.get(map,repInstrumentalness)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repInstrumentalness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map

def updateLiveness(map, rep, position):
    repLiveness = float(rep['liveness'])
    entry = om.get(map,repLiveness)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repLiveness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map

def updateLoudness(map, rep, position):
    repLoudness = float(rep['loudness'])
    entry = om.get(map,repLoudness)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repLoudness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map

def updateSpeechiness(map, rep, position):
    repSpeechiness = float(rep['speechiness'])
    entry = om.get(map,repSpeechiness)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repSpeechiness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map

def updateTempo(map, rep, position):
    repTempo = float(rep['tempo'])
    entry = om.get(map,repTempo)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repTempo, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map

def updateValence(map, rep, position):
    repValence = float(rep['valence'])
    entry = om.get(map,repValence)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repValence, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map
#------------------------------------------------


# Funciones para creacion de datos



# Funciones de consulta

def repSize(catalog):
    return lt.size(catalog["reps"])

def indexHeight(catalogIndex):
    return om.height(catalogIndex)

def getChar(charList, charPos):
    bestChar = mp.get(charList, charPos)
    return me.getValue(bestChar)

def getGenre(genreList, genrePos):
    tempoRange = lt.getElement(genreList,genrePos)
    return tempoRange


def getPosition(catalog):
    pos = lt.size(catalog["reps"]) + 1
    return pos

def numArtists(catalog):
    artistList = mp.keySet(catalog["artists"])
    return lt.size(artistList)
#--------------------------------------------------------------------------------------------

# Primer Requerimiento

def getCharByRange(catalog, bestChar, minIns, maxIns):
    lst = om.values(catalog[bestChar], minIns, maxIns)
    finalLst = deleteRepeated(lst)
    totreps = lt.size(finalLst)
    return totreps, lst

def deleteRepeated(lst):
    finalLst = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpPosition)
    for cmpLst in lt.iterator(lst):
        for cmpPos in lt.iterator(cmpLst):
            if lt.isPresent(finalLst, cmpPos) == 0:
                lt.addLast(finalLst, cmpPos)
    return finalLst

# Segundo Requerimiento



# Tercer Requerimiento

# Cuarto Requerimiento



# Quinto Requerimiento

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpCharacteristics(char1, char2):
    if (float(char1) == float(char2)):
        return 0
    elif float(char1) > float(char2):
        return 1
    else:
        return -1

def cmpPosition(pos1,pos2):
    if int(pos1) == int(pos2):
        return 0
    elif int(pos1) > int(pos2):
        return 1
    else:
        return -1

def cmpUserId(id1,entry):
    identry = me.getKey(entry)
    if (int(id1) == int(identry)):
        return 0
    elif (int(id1) > int(identry)):
        return 1
    else:
        return -1

def cmpArtistId(id1, entry):
    identry = me.getKey(entry)
    if id1 == identry:
        return 0
    elif id1 > identry:
        return 1
    else:
        return -1

def cmpTempoRange(range1, range2):
    if range1[0]+range1[1] == range2[0]+range2[1]:
        return 0
    elif range1[0]+range1[1] > range2[0]+range2[1]:
        return 1
    else:
        return -1
# Funciones de ordenamiento



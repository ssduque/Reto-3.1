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
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
#------------------------
# Construccion de modelos
#------------------------
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
                "energy":None,
                "trackMap":None,
                "artists":None,
                "reps2": None,
                "times":None,
                "feelings":None}

    catalog["reps"] = lt.newList(datastructure="ARRAY_LIST")
    catalog["instrumentalness"]= om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["liveness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["speechiness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["danceability"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["valence"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["loudness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["tempo"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["acousticness"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["energy"] = om.newMap(omaptype='RBT', comparefunction=cmpCharacteristics)
    catalog["artists"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0, comparefunction=cmpArtistId)
    catalog["reps2"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0, comparefunction=cmpUserId)
    
    catalog["times"] = om.newMap(omaptype='RBT', comparefunction=compareTimes)
    catalog["feelings"] = mp.newMap(numelements=40000, prime=20011, maptype="CHAINING", loadfactor = 2.0)

    return catalog

#------------------------------------------------
# Funciones para agregar informacion al catalogo
#------------------------------------------------
def addFeelings(catalog, feeling):
    addFeeling(catalog, feeling)

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
        updateEnergy(catalog["energy"],rep, position)
        updateTimes(catalog["times"],rep, position)
    

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

def addFeeling(catalog,feeling):
    existsEntry = mp.get(catalog["feelings"], feeling["hashtag"])
    if existsEntry == None:
        dataentry = newDataEntry()
        mp.put(catalog["feelings"],feeling["hashtag"],dataentry)
    else:
        dataentry = me.getValue(existsEntry)
    addEntry(dataentry, feeling)

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

def updateEnergy(map, rep, position):
    repValence = float(rep['energy'])
    entry = om.get(map,repValence)
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repValence, dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map

def updateTimes(map, rep, position):
    repOccuredOn = rep['created_at']
    repDate = datetime.datetime.strptime(repOccuredOn, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map,repDate.time())
    if (entry is None):
        dataentry = newDataEntry()
        om.put(map, repDate.time(), dataentry)
    else:
        dataentry = me.getValue(entry)
    addEntry(dataentry, position)
    return map


#---------------------------------
# Funciones para creacion de datos
#----------------------------------

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

#------------------------
# Funciones de consulta
#------------------------

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

def req2(catalog, minCharE, maxCharE, minCharD, maxCharD):
    lst1 = om.values(catalog["energy"], minCharE, maxCharE)
    lst2 = om.values(catalog["danceability"], minCharD, maxCharD)
    finalLst1 = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpPosition)
    finalLst2 = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpPosition)
    finalLst3 = lt.newList(datastructure="ARRAY_LIST", cmpfunction=cmpPosition)
    for element in lt.iterator(lst1):
        for element1 in lt.iterator(element):
            lt.addLast(finalLst1, element1)
    for element in lt.iterator(lst2):
        for element1 in lt.iterator(element):
            lt.addLast(finalLst2, element1)
    for element in lt.iterator(finalLst1):
        if lt.isPresent(finalLst2, element):
            lt.addLast(finalLst3, element)
    finalList = deleteRepeated(finalLst3)
    return finalLst


        



# Tercer Requerimiento

# Cuarto Requerimiento



# Quinto Requerimiento

def req5(catalog, initialTi, finalTi):

    # Obtiene una lista que contiene en cada posición una lista con los eventos de escucha de una determinada fecha

    lst = om.values(catalog['times'], initialTi, finalTi)

    # Crea un diccionario para cada genero musical

    reggae = { 'reps': 0, 'avg' : 0, 'name': 'Reggae'}
    d_t = { 'reps' : 0, 'avg' : 0, 'name' : 'Down-Tempo'}
    c_o = { 'reps' : 0, 'avg' : 0, 'name' : 'Chill-Out'}
    h_h = { 'reps' : 0, 'avg' : 0, 'name' : 'Hip-Hop'}
    j_f = { 'reps' : 0, 'avg' : 0, 'name' : 'Jazz and Funk'}
    po = { 'reps' : 0, 'avg' : 0, 'name' : 'Pop'}
    rYb = { 'reps' : 0, 'avg' : 0, 'name' : 'R&B'}
    rock = { 'reps' : 0, 'avg' : 0, 'name' : 'Rock'}
    metal = { 'reps' : 0, 'avg' : 0, 'name' : 'Metal'}

    # Para cada elemento en cada fecha de la lista de fechas obtiene el genero y lo suma a la cantidad de pistas de ese determinado genero,
    # Adicionalmente toma el valor de vader_avg y lo suma a la suma de su determinado genero

    for element in lst:
        for element1 in element:
            a = mp.get(catalog['reps2'], element1['user_id'])
            b = me.getValue(a)['hashtag']
            c = mp.get(catalog['feelings'], b)
            senti = me.getValue(c)
            if(element1['tempo'] >= 60 and element1['tempo'] <= 90 ):
               reggae['reps'] = reggae['reps'] + 1
               reggae['avg'] = reggae['avg'] + senti['vader_avg']
            if(element1['tempo'] >= 70 and element1['tempo'] <= 100 ):
               d_t['reps'] = d_t['reps'] + 1
               d_t['avg'] = d_t['avg']+ senti['vader_avg']
            if(element1['tempo'] >= 90 and element1['tempo'] <= 120 ):
               c_o['reps'] = c_o['reps'] + 1
               c_o['avg'] = c_o['avg']+ senti['vader_avg']
            if(element1['tempo'] >= 85 and element1['tempo'] <= 115 ):
               h_h['reps'] = h_h['reps']+ 1
               h_h['avg'] = h_h['avg'] + senti['vader_avg']
            if(element1['tempo'] >= 120 and element1['tempo'] <= 125 ):
               j_f['reps'] = j_f['reps'] + 1
               j_f['avg'] = j_f['avg']+ senti['vader_avg']
            if(element1['tempo'] >= 100 and element1['tempo'] <= 130 ):
               po['reps'] = po['reps'] + 1
               po['avg'] = po['avg']+ senti['vader_avg']
            if(element1['tempo'] >= 60 and element1['tempo'] <= 80 ):
               rYb['reps'] = rYb['reps']+ 1
               rYb['avg'] = rYb['avg'] + senti['vader_avg']
            if(element1['tempo'] >= 110 and element1['tempo'] <= 140 ):
               rock['reps'] = rock['reps'] + 1
               rock['avg'] = rock['avg'] + senti['vader_avg']
            if(element1['tempo'] >= 100 and element1['tempo'] <= 160 ):
               metal['reps'] = metal['reps'] + 1
               metal['avg'] = metal['avg'] + senti['vader_avg']

    # Obtiene el genero mas repetido, el promedio de vader_avg de cada una de las pistas que pertenecen a ese genero y los retorna

    maxi = max(reggae['reps'], d_t['reps'], c_o['reps'], h_h['reps'], j_f['reps'], po['reps'], rYb['reps'], rock['reps'], metal['reps']) 
    name = maxi['name']
    avg = (maxi['reps']/maxi['avg'])
    return name, avg

def req51(catalog, initialTi, finalTi):

    lst = om.values(catalog['times'], initialTi, finalTi)
    return lst



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

def compareTimes(time1, time2):
    """
    Compara dos tiempos
    """
    if (time1 == time2):
        return 0
    elif (time1 > time2):
        return 1
    else:
        return -1
# Funciones de ordenamiento



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
    """Crea un catalogo con las siguientes entradas:
    1. halfList: Una lista con las entradas del primer archivo csv.
    2. completeList: Una lista de todas las entradas que estan en ambos archivos csv combinadas
    3. Una lista de diccionarios con los artistas y el numero de veces que cada uno se repite en el completeList
    4. Una lista de diccionarios con las pistas y el numero de veces que cada una se repite en el completeList
    5. Un RBT creado para ordenar las entradas del primer archivo csv y poderlas combinar con el segundo archivo."""

    catalog = {"halfList":None,
                "completeList": None,
                "artistList":None,
                "trackList":None,
                "trackMap":None}

    catalog["halfList"] = lt.newList("SINGLE_LINKED")
    catalog["completeList"] = lt.newList("SINGLE_LINKED")
    catalog["artistList"] = lt.newList("SINGLE_LINKED")
    catalog["trackList"] = lt.newList("SINGLE_LINKED")
    catalog["trackMap"]= om.newMap(omaptype='RBT')
    return catalog

# Funciones para agregar informacion al catalogo

def addFirstEntrySet(catalog, entry):
    lt.addLast(catalog["halfList"], entry)
    position = lt.size
    addToTrackMap(catalog,entry,position)

def addSecondEntrySet(catalog, entry):
    date = entry["created_at"]
    trackId = entry["track_id"]
    userId = entry["user_id"]
    artistId = entry["artist_id"]
    trackMap = catalog["trackMap"]
    artistList = catalog["artistList"]
    trackList = catalog["trackList"]
    userMap = me.getValue(om.get(trackMap, trackId))
    dateMap = me.getValue(om.get(userMap, userId))
    position = me.getValue(om.get(dateMap, date))
    halfEntry = lt.getElement(catalog["halfList"], position)
    fullEntry = halfEntry + entry
    lt.addLast(catalog["completeList"], fullEntry)

    existsArtist = lt.isPresent(artistList,artistId)
    existsTrack = lt.isPresent(trackList,trackId)
    if existsArtist != 0:
        artistEntry = lt.getElement(artistList,existsArtist)
        artistEntry["repetitions"]+=1
    else:
        artistEntry = newArtistEntry(artistId)
        lt.addLast(artistList,artistEntry)
    if existsTrack == 0:
        trackEntry = newTrackEntry(trackId)
        lt.addLast(trackList,trackEntry)
    else:
        trackEntry = lt.getElement(trackList,existsTrack)
        artistEntry["repetitions"]+=1

def addToTrackMap(catalog, entry, position):
    trackMap = catalog["trackMap"]
    existsTrack = om.contains(trackMap, entry["track_id"])
    if existsTrack==True:
        userMap = me.getValue(om.get(trackMap, entry["track_id"]))
        existsUser = om.contains(userMap, entry["user_id"])
        if existsUser:
            dateMap = me.getValue(om.get(userMap, entry["user_id"]))
            om.put(dateMap,entry["created_at"],position)
        else:
            dateMap = newDateMap()
            om.put(dateMap,entry["created_at"],position)
            om.put(userMap,entry["user_id"],dateMap)
    else:
        userMap = newUserMap()
        dateMap = newDateMap()
        om.put(dateMap, entry["created_at"], position)
        om.put(userMap, entry["user_id"], dateMap)
        om.put(trackMap, ["track_id"], userMap)


# Funciones para creacion de datos

def newUserMap():
    userMap = om.newMap(omaptype="RBT")
    return userMap

def newDateMap():
    dateMap = om.newMap(omaptype="RBT")
    return dateMap

def newArtistEntry(artistId):
    entry = {"artistId": None, "repetitions": 1}
    entry["artistId"]= artistId
    return entry

def newTrackEntry(trackId):
    entry = {"trackId": None, "repetitions": 1}
    entry["trackId"]= trackId
    return entry



# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

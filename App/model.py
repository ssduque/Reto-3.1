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
                "trackMap":None}

    catalog["reps"] = lt.newList("SINGLE_LINKED")
    catalog["instrumentalnessIndex"]= om.newMap(omaptype='RBT')
    return catalog

# Funciones para agregar informacion al catalogo

def addRep(catalog, rep):
    lt.addLast(catalog["reps"], rep)
    updateInstrumentalnessIndex(catalog["instrumentalnessIndex"],rep)

def updateInstrumentalnessIndex(map, rep):
    repInstrumentalness = rep['instrumentalness']
    entry = om.get(map,repInstrumentalness)
    if (entry is None):
        dataentry = newDataEntry(rep)
        om.put(map, repInstrumentalness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addInstrumentalnessIndex(dataentry, rep)
    return map


def addInstrumentalnessIndex(dataentry, rep):
    lt.addLast(dataentry,rep)
    return dataentry

def newDataEntry(rep):
    entry = lt.newList("SINGLE_LINKED")
    return entry
   


# Funciones para creacion de datos



# Funciones de consulta

def repSize(catalog):
    return lt.size(catalog["reps"])

def indexHeight(catalog):
    return om.size(catalog["instrumentalnessIndex"])

def getInstrimentalnessByRange(catalog, minIns, maxIns):
    lst = om.values(catalog["instrumentalnessIndex"], minIns, maxIns)
    totreps = 0
    for lstrep in lt.iterator(lst):
        totreps += lt.size(lstrep)
    return totreps

# Funciones utilizadas para comparar elementos dentro de una lista


# Funciones de ordenamiento

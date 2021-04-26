"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Buscar eventos de escucha en rango de la caracteristica deseada")


def printCharacteristics():
    print("1. Instrumentalness")
    print("2. Liveness")
    print("3. Speechiness")

    print("4. Danceability")
    print("5. Valence")
    print("6. Loudness")

    print("7. Tempo")
    print("8. Acousticness")
    print("9. Energy")

catalog = {}
charList = controller.newCharList()
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()
        controller.loadEvents(catalog)
        print('Eventos cargados: ' + str(controller.repSize(catalog)))
    elif int(inputs[0]) == 2:
        printCharacteristics()
        charPos = int(input("Ingrese el numero de la caracteristica que desea buscar: "))
        bestChar = controller.getChar(charList, charPos)
        if bestChar == None:
            print("Ingrese una numero valido")
        else:
            minChar = float(input("Ingrese el minimo de "+bestChar+": "))
            maxChar = float(input("Ingrese el maximo de "+bestChar+": "))

            total = controller.getCharByRange(catalog, bestChar, minChar, maxChar)
            print("\nTotal de eventos de escucha en el rango de "+bestChar+": " + str(total))
            print('Altura del arbol: ' + str(controller.indexHeight(catalog[bestChar])))

    else:
        sys.exit(0)
sys.exit(0)

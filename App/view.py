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
    print("3- Buscar musica para festejar")
    print("4- ")
    print("5- Estudiar un genero musical")
    print("6- Buscar el genero musical mas escuchado en un rango de horas")


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

def printreq2(result):
    counter = 0
    for element1 in lt.iterator(result):
        element = lt.getElement(catalog["reps"], element1)
        print("\n El id de la pista " + str(counter)+ "es: " + element["track_id"] + "la energia es: " + element["energy"] + " y la danzabilidad es: " + element["danceability"] )
        counter = counter + 1
        if counter == 5:
            break
def printGenres():
    print("1. Reggae")
    print("2. Down-Tempo")
    print("3. Chill-out")

    print("4. Hip-hop")
    print("5. Jazz and Funk")
    print("6. Pop")

    print("7. R&B")
    print("8. Rock")
    print("9. Metal")

    print("10. Otro genero")


catalog = {}
charList = controller.newCharList()
genreList = controller.newGenreList()
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
        numArtist = controller.numArtists(catalog)
        print('Eventos cargados: ' + str(controller.repSize(catalog)))
        print("Artistas unicos: " + str(numArtist))

    elif int(inputs[0]) == 2:
        printCharacteristics()
        charPos = int(input("Ingrese el numero de la caracteristica que desea buscar: "))
        if charPos <= 0 or charPos > 9:
            print("Ingrese una numero valido")
        else:
            bestChar = controller.getChar(charList, charPos)
            minChar = float(input("Ingrese el minimo de "+bestChar+": "))
            maxChar = float(input("Ingrese el maximo de "+bestChar+": "))
            if minChar > 1.00 or minChar < -1.00 or maxChar > 1.00 or maxChar < -1.00:
                print("Ingrese un numero entre 1 y -1.")
            else:
                total = controller.getCharByRange(catalog, bestChar, minChar, maxChar)
                print("\nTotal de eventos de escucha en el rango de "+bestChar+": " + str(total[0]))
                print('Altura del arbol: ' + str(controller.indexHeight(catalog[bestChar])))

    elif int(inputs[0]) == 3:
        minCharE = float(input("Ingrese el minimo de Energia: "))
        maxCharE = float(input("Ingrese el maximo de Energia: "))
        minCharD = float(input("Ingrese el minimo de Danzabilidad: "))
        maxCharD = float(input("Ingrese el maximo de Danzabilidad: "))
        result = controller.req2(catalog, minCharE, maxCharE, minCharD, maxCharD)
        answer = lt.size(result)
        print("\nTotal de pistas unicas para festejar: " + str(answer))
        print("\nAlgunas de las pistas son: ")
        printreq2(result)
    
    elif int(inputs[0]) ==5:
        printGenres()
        genreTuple = tuple(input("Ingrese los numeros de los generos que desea buscar separados por comas: "))
        for genrePos in genreTuple:
            genrePos = int(genrePos)
            if genrePos <= 0 or genrePos > 10:
                print("Ingrese una numero valido")
            elif genrePos !=10:
                tempoRange = controller.getGenre(genreList,genrePos)
                genre = tempoRange[2]
                minTempo = tempoRange[0]
                maxTempo = tempoRange[1]
                total = controller.getCharByRange(catalog,"tempo",minTempo,maxTempo)
                print("Para "+str(genre)+" el tempo esta entre "+str(minTempo)+" y "+str(maxTempo)+" BPM...")
                print("\nEl numero de reproducciones para este genero fueron: "+str(total[0]))
            elif genrePos == 10:
                genre = input("Ingrese el nombre del nuevo genero: ")
                minTempo = float(input("Ingrese el valor minimo del tempo: "))
                maxTempo = float(input("Ingrese el valor maximo del tempo: "))
                total = controller.getCharByRange(catalog,"tempo",minTempo,maxTempo)
                print("Para "+str(genre)+" el tempo esta entre "+str(minTempo)+" y "+str(maxTempo)+" BPM...")
                print("\nEl numero de reproducciones para este genero fueron: "+str(total[0]))
    
    elif int(inputs[0]) == 6:
        initialTime = input("Ingrese la hora desde la que desea buscar (H:M:S): ")
        finalTime = input("Ingrese la hora desde la que desea buscar (H:M:S): ")
        result = controller.req5(catalog, initialTime, finalTime)
        print(result)
        

    else:
        sys.exit(0)
sys.exit(0)

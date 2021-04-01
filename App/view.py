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

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Funciones para la impresión de resultados


def printResults(ord_videos, sample):
    """"
    La función de printResults() nos permite imprimir
    los videos según el tamaño del sample
    la usamos para la impresión del primer
    video en la carga del catálogo y para mostrar los
    resultados del primer requerimiento
    """
    size = lt.size(ord_videos)
    if size > sample:
        print("Los primeros ", sample, " videos ordenados son:")
        i = 1
        while i <= sample:
            video = lt.getElement(ord_videos, i)
            print("\n")
            print(
                'Título: ' + str(video.get('title')) + ", " +
                'Nombre del canal: ' + str(video.get('channel_title')) + ", " +
                'Fue tendencia el día: ' + str(video.get('trending_date'))
                + ", " +
                'Visitas: ' + str(video.get('views')) + ", " +
                'Likes: ' + str(video.get('likes')) + ", " +
                'Dislikes: ' + str(video.get('dislikes')) + ", " +
                'Fecha de publicación: ' + str(video.get('dislikes')))
            i += 1


def printResultsv2(ord_videos, sample):
    printlist = []
    i = 1
    while len(printlist) <= (sample - 1):
        element = lt.getElement(ord_videos, i)
        title = str(element.get('title'))
        if title not in printlist:
            printlist.append(title)
            print("\n")
            print(
                'Título: ' + str(element.get('title')) + ", " +
                'Nombre del canal: ' + str(element.get('channel_title'))
                + ", " + 'Visitas: ' + str(element.get('views')) + ", " +
                'Likes: ' + str(element.get('likes')) + ", " +
                'Dislikes: ' + str(element.get('dislikes')) + ", " +
                'Tags: ' + str(element.get('tags')))
        i += 1


def printResultsv3(result):
    print(
            'Título: ' + str(result[0].get('title')) + ", " +
            'Nombre del canal: ' + str(result[0].get('channel_title')) + ", " +
            'País: ' + str(result[0].get('country')) + ", " +
            'No. de días trending: ' + str(result[1]))


# Menu de opciones


def printMenu():
    """
    La función de PrintMenu() Muestra las cinco opciones que tiene el
    usuario para la busqueda de Videos según los requerimientos
    """
    print("\n_______________________________________________________________")
    print("Bienvenido")
    print("1- Inicializar catálogo")
    print("2- Cargar información en el catálogo")
    print(
        "3- Conocer cuáles son los n videos con más views que son "
        + " tendencia en un país, dada una categoría específica."
        )
    print(
        "4- Conocer cuál es el video que más días ha sido" +
        " trending para un país específico.")
    print(
        "5- Cuál es el video que más días ha sido" +
        " trending para una categoría específica.")
    print(
        "6- Conocer cuáles son los n videos diferentes con" +
        " más likes en un país con un tag específico.")
    print("0- Salir")


# Funciones de inicialización


def initCatalog(list_type):
    """
    La función initCatalog() Inicializa el catalogo de Videos
    retornando la función correspondiente del controller
    """
    return controller.initCatalog(list_type)


def loadData(catalog):
    """
    La función LoadData() carga el catalogo de Videos en la
    estructura de datos escogida retornando la función
    correspondiente del controller
    """
    controller.loadData(catalog)


# Menu principal

while True:
    printMenu()
    print('\n')
    inputs = input('Seleccione una opción para continuar: ')

    if int(inputs[0]) == 1:
        correct = True
        while correct:
            print(
                'Ingrese el tipo de mapa a utilizar. Digite 1 si desea' +
                ' PROBING, digite 2 si desea CHAINING.')
            map_type_inp = int(input(''))
            if map_type_inp == 1:
                map_type = 'PROBING'
                correct = False
                break
            elif map_type_inp == 2:
                map_type = 'CHAINING'
                correct = False
                break
            else:
                print('Digite un número válido.')
        print(
            'Ingrese el factor de carga. ' +
            '(Utilice el punto como separador decimal): ')
        load_factor = float(
            input(''))
        print("Inicializando Catálogo ....")
        x = controller.initCatalog(map_type, load_factor)

    elif str(inputs[0]) == "2":
        print("\nCargando información de los archivos ....")
        answer = controller.loadData(x)
        print('Videos cargados: ' + str(controller.videosSize(x)))
        print('Categorías cargadas: ' + str(controller.categoriesSize(x)))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")

    elif str(inputs[0]) == "3":
        pais = input("\nIngrese el país de referencia: ")
        categoria = int(input('Ingrese la categoría de referencia: '))
        n = input("Ingrese el número de videos que desea imprimir: ")
        print("\nCargando ....")
        result = controller.getVideosByCategoryAndCountry(x, categoria, pais)
        printResults(result[1], int(n))

    elif str(inputs[0]) == "4":
        pais = input("Ingrese el país de referencia: ")
        print("\nCargando ....")
        videos_filtrados = controller.getVideosByCountry(x, pais)
        result = controller.getMostTrendingDaysByID(videos_filtrados.get(
            'videos'))
        printResultsv3(result)

    elif str(inputs[0]) == "5":
        categoria = int(input('Ingrese la categoría de referencia: '))
        print("\nCargando ....")

    elif str(inputs[0]) == "6":
        pais = input("Ingrese el país de referencia: ")
        tag = input('Ingrese el tag de referencia: ')
        n = int(input("Ingrese el número de videos que desea imprimir: "))
        print("\nCargando ....")

    elif str(inputs[0]) == "0":
        sys.exit(0)

    else:
        print("\n")
        print("Opción No Válida")

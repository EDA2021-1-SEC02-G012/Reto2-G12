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
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.DataStructures import mapentry as me
import time
assert cf

"""
Se define la estructura de un catálogo de videos.
El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog(map_type, load_factor):
    """ Inicializa el catálogo de videos

    Crea una lista vacia para guardar todos los videos

    Se crean indices (Maps) por los siguientes criterios:
    Título
    Nombre del canal
    Categoría
    Tags
    Views
    Likes

    Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'category_id': None,
               'category': None}

    """
    Esta lista contiene todo los videos encontrados
    en los archivos de carga.  Estos videos no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['videos'] = lt.newList('SINGLE_LINKED')

    """
    Esta lista contiene las categorías
    """
    catalog['category_id'] = lt.newList('SINGLE_LINKED')

    """
    A continuación se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los videos de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es la categoría del video
    """
    catalog['category'] = mp.newMap(
        40,
        maptype=map_type,
        loadfactor=load_factor)

    """
    Este indice crea un map cuya llave es el país del video
    """
    catalog['country'] = mp.newMap(
        20,
        maptype=map_type,
        loadfactor=load_factor)

    return catalog


# Funciones para creacion de datos


def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    addCategoryFORMAP(catalog, video['category_id'], video)
    addCountryFORMAP(catalog, video['country'], video)


def addCategory(catalog, category):
    """
    La función de addCategory() adiciona una categoría a la
    lista de categorías
    """
    c = newCategory(category)
    lt.addLast(catalog['category_id'], c)


def addCategoryFORMAP(catalog, c_id, video):
    categories = catalog['category']
    existcategory = mp.contains(categories, c_id)
    if existcategory:
        entry = mp.get(categories, c_id)
        category = me.getValue(entry)
    else:
        category = newCategory(c_id)
        mp.put(categories, c_id, category)
    lt.addLast(category['videos'], video)


def addCountryFORMAP(catalog, country_name, video):
    countries = catalog['country']
    existcountry = mp.contains(countries, country_name)
    if existcountry:
        entry = mp.get(countries, country_name)
        country = me.getValue(entry)
    else:
        country = newCountry(country_name)
        mp.put(countries, country_name, country)
    lt.addLast(country['videos'], video)


def newCategory(c_id):
    category = {"c_id": "", "videos": None}
    category['c_id'] = c_id
    category['videos'] = lt.newList('ARRAY_LIST', None)
    return category


def newCountry(country_name):
    """
    La función de newCountry() crea una nueva estructura para
    modelar los videos a partir de los paises
    """
    country = {'country_name': "", "videos": None}
    country['country_name'] = country_name
    country['videos'] = lt.newList('ARRAY_LIST', None)
    return country


# Funciones para agregar informacion al catalogo

# Funciones de consulta

def getVideosByCriteriaList(catalog, criteria, x):
    """
    La función de getVideosByCriteriaList() filtra los videos por un
    criterio específico dado un x. El catálogo debe ser una lista.
    """
    listaretorno = lt.newList("ARRAY_LIST")
    for element in lt.iterator(catalog):
        nombre_pais = element.get(criteria)
        if nombre_pais == x:
            lt.addLast(listaretorno, element)

    return listaretorno


def getVideosByCriteriaMap(catalog, criteria, key):
    """
    La función de getVideosByCriteriaMap() filtra los videos por un
    criterio específico dado un x. El catálogo debe ser un mapa.
    """
    values = catalog[criteria]
    entry = mp.get(values, str(key))
    result = me.getValue(entry)
    return result


def getVideosByCategoryAndCountry(catalog, category, country):
    sublist = getVideosByCriteriaMap(
        catalog, 'category', category).get('videos')
    sublist2 = getVideosByCriteriaList(sublist, 'country', country)
    return sortVideos(sublist2, lt.size(sublist2), ms, cmpVideosByViews)


def getMostTrendingDaysByTitle(videos):
    ids = {}
    pos = {}
    i = 1

    while i <= lt.size(videos):
        video_id = lt.getElement(videos, i).get('video_id')

        if video_id in ids:
            ids[video_id] += 1
        else:
            ids[video_id] = 1
            pos[video_id] = i
        i += 1

    video = max(ids, key=ids.get)
    result = lt.getElement(videos, pos[video]) 

    return (result, ids[video])


def videosSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['videos'])


def categoriesSize(catalog):
    """
    Numero de autores en el catalogo
    """
    return mp.size(catalog['category'])


# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByViews(video1, video2) -> bool:
    """
    La función de cmpVideosbyViews() retorna True or False si las visitas
    de un video son mayores o menores a las visitas de otro video
    """
    return (float(video1['views']) > float(video2['views']))

# Funciones de ordenamiento


def sortVideos(catalog, size, sort_type, cmp):
    """
    La Función sortVideos() la usamos en varios requerimientos por la necesidad
    de tener la información organizada. Por esto mismo, la función cuenta con
    cuatro parámetros en donde destacan "cmp" y "sort_type". Para cada caso
    particular, dejamos que según estos dos parámetros se invoque la función
    correspondiente de la librería sort y usando los algoritmos de merge sort
    y quick sort
    """
    sub_list = lt.subList(catalog, 0, size)
    sub_list = sub_list.copy()
    start_time = time.process_time()

    sorted_list = ms.sort(sub_list, cmp)

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

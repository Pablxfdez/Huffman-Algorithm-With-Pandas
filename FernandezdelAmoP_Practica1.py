"""
Práctica 1. Código de Huffmann y Teorema de Shannon
"""

import os
import numpy as np
import pandas as pd
import math 
#### Vamos al directorio de trabajo
os.getcwd()
#os.chdir('D:\Documents\MATEMÁTICAS UCM\4º MATEMÁTICAS 22-23\2 CUATRI\GEOMETRÍA COMPUTACIONAL\Practicas\Practica 1')
#files = os.listdir('D:\Documents\MATEMÁTICAS UCM\4º MATEMÁTICAS 22-23\2 CUATRI\GEOMETRÍA COMPUTACIONAL\Practicas\Practica 1')

with open('GCOM2023_pract1_auxiliar_eng.txt', 'r',encoding="utf8") as file: #r sirve para leer, si quiero escribir es w. el encoding es siempre el mismo
      en = file.read()
     
with open('GCOM2023_pract1_auxiliar_esp.txt', 'r',encoding="utf8") as file:
      es = file.read()


#### Contamos cuantos caracteres hay en cada texto
from collections import Counter
tab_en = Counter(en)
tab_es = Counter(es)
#Aquí modificamos la plantilla para tener también una codificación de los caracteres que pertenecen al lenguaje pero no aparecen en el texto
SEng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '?', '-', '\n', ',', '”','“', '(',  ')', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SEsp = ['a', 'á', 'b', 'c', 'd', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'ó', 'p', 'q', 'r', 's', 't', 'u', 'ú', 'ü', 'v', 'w', 'x', 'y', 'z', 'A', 'Á', 'B', 'C', 'D', 'E', 'É', 'F', 'G', 'H', 'I', 'Í', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'Ó', 'P', 'Q', 'R', 'S', 'T', 'U', 'Ú', 'Ü', 'V', 'W', 'X', 'Y', 'Z', '¡', '!', '¿', '?', '-', '\n', ',','”','“', '(',  ')', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for char in SEng:
    if char not in list(tab_en.keys()):
        tab_en[char] = 0  #los añadimos con frecuencia 0 ya que no aparecen en el texto
for char in SEsp:
    if char not in list(tab_es.keys()):
        tab_es[char] = 0  #los añadimos con frecuencia 0 ya que no aparecen en el texto

#### Transformamos en formato array de los carácteres (states) y su frecuencia
#### Finalmente realizamos un DataFrame con Pandas y ordenamos con 'sort'
tab_en_states = np.array(list(tab_en)) #array con las claves. List de un diccionario sacauna lista con las claves
tab_en_weights = np.array(list(tab_en.values())) #array con las frecuencias
tab_en_probab = tab_en_weights/float(np.sum(tab_en_weights))
distr_en = pd.DataFrame({'states': tab_en_states, 'probab': tab_en_probab})
distr_en = distr_en.sort_values(by='probab', ascending=True)
distr_en.index=np.arange(0,len(tab_en_states))

tab_es_states = np.array(list(tab_es))
tab_es_weights = np.array(list(tab_es.values()))
tab_es_probab = tab_es_weights/float(np.sum(tab_es_weights))
distr_es = pd.DataFrame({'states': tab_es_states, 'probab': tab_es_probab })
distr_es = distr_es.sort_values(by='probab', ascending=True)
distr_es.index=np.arange(0,len(tab_es_states))

##### Para obtener una rama, fusionamos los dos states con menor frecuencia
distr = distr_en
''.join(distr['states'][[0,1]]) 

### Es decir:
states = np.array(distr['states'])
probab = np.array(distr['probab'])
state_new = np.array([''.join(states[[0,1]])])   #Ojo con: state_new.ndim
probab_new = np.array([np.sum(probab[[0,1]])])   #Ojo con: probab_new.ndim
codigo = np.array([{states[0]: 0, states[1]: 1}])
states =  np.concatenate((states[np.arange(2,len(states))], state_new), axis=0)
probab =  np.concatenate((probab[np.arange(2,len(probab))], probab_new), axis=0)
distr = pd.DataFrame({'states': states, 'probab': probab, })
distr = distr.sort_values(by='probab', ascending=True)
distr.index=np.arange(0,len(states))

#Creamos un diccionario
branch = {'distr':distr, 'codigo':codigo}

## Ahora definimos una función que haga exáctamente lo mismo
def huffman_branch(distr):
    states = np.array(distr['states'])
    probab = np.array(distr['probab'])
    state_new = np.array([''.join(states[[0,1]])])
    probab_new = np.array([np.sum(probab[[0,1]])])
    codigo = np.array([{states[0]: 0, states[1]: 1}])
    states =  np.concatenate((states[np.arange(2,len(states))], state_new), axis=0)
    probab =  np.concatenate((probab[np.arange(2,len(probab))], probab_new), axis=0)
    distr = pd.DataFrame({'states': states, 'probab': probab})
    distr = distr.sort_values(by='probab', ascending=True)
    distr.index=np.arange(0,len(states))
    branch = {'distr':distr, 'codigo':codigo}
    return(branch) 

def huffman_tree(distr):
    tree = np.array([])
    while len(distr) > 1:
        branch = huffman_branch(distr)
        distr = branch['distr']
        code = np.array([branch['codigo']])
        tree = np.concatenate((tree, code), axis=None)
    return(tree)
#obtenemos los árboles de huffman asociados al texto en ingés y español
tree_en = huffman_tree(distr_en)
tree_es= huffman_tree(distr_es)

#Esta función recibe un árbol de huffman y devuelve la tabla de códigos, es deicr, un diccionario donde las claves con los caracteres y los valores su codificación de Huffman
def tabla_codigos(tree):
    tabla = {}
    for par in tree:
        for item in par.items():
            if len(item[0])==1 :
                tabla[item[0]]=str(item[1])
            else:
                for i in item[0] :
                    tabla[i]= str(item[1])+tabla[i] 
    return tabla

#Guardamos las tablas asociadas a cada árbol en las siguientes variables:
tabla_en= tabla_codigos(tree_en)
tabla_es= tabla_codigos(tree_es)

# A continuación, definimos dos funciones que reciben como entrada un string y devuelven la codificación asociada al inglés o al español de este, codificar_en y codificar_es respectivamente 
def codificar_en(texto):
    codigo=''
    for i in texto:
        codigo+=tabla_en[i]
    return codigo

def codificar_es(texto):
    codigo=''
    for i in texto:
        codigo+=tabla_es[i]
    return codigo

#Para decodificar un código de Huffman, independientemente de que sea el código de un caracter o un texto, aplicaremo sun procedimiento estudiado en Estructuras de Datos
# Básicamente, como para cada char su prefijo es único ( base de la codificación de huffman), por cada digito que leemos de código (1 o 0), hacemos un filtro en nuestra tabla de códigos.
#Es decir, que si leemos un 1 como caracter inicial, descartaremos de nuestra tabla todos aquellos caracteres cuya codificación empiece por 0.
# Si en vez de estar en el primer dígito estamos en el dígito n, aplicaremos el mismo razonamiento, eliminando aquellos caracteres cuyo código tiene longitud menor a n.
# Al iterar sobre el código input, nuestro diccionario tendrá en un momento tamaño uno. Ahí añadmios al resultado la única clave que hay y reseteamos el diccionario, continuando con el algoritmo hasta llegar al final del código input.
# Primero para el texto en inglés y a continuación para en castellano.

def decodificar_en(codigo):
    aux=tabla_en.copy() #Como los diccionarios son mutables, creamos copia para no modificar nuestra tabla de códigos
    n=0  #Vamos almacenando la longitud del código asociado al char que estamos intentando encontrar, cuando encontramos un char cuyo código equivale al leído, reseteamos a 0 y volvemos a realizar el proceso
    resultado=''
    for i in codigo:
        lista_elim=[] #Como no podemos iterar sobre un diccionario al que modificamos su tamaño, me creo una lista con los claves que hay que eliminar
        for j in aux:
            if len(tabla_en[j])<=n:
                lista_elim.append(j)  #Si el código asociado a un caracter es más corto que la longitud de código que llevamos (sin decodificar e iterada), hay que eliminarlo
            else:
                if tabla_en[j][n]!=i:  #Si el dígito de código leído no corresponde al dígito del código asociado a una clave para la misma posición, hay que eliminarlo.
                 lista_elim.append(j)
        for k in lista_elim:
            del aux[k]
        n+=1 #Aumentamos en 1 la posición del código que estamos leyendo
        if len(aux)==1:   #Cuando solo queda una clave en el diccionario, esta es la buscada, así que la concatenamos a resultado y reseteamos para continuar el proceso
            resultado+=list(aux.keys())[0]
            aux=tabla_en.copy()
            n=0        
    return resultado

def decodificar_es(codigo):
    aux=tabla_es.copy()
    n=0
    resultado=''
    for i in codigo:
        lista_elim=[]
        for j in aux:
            if len(tabla_en[j])<=n:
                lista_elim.append(j)
            else:
                if tabla_es[j][n]!=i:
                 lista_elim.append(j)
        for k in lista_elim:
            del aux[k]
        n+=1
        if len(aux)==1:
            resultado+=list(aux.keys())[0]
            aux=tabla_es.copy()
            n=0        
    return resultado

# Función que recibe un texto y lo convierte a binario trivial.
def text_a_binario(texto):
    result = ' '.join(format(ord(c), 'b') for c in texto)
    return result


# EJERCICIO 2
print('EJERCICIO 1:\n A partir de las muestras dadas, hallar el código Huffman binario de SEng y SEsp, y sus longitudes medias L(SEng) y L(SEsp). Comprobar que se satisface el Primer Teorema de Shannon \n')
#Imprimimos ambas tablas de códigos
print(f'La tabla de códigos de SEng es:\n')
for item in tabla_en.items():   
    print(f'{item[0]} : {item[1]}')


print(f'La tabla de códigos de SEsp es:\n')
for item in tabla_en.items():
    print(f'{item[0]} : {item[1]}')
 


long_media_en=0
entropia_en=0
long_media_es=0
entropia_es=0
for indice_fila, valor_fila in distr_en[distr_en['probab']!=0].iterrows():
    long_media_en += len(tabla_en[valor_fila['states']])*valor_fila['probab'] #Calculamos longitudes medias con la fórmula vista en clase
    entropia_en-=valor_fila['probab']*math.log2(valor_fila['probab'])
for indice_fila, valor_fila in distr_es[distr_es['probab']!=0].iterrows():
    long_media_es += len(tabla_es[valor_fila['states']])*valor_fila['probab']   
    entropia_es-=valor_fila['probab']*math.log2(valor_fila['probab'])

print(f'\nLa longitud media de SEng, L(SEng), es igual a {long_media_en}; y su entropía, H(SEng); es igual a {entropia_en}')
print(f'La longitud media de SEsp, L(SEsp), es igual a {long_media_es}; y su entropía, H(SEsp), es igual a {entropia_es}')

print('\nEntonces, para ambos alfabetos el Primer Teorema de Shannon se cumple, ya que H(i) <= L(i) < H(i)+1; con i SEng o SEsp')


#EJERCICIO 2:
print('\n\nEJERCICIO 2:\n Utilizando los códigos obtenidos en el apartado anterior, codificar la palabra cognada X =“dimension” para ambas lenguas. Comprobar la eficiencia de longitud frente al código binario usual. \n')

dimension_en=codificar_en('dimension')
dimension_es=codificar_es('dimension')
dimension_bin=text_a_binario('dimension')
print('La palabra dimension codificada para el ingles es:', dimension_en)
print('La palabra dimension codificada para el español es:', dimension_es)
print('La palabra dimension codificada en binario es:', dimension_bin)
print(f'\nPor tanto, la longitud de la cadena utilizando el código binario es {len(dimension_bin)/len(dimension_en)} mayor que utilizando Huffman')


#EJERCICIO 3:
print('\n\nEJERCICIO 3:\n Utilizando los códigos obtenidos en el apartado anterior, codificar la palabra cognada X =“dimension” para ambas lenguas. Comprobar la eficiencia de longitud frente al código binario usual. \n')

print('Decodificando 0101010001100111001101111000101111110101010001110 del inglés se obtiene la palabra:', decodificar_en('0101010001100111001101111000101111110101010001110'))







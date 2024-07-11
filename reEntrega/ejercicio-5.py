def leer_textos(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        textos = [linea.strip().upper() for linea in archivo]
    return textos

def escribir_resultado(nombre_archivo_salida, texto, distancia_maxima):
    with open(nombre_archivo_salida, 'w') as archivo:
        archivo.write(f'{texto}\n')
        archivo.write(f'{distancia_maxima}\n')

import random
from collections import Counter

def distancia(a, b):
    change = 0
    n = len(a)

    for i in range(1, n + 1):
        if a[i - 1] != b[i - 1]:
            change += 1
    
    return change

def texto_mas_equilibrado_aleatorio(textos):
    # Inicializar el texto resultado
    texto_resultado = []
    
    # La longitud de los textos es igual, así que tomamos la longitud del primer texto
    longitud_texto = len(textos[0])

    # Inicializar el Counter
    contador = Counter()
 
    # Iterar sobre cada posición en los textos
    for i in range(longitud_texto):

        # Evaluar el impacto de cada carácter en la posición i
        mejor_caracter = None
        menor_distancia_maxima = float('inf')
        
        caracteres_recorridos_por_columna = set()

        caracteres = []

        #candidatos = []

        for texto in textos:

            caracter = texto[i]

            #contador[caracter] += 1

            caracteres.append(caracter) 

            if caracter not in caracteres_recorridos_por_columna:
                
                #contador[caracter] += 1

                for texto in textos:

                    # Generar un texto candidato con el caracter en la posición i
                    texto_candidato = texto_resultado + [caracter] + [texto[j] for j in range(i + 1, longitud_texto)]

                    # Calcular la distancia para cada texto con el texto candidato
                    distancias = [distancia(texto_candidato, texto) for texto in textos]

                    distancia_maxima = max(distancias)
                
                    if distancia_maxima < menor_distancia_maxima:
                        menor_distancia_maxima = distancia_maxima
                        mejor_caracter = caracter
                        #candidatos.append((caracter, distancia_maxima))
                        #contador[caracter] += 1

                caracteres_recorridos_por_columna.update(caracter)

        
        contador = Counter(caracteres)

        # Decidir si usar el mejor carácter o uno al azar
        numero_azar = random.random()
        if numero_azar < 1/len(textos):

            # Obtener los valores en orden ascendente de frecuencia
            #valores_ordenados = sorted(contador.items(), key=lambda item: item[1])
            # Seleccionar un carácter al azar de acuerdo al porcentaje de frecuencia de aparición
            #for caracter, conteo in valores_ordenados:
            #    if numero_azar < conteo/(len(textos)*len(textos[0])):
            #        mejor_caracter = caracter
            #        break

            # Recorrer los valores en orden ascendente de frecuencia
            for i in range(1, len(contador) + 1):
                frecuencia = contador.most_common(i)[0][1]
                print("frecuencia ", frecuencia)
                # Seleccionar un carácter al azar de acuerdo al porcentaje de frecuencia de aparición
                if numero_azar < frecuencia/(len(textos)):
                    mejor_caracter = contador.most_common(i)[0][0]
                    print("mejor_caracter ", mejor_caracter)

        # Añadir el carácter seleccionado al texto resultado
        texto_resultado.append(mejor_caracter)
    
    # Unir la lista de caracteres en un solo texto
    texto_resultado = ''.join(texto_resultado)
    
    return texto_resultado

def generar_vecinos(texto):
    vecinos = set()
    longitud_texto = len(texto)
    letras = set(texto.upper())
    
    for i in range(longitud_texto):
        for letra in letras:
            if texto[i].upper() != letra.upper():
                vecino = texto[:i] + letra + texto[i+1:]
                vecinos .add(vecino)
    
    return vecinos

def texto_mas_equilibrado_busqueda_local(textos, max_iter, mejor_distancia_maxima_global, vecinos_recorridos):
    texto_actual = texto_mas_equilibrado_aleatorio(textos)
    mejor_texto = texto_actual
    mejor_distancia_maxima = mejor_distancia_maxima_global
    counter = 0
    
    for _ in range(max_iter):
        vecinos = generar_vecinos(texto_actual)
        vecinosARecorrer = vecinos - vecinos_recorridos
        mejor_vecino = None
        
        for vecino in vecinosARecorrer:
            distancias = [distancia(vecino, texto) for texto in textos]
            distancia_maxima = max(distancias)
            
            if distancia_maxima < mejor_distancia_maxima:
                print("vecino: ", vecino, distancia_maxima)
                mejor_distancia_maxima = distancia_maxima
                mejor_vecino = vecino
                counter = 0
            else:
                # Vamos acumulando la cantidad de iteraciones en las cuales la distancia no mejora
                counter += 1
        
        vecinos_recorridos.update(vecinosARecorrer)
        
        if mejor_vecino is None:
            print("No hay mejor vecino, se alcanza un optimo local")
            break

        if counter > max_iter/2:
            # Si a esta altura de las iteraciones la distancia no mejora, salgo de la busqueda 
            break

        texto_actual = mejor_vecino
        mejor_texto = mejor_vecino
    
    return mejor_texto, mejor_distancia_maxima, vecinos_recorridos

def grasp(textos, max_iter):
    mejor_texto_global = None
    mejor_distancia_maxima_global = float('inf')
    vecinos_recorridos = set()
    counter = 0
    
    # Flag para indicar que la distancia_maxima cambia seguido
    flag_iter = True

    for _ in range(max_iter):
        texto_mejorado, distancia_maxima, vecinos = texto_mas_equilibrado_busqueda_local(textos,max_iter, mejor_distancia_maxima_global, vecinos_recorridos)
        
        if distancia_maxima < mejor_distancia_maxima_global:
            mejor_distancia_maxima_global = distancia_maxima
            mejor_texto_global = texto_mejorado
            if flag_iter:
                counter = 0
            else:
                flag_iter = True
        else:
            # Vamos acumulando la cantidad de iteraciones en las cuales la distancia no mejora
            counter += 1
            flag_iter = False

        vecinos_recorridos.update(vecinos)

        # Si la cantidad de iteraciones en las cuales la distancia no mejora es 1000, salimos de las iteraciones
        if counter > max_iter/2:
            break
    
    return mejor_texto_global, mejor_distancia_maxima_global

def main(nombre_archivo_entrada, nombre_archivo_salida):
    textos = leer_textos(nombre_archivo_entrada)
    mejor_texto, mejor_distancia_maxima = grasp(textos, len(textos)*len(textos[0]))
    escribir_resultado(nombre_archivo_salida, mejor_texto, mejor_distancia_maxima)

# Ejemplo de uso
#nombre_archivo_entrada = 'textos_entrada.txt'
#nombre_archivo_salida = 'resultado_salida.txt'
nombre_archivo_entrada='texto_mas_parecido_20_300_1.txt'
nombre_archivo_salida = 'texto_mas_parecido_20_300_1_resultado.txt'
main(nombre_archivo_entrada, nombre_archivo_salida)

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

# Ejemplo de uso
#textos = ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE"] # Ejemplo donde demuestra que el greedy no es optimo
textos = ["ABBAC", "BBAAC", "CBAAB", "ABCAA", "ACCCC", "BCACB"]
texto_generado = texto_mas_equilibrado_aleatorio(textos)
print(f'El texto mas parecido generado es: "{texto_generado}".')

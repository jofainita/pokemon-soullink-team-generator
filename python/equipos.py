from itertools import combinations
from itertools import permutations
import numpy as np
import pandas as pd 
   
def sacar_combinaciones(tipos):
    # combinaciones = pd.DataFrame(columns=['Tipo1','Tipo2','num','compatibles'])
    combinaciones = tipos.drop_duplicates(subset='num', keep='first')
    combinaciones = combinaciones.reset_index(drop=True)
    combinaciones['compatibles'] = 0
    combinaciones['incompatibles'] = 0
    combinaciones['compatibles'] = combinaciones['compatibles'].astype('object')
    combinaciones['incompatibles'] = combinaciones['incompatibles'].astype('object')
    for i in range (len(combinaciones)):
        # seria_actual = combinaciones.iloc[i]
        combinaciones_compatibles = combinaciones[combinaciones['Tipo1'] != combinaciones['Tipo1'][i]].copy()
        combinaciones_compatibles = combinaciones_compatibles[combinaciones_compatibles['Tipo2'] != combinaciones['Tipo1'][i]].copy()
        combinaciones_compatibles = combinaciones_compatibles[combinaciones_compatibles['Tipo1'] != combinaciones['Tipo2'][i]].copy()
        combinaciones_compatibles = combinaciones_compatibles[combinaciones_compatibles['Tipo2'] != combinaciones['Tipo2'][i]].copy()
        combinaciones['compatibles'][i] = combinaciones_compatibles['num'].tolist()
        combinaciones_not_compatibles = np.setdiff1d(combinaciones['num'].tolist(), combinaciones['compatibles'][i])
        combinaciones['incompatibles'][i] = combinaciones_not_compatibles.tolist()
    return combinaciones

def common_elements(list1, list2):
    return [element for element in list1 if element in list2]

def sacar_tipos(tipos):
    tipos['num'] = 0
    contador = 1
    for i in range (len(tipos)):
        for j in range (len(tipos)):
            if tipos['num'][i] == 0:
                tipos['num'][i] = contador
                contador += 1
            tipo1_aux = tipos['Tipo1'][i]
            tipo2_aux = tipos['Tipo2'][i]
            if (tipo1_aux == tipos['Tipo1'][j] and tipo2_aux == tipos['Tipo2'][j]) or (tipo1_aux == tipos['Tipo2'][j] and tipo2_aux == tipos['Tipo1'][j]):
                tipos['num'][j] = tipos['num'][i]
    return tipos

# Demasiaado lento
#def sacar_todas_combinaciones(combinaciones, todas_combinaciones):
#    n_prueba = 0
#    hechos = []
#    for n_prueba in range (len(combinaciones)):
#        n = combinaciones['num'][n_prueba]
#        posibles_actuales = combinaciones['compatibles'][n_prueba]
#        posibles_actuales = list(set(posibles_actuales) - set(hechos))
#        posibles_combinaciones = permutations(posibles_actuales)
#        for i in posibles_combinaciones:
#            lista_aux = list(i)
#            actual_final_list = lista_aux.copy()
#            for j in lista_aux:
#                if j in actual_final_list:
#                    set_aux = set(actual_final_list)
#                    incompatible_list_aux = combinaciones[combinaciones['num'] == j]['incompatibles'].tolist()
#                    incompatible_list_aux_sin_numero = incompatible_list_aux[0].copy()
#                    incompatible_list_aux_sin_numero.remove(j)
#                    set_comparar = set(incompatible_list_aux_sin_numero)
#                    actual_final_list= list(set_aux - set_comparar)                   
#                else:
#                    pass
#            actual_final_list.append(combinaciones['num'][n_prueba])
#            actual_final_list.sort()
#            print (i)
#            if actual_final_list not in todas_combinaciones:
#                todas_combinaciones.append(actual_final_list)
#                print (todas_combinaciones)
#                print (i)
#        hechos.append(n)
#            #print(str(n_prueba) + '_' + str(len(posibles_combinaciones)))
#    return todas_combinaciones
#

def sacar_todas_combinaciones(combinaciones, todas_combinaciones):
    iterador = 0
    for n in range (len(combinaciones)):
        n = combinaciones['num'][iterador]
        compatibles_base = combinaciones['compatibles'][iterador]
        for i in range (len(compatibles_base)):
            list_aux = compatibles_base.copy()
            list_aux.insert(0, list_aux.pop(i))
            for j in list_aux:
                if j in list_aux:
                    set_aux = set(list_aux)
                    incompatible_list_aux = combinaciones[combinaciones['num'] == j]['incompatibles'].tolist()
                    incompatible_list_aux_sin_numero = incompatible_list_aux[0].copy()
                    incompatible_list_aux_sin_numero.remove(j)
                    set_comparar = set(incompatible_list_aux_sin_numero)
                    list_aux= list(set_aux - set_comparar)
                else:
                    pass
            list_aux.append(combinaciones['num'][iterador])
            list_aux.sort()
            if list_aux not in todas_combinaciones:
                todas_combinaciones.append(list_aux)
        iterador += 1
    return todas_combinaciones


def main():
    pokimones = pd.read_table('Bocatacas.tsv')
    entrenador1 = pd.DataFrame(columns=['Ruta','Pokemon','Tipo'])
    entrenador2 = pd.DataFrame(columns=['Ruta','Pokemon','Tipo']) 
    entrenador1[['Ruta','Pokemon','Tipo']] = pokimones[['Localizacion', 'Pokemon_', 'Tipo_']].copy()
    entrenador2[['Ruta','Pokemon','Tipo']] = pokimones[['Localizacion', 'Pokemon', 'Tipo']].copy()
    tipos = pd.DataFrame(columns=['Tipo1','Tipo2','num'])
    tipos['Tipo1']= entrenador1['Tipo'].copy()
    tipos['Tipo2']= entrenador2['Tipo'].copy()
    tipos = tipos[tipos['Tipo1'] != tipos['Tipo2']]
    tipos = tipos.reset_index(drop=True)
    tipos = sacar_tipos(tipos)
    combinaciones = sacar_combinaciones(tipos)
    todas_combinaciones = []
    todas_combinaciones = sacar_todas_combinaciones(combinaciones, todas_combinaciones)
    for i in todas_combinaciones:
        print (i)
    todas_combinaciones_df = pd.DataFrame(todas_combinaciones)
    todas_combinaciones_df.to_excel('todas_combinaciones.xlsx')
    

if __name__ == "__main__":
    main()

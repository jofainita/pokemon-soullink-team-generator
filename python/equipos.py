from itertools import combinations
from itertools import permutations
import numpy as np
import pandas as pd 
import sqlite3
from sqlite3 import Error as sqlite3Error
import json
   
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
        combinaciones['incompatibles'][i] = combinaciones_not_compatibles.tolist().copy()
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

def connect_to_db():
    try:
        conn = sqlite3.connect('/home/jofa/Documents/pokimones/pokemon-soullink-team-generator/PokeTeamViewer/poke_database.db')
    except sqlite3Error as e:
        print(e)
    return conn

def create_tables(conn):
    table1 = """ CREATE TABLE IF NOT EXISTS Datos_base (
                                        id integer PRIMARY KEY,
                                        Ruta text NOT NULL,
                                        Pokemon_1 text NOT NULL,
                                        Mote_1 text NOT NULL,
                                        Tipo_1 text NOT NULL,
                                        Pokemon_2 text NOT NULL,
                                        Mote_2 text NOT NULL,
                                        Tipo_2 text NOT NULL,
                                        Id_Tipo integer NOT NULL
                                        ); """
    
    table2 = """ CREATE TABLE IF NOT EXISTS Asociacion_tipos (
                                        id integer PRIMARY KEY,
                                        Tipo_1 text NOT NULL,
                                        Tipo_2 text NOT NULL,
                                        Id_Tipo integer NOT NULL); """
    
    table3 = """ CREATE TABLE IF NOT EXISTS Posibles_combinaciones (
                                        id integer PRIMARY KEY,
                                        Combinacion text NOT NULL,
                                        Cantidad integer NOT NULL); """
    table4 = """ CREATE TABLE IF NOT EXISTS Incompatible (
                                        id integer PRIMARY KEY,
                                        Tipo integer NOT NULL,
                                        incompatibles text NOT NULL); """
    try:
        c = conn.cursor()
        c.execute(table1)
        c.execute(table2)
        c.execute(table3)
        c.execute(table4)
    except sqlite3Error as e:
        print(e)

def fill_tables(conn, pokimones, tipos, todas_combinaciones, combinaciones):
    sql1 = """ INSERT INTO Datos_base (Ruta, Pokemon_1, Mote_1, Tipo_1, Pokemon_2, Mote_2, Tipo_2, Id_Tipo) VALUES (?, ?, ?, ?, ?, ?, ?, ?) """
    sql2 = """ INSERT INTO Asociacion_tipos (Tipo_1, Tipo_2, Id_Tipo) VALUES (?, ?, ?) """
    sql3 = """ INSERT INTO Posibles_combinaciones (Combinacion, Cantidad) VALUES (?, ?) """
    sql4 = """ INSERT INTO Incompatible (Tipo, incompatibles) VALUES (?, ?) """
    try:
        c = conn.cursor()
        for i in range (len(pokimones)):
            c.execute(sql1, (pokimones['Localizacion'][i], pokimones['Pokemon_'][i], pokimones['Mote_'][i], pokimones['Tipo_'][i], pokimones['Pokemon'][i], pokimones['Mote'][i], pokimones['Tipo'][i], int(pokimones['id_tipo'][i])))
        for i in range (len(tipos)):
            c.execute(sql2, (tipos['Tipo1'][i], tipos['Tipo2'][i], int(tipos['num'][i])))
        for i in range (len( todas_combinaciones)):
            list_element =  todas_combinaciones[i]
            tamanyo = len(list_element)
            meter = json.dumps(list(map(int, list_element)))
            c.execute(sql3, (meter, tamanyo))
        for i in range (len(combinaciones)):
            list_element =  combinaciones['incompatibles'][i]
            meter = json.dumps(list(map(int, list_element)))
            c.execute(sql4, (int(combinaciones['num'][i]), meter))
        conn.commit()
        
    except sqlite3Error as e:
        print(e)

def main():
    conn = None # conexion a la base de datos
    pokimones = pd.read_table('/home/jofa/Documents/pokimones/pokemon-soullink-team-generator/python/src/Bocatacas.tsv')
    entrenador1 = pd.DataFrame(columns=['Ruta','Pokemon','Tipo'])
    entrenador2 = pd.DataFrame(columns=['Ruta','Pokemon','Tipo']) 
    entrenador1[['Ruta','Pokemon','Tipo']] = pokimones[['Localizacion', 'Pokemon_', 'Tipo_']].copy()
    entrenador2[['Ruta','Pokemon','Tipo']] = pokimones[['Localizacion', 'Pokemon', 'Tipo']].copy()
    tipos = pd.DataFrame(columns=['Tipo1','Tipo2','num'])
    tipos['Tipo1']= entrenador1['Tipo'].copy()
    tipos['Tipo2']= entrenador2['Tipo'].copy()
    tipos = tipos[tipos['Tipo1'] != tipos['Tipo2']]
    pokimones = pokimones[pokimones['Tipo_'] != pokimones['Tipo']]
    pokimones = pokimones.reset_index(drop=True)
    tipos = tipos.reset_index(drop=True)
    tipos = sacar_tipos(tipos)
    pokimones['id_tipo'] = tipos['num'].copy()
    combinaciones = sacar_combinaciones(tipos)
    todas_combinaciones = []
    todas_combinaciones = sacar_todas_combinaciones(combinaciones, todas_combinaciones)
    # for i in todas_combinaciones:
    #     print (i)
    todas_combinaciones_df = pd.DataFrame(todas_combinaciones)
    todas_combinaciones_df.to_excel('/home/jofa/Documents/pokimones/pokemon-soullink-team-generator/python/output/todas_combinaciones.xlsx')
    conn = connect_to_db()
    create_tables(conn)
    fill_tables(conn, pokimones, tipos, todas_combinaciones, combinaciones)
    

if __name__ == "__main__":
    main()

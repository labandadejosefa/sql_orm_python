#M5 SQL ORM: Ejercicio de profundización 

import sqlite3
import csv
import requests
import json


def create_schema():
    #conecto a la DB, y si no existe -como es el caso-, la crea en este mismo momento
    conn = sqlite3.connect('inventario.db') 
    c = conn.cursor()

    c.execute("""DROP TABLE IF EXISTS producto;
            """)
    
    
    c.execute("""CREATE TABLE producto(
                    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                    [code_id] TEXT, 
                    [site_id] TEXT,
                    [title] TEXT,
                    [price] INTEGER, 
                    [currency_id] TEXT,
                    [initial_quantity] INTEGER,
                    [available_quantity] INTEGER,
                    [sold_quantity] INTEGER
                    );
                    """)
    conn.commit()
    conn.close()


#Lleno la tabla creada en la función anterior, con los datos del csv modificados como string MLA+nro
def fill():
    url= 'https://api.mercadolibre.com/items?ids='

    with open('meli_technical_challenge_data.csv') as file:
        data = list(csv.DictReader(file))

    #cargo la lista datos, con cada url de la forma 'https://api.mercadolibre.com/items?ids=MLAnumero', con los datos que pide el ejercicio
    datos = []


    for i in range(15): #Probé con 15 para verificar funcionamiento. Para la totalidad de los datos, usar range(len(data))
        dir = url + str(data[i]['site']) + str(data[i]['id'])
        info = requests.get(url=dir).json()

        if info[0]['code']==200:
            if info[0]['body'].get('id')!= None and info[0]['body'].get('site_id')!=None and info[0]['body'].get('title')!=None and info[0]['body'].get('price')!=None and info[0]['body'].get('currency_id')!=None and info[0]['body'].get('initial_quantity')!=None and info[0]['body'].get('available_quantity')!=None and info[0]['body'].get('sold_quantity')!=None:

                datos.append({'id':info[0]['body'].get('id'), 'site_id':info[0]['body'].get('site_id'), 'title':info[0]['body'].get('title'),'price':info[0]['body'].get('price'),'currency_id':info[0]['body'].get('currency_id'), 'initial_quantity':info[0]['body'].get('initial_quantity'),
                        'available_quantity':info[0]['body'].get('available_quantity'), 'sold_quantity':info[0]['body'].get('sold_quantity')}) 
                        
        else:
            print('Artículo no encontrado')    
    
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
  
    lista_unpacked=[]

    for i in datos:
        lista_unpacked.append(list(i.values())) 


    c.executemany("""
       INSERT INTO producto (code_id, site_id, title, price, currency_id, initial_quantity, available_quantity, sold_quantity)
       VALUES (?,?,?,?,?,?,?,?);""", lista_unpacked)


    conn.commit()
    conn.close()


def fetch(code):
    conn = sqlite3.connect('inventario.db') 
    c = conn.cursor()

    consulta = c.execute('SELECT * FROM producto WHERE code_id = ?', (code,))
    
    if consulta !=None:
        for row in consulta:
            print("\nArtículo consultado:\n", row)
    else:
        print("La consulta realizada contiene algún dato faltante. ")

    conn.close()


if __name__ == '__main__':
    print("Ejercicio de profundización SQL_ORM\n")
    # Crear DB
    create_schema()

    # Completar la DB con el CSV

    fill()

    # Leer filas
    #fetch('MLA806707270')
    fetch('MLA845041373')
    #fetch('MLA717159516')

    
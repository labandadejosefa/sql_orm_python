#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)


def fill():
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)

    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> el tutor de ese estudiante (el objeto creado antes)

    # No olvidarse que antes de poder crear un estudiante debe haberse
    # primero creado el tutor.

    Session = sessionmaker(bind=engine)
    session = Session()

    tutor1=Tutor(name='Tom')
    tutor2=Tutor(name='Vinicius')
    tutor3=Tutor(name='Elis')

    session.add(tutor1)
    session.add(tutor2)
    session.add(tutor3)

    estudiantes=[]

    estud1=Estudiante(name='Caetano', age=79,grade=3,tutor=tutor1)
    estud2=Estudiante(name='Gilberto', age=79, grade=4, tutor=tutor2)
    estud3=Estudiante(name='Lenine', age=63, grade=2, tutor=tutor2)
    estud4=Estudiante(name='Bethania', age=76, grade=5, tutor=tutor3)
    estud5=Estudiante(name='Joao', age=48, grade=6, tutor=tutor1)

    estudiantes.extend([estud1, estud2, estud3, estud4, estud5])

    session.add_all(estudiantes) 
    session.commit()
    print('Lista de estudiantes: ', estudiantes) #No lo pide, pero print para ver cómo quedan

def fetch():
    print('Comprovemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creaods de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez

    Session = sessionmaker(bind=engine) 
    session = Session()

    query = session.query(Estudiante)

    print('Todos los objetos creados en la tabla Estudiante:\n')

    for estudiante in query:
        print(estudiante)


def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name

    Session = sessionmaker(bind=engine)
    session = Session()

    resultados = session.query(Estudiante).join(Estudiante.tutor).filter(Tutor.name==tutor)

    print('Estudiantes que comparten al tutor', tutor ,': ')
    for resultado in resultados:
        print(resultado)



def modify(id, name):
    print('Modificando la tabla')
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debe
    # 1) buscar con una query el tutor por "tutor.name" usando name
    # pasado como parámetro y obtener el objeto del tutor
    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función update_persona_nationality

    Session = sessionmaker(bind=engine)
    session = Session()

    #Busco x nombre, el tutor que quiero cambiar. Lo guardo en la variable tutor_cambio
    query = session.query(Tutor).filter(Tutor.name==name)
    tutor_cambio = query.first()

    #Busco x id, al estudiante al que le quiero cambiar el tutor. Lo guardo en estud_cambio
    query2 = session.query(Estudiante).filter(Estudiante.id==id)
    estud_cambio = query2.first()

    #Actualizo al estudiante con nombre "name"
    estud_cambio.tutor = tutor_cambio

    session.add(estud_cambio)
    session.commit()

    query3= session.query(Estudiante).filter(Estudiante.id==id)
    
    print('Datos actualizados del estudiante ', query3.all() )


def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona

    Session = sessionmaker(bind=engine)
    session = Session()

    resultados = session.query(Estudiante).filter(Estudiante.grade==grade).count()

    print(f'Hay {resultados} estudiantes que cursan el', grade ,'º grado')


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    fill()
    fetch()

    opcion1=int(input('\nIngrese una opción para filtrar por tutor:\n1: Tom\n2: Vinicius\n3: Elis\n'))

    if opcion1 ==1:
        tutor='Tom'
    elif opcion1 ==2:
        tutor='Vinicius'
    elif opcion1 ==3:
        tutor='Elis'
    else:
        print('La opción ingresada es inválida. ')

    #tutor = 'nombre_tutor'
    search_by_tutor(tutor)

    opcion2 = int(input('\nIngrese una opción para REEMPLAZAR al tutor del estudiante 2:\n1: Tom\n2: Vinicius\n3: Elis\n'))

    if opcion2 ==1:
        nuevo_tutor='Tom'
    elif opcion2 ==2:
        nuevo_tutor='Vinicius'
    elif opcion2 ==3:
        nuevo_tutor='Elis'
    else:
        print('La opción ingresada es inválida. ')


    #nuevo_tutor = 'nombre_tutor'
    id = 2
    modify(id, nuevo_tutor)

    opcion3 = int(input('\nIngrese una opción para contar el número de estudiantes por grado: 1, 2,...,6:\n'))

    for i in range(1,7):
        if opcion3 ==i:
            grade=i 

    #grade = 2
    count_grade(grade)

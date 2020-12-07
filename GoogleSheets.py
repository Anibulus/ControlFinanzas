import os
from socket import gethostbyname, create_connection, error
import pygame
import time
import gspread #Libreria para sheets de google

pygame.init()
#Funciones basicas para cualquier sheet
class GoogleSheet():
#Características
    KEY=""
    hojas="" #Conjunto de hojas
    hojaActual=""#Hoja seleccionada
    sonido=""

    #Sobrecarga con parametro @KEY
    def __init__(self, key=""):
        self.KEY=key


    #Setters y getters
    def getKey(self):
        return self.KEY

#Métodos de gran importancia en los procesos

    #Retorna true o false 
    def conexion(self):
        conectividad=True
        try:
            gethostbyname("google.com")
            conexion=create_connection(("google.com",80),1)
            conexion.close()
        except error:
            conectividad=False
        return conectividad

    #Obtiene el sheet al que desea ingresar
    def acceso(self,credentials): #Se llama a si mismo
        gc=gspread.service_account(filename=credentials)
        #Nota: Tambien se debe compartir el sheet con el correo que esta en credentials
        if(self.conexion()):
            sh= gc.open_by_key(self.getKey())#Parte de la url
            lista=sh.worksheets()
            #Obtiene el titulo de cada elemento
            for item in range(len(lista)):
                lista[item]=lista[item].title
            self.haciendoALaMamada()
            self.hojas=lista
            self.mostrarOpciones(lista)
        else:
            sh=False
            self.sans("No hay conexion en este momento....")
        return sh

    def decisionNumerica(self, msj):
        incorrecto=True
        respuesta=0
        while (incorrecto):
            try:
                self.sans(msj)
                respuesta=int(input())
                incorrecto=False                
            except error:
                self.sans("Bueno tu estas pendejo, ¿o que?")
            finally: 
                self.clear()
        return respuesta
    
    def ingresarCifra(self):
        #TODO Hacer inteligente para sumar dentro de la misma, con espacios, sumas y comas
        incorrecto=True
        respuesta=0.0
        while (incorrecto):
            try:
                tmp=input()
                if(tmp==""):#No hay nada que registrar
                    respuesta={"isNumber":False}
                else:
                    respuesta={"isNumber":True, "respuesta":float(tmp)}
                incorrecto=False                
            except:
                self.sans("Bueno tu estas pendejo, ¿o que?")
            finally: 
                self.clear()
        return respuesta


#Métodos que sirven con fines estéticos

    #Limpia la console
    def clear(self): 
        os.system('cls') #on Windows System

    #Muestra enumeradamente las opciones
    def mostrarOpciones(self, lista):
        print("0-. Salir")
        for item in range(len(lista)):
            print(str(item+1)+"-. "+lista[item]) 

    def ConvertirDineroADecimal(self, lista):
        contador=0
        for item in lista:
            #Quita el signo de peso y da formato al decimal
            tmp=str(item).replace("$","")
            tmp=tmp.split(",")
            tmp=tmp[0].replace(".","")+"."+tmp[1]
            lista[contador]=tmp
            contador+=1
        return lista
            
        
    def removerEspaciosVacios(self,lista):
        while "" in lista:
            lista.remove("")
        return lista

    def sans(self,msj, ending=""):
        self.reproducir()      
        for x in msj:
            # Back up one character then print our next frame in the animation
            print(x,sep="", end=ending, flush=True)
            time.sleep(0.06)
        self.detener()

    def haciendoALaMamada(self):
        print("Ingresando", end="")
        for i in range(3):
            time.sleep(1)
            print(".", end="")
        time.sleep(1)
        self.clear()
        self.sans("Estamos dentro...")
        time.sleep(2)
        self.clear()
        time.sleep(0.5)
    

    def setSonido(self,sound):
        self.sonido=sound

    def getSonido(self):
        return self.sonido

    def reproducir(self):   
        pygame.mixer.music.load(self.sonido)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0.0)        
        
    def detener(self):
        pygame.mixer.music.stop()
#Fin de clase sheetsGoogle 

##Acciones con sheets de google

#TODO entender la diferencia entre ambos
#res=worksheet.get_all_records()
#print(res)
#res=worksheet.get_all_values()
#print(res)

#CRUD
#print(worksheet.row_values(1))
#print(worksheet.col_values(1))
#print(worksheet.get("A2"))
#print(worksheet.get("A2:C2"))
#Append(obj) o insert (obj, index) es posible
#worksheet.append_row(row,1)
#Row, Column (No empíeza en 0), value
#worksheet.update_cell(6,2,"Me estoy modificando jeje")
#worksheet.delete_row(1)
#wks.format('A1:B1', {'textFormat': {'bold': True}})
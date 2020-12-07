import os
from socket import gethostbyname, create_connection, error
import pygame
import time
from datetime import date
import gspread #Libreria para sheets de google

#Funciones basicas para cualquier sheet
class GoogleSheet():
#Características
    KEY=""#url
    hojas="" #Conjunto de hojas
    hojaActual=""#Hoja seleccionada
    acciones=()
    sonido=""
    DIAS_CORTE=(14,29)#Das en los que hago corte
    #Objetos de las hojas
    finanzas=""
    concentrado=""
    activos=""
    obligaciones=""
    luz=""

    def __init__(self, key="", sonido=""):
        pygame.init()
        self.KEY=key
        self.sonido=sonido
        self.concentrado=Concentrado(sonido)
        self.finanzas=Flujo(sonido)#TODO Renombrara a flujo
        self.luz=CFE(sonido)
        #TODO Pendientes las otras dos Hojas
        self.activos=""
        self.obligaciones=""        

    #Setters y getters
    def getKey(self):
        return self.KEY
    
    def setHojas(self, hojas):
        self.hojas=hojas

    def getHojas(self):
        return self.hojas

    def setHojaActual(self,hojas, eleccion):
        if(self.conexion()):
            self.hojaActual=hojas.get_worksheet(eleccion-1)            
        else:
            self.hojaActual=None

    def getHojaActual(self):
        return self.hojaActual

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
            sh=gc.open_by_key(self.getKey())#Parte de la url
            lista=sh.worksheets()            
            self.haciendoALaMamada()
            self.mostrarOpciones(self.ConvertirSheetsALista(lista))
            self.setHojas(sh)#Setea las hojas utilizables                    
        else:
            sh=None
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

    #
    def menuPrincipal(self,eleccion):
        while eleccion!=0:            
                self.setHojaActual(eleccion)
                if eleccion==1:#Flujo
                    pass
                elif eleccion==2:#Concentrado
                    pass
                elif eleccion==3:
                    pass
                elif eleccion==4:
                    pass
                elif eleccion==5:
                    pass
                elif eleccion==6:
                    pass


#Métodos que sirven con fines estéticos

    #Limpia la console
    def clear(self): 
        os.system('cls') #on Windows System

    def ConvertirSheetsALista(self,lista):
        #Obtiene el titulo de cada elemento
        for item in range(len(lista)):
            lista[item]=lista[item].title
        return lista

    #Muestra enumeradamente las opciones
    def mostrarOpciones(self, lista):
        print("0-. Salir")
        contador=0
        for item in lista:
            print(str(contador+1)+"-. "+item)
            contador+=1

    def previoAccion(self):
        #sh.get_worksheet(0).title
        return self.decisionNumerica("Se encuentra en "+str(self.getHojaActual().title)+" \n¿Qué accion deseas realizar? ")

    def mostrarAcciones(self):
        self.mostrarOpciones(self.acciones)
        return self.previoAccion()

    def convertirDineroADecimal(self, lista):
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


###print(sh.get_worksheet(1))
   #         print(sh.get_worksheet(1).title)
    #        worksheet=sh.get_worksheet(1)
     #       print(worksheet.acell("a2"))
      #      print(worksheet.cell(3,4).value)
       #     print(sh.get_worksheet(1).cell(3,4).value)    

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









#Hace herencia de sheetsGoogle
class Flujo(GoogleSheet):
    #Características
    #TODO Lo registrado tiene que quedar tambien en el sheet de concentrado
    acciones=("Registrar")
    
    #Constructor
    def __init__(self, sonido):  
        self.sonido=sonido
    #TODO reducir en concentrado el registro de un gusto y/o comida
#Fin de clase flujo










#Hace herencia de sheetsGoogle
class Concentrado(GoogleSheet):
    #Características
    #TODO Lo registrado tiene que quedar tambien en el sheet de concentrado
    acciones=("Concentrado","Corte", "Aportación", )
    CONCEPTOS=("Saldo de tarjeta de Nómina", "Ahorro del mes","Alcancía", "Cartera", "Saldo de tarjeta de Crédito")
    DIAS_CORTE=(14,29)#Das en los que hago corte

    #Constructor
    def __init__(self,sonido):
        self.sonido=sonido
    #métodos
    #TODO ver si hacerlo para fechas especificas o hacerlo por si solo
    def corteAlimento(self):#Semantica python, donde se llama a si mismo  
        #Siempre eprueba conexion qantes de continuar
        if(self.conexion()):
            cell = self.hojaActual.find("Concentrado")
            print("Found something at R%sC%s" % (cell.row, cell.col))
            #Obtiene los elementos individuales registrados      
            datos=self.hojaActual.get("F3:F100")#Celdas donde se encuentran los datos
            total=.0
            for item in datos:
                #Quita el signo de peso y da formato al decimal
                tmp=str(item[0]).replace("$","")
                tmp=tmp.split(",")
                total+=float(tmp[0].replace(".","")+"."+tmp[1])            
            self.sans("El total ha sido de: "+str(total))       

            #Ubica la quincena del momento y coloca el valor correspoondiente
            #Es más tres porque ocupara una posición más abajo ademas de los 2 espacios que no se utilizan
            datos=self.hojaActual.get("E3:E100")
            self.hojaActual.update_cell(len(datos)+3,5, str(int(total)) + " Quincena "+str(len(datos)+1))

            #Borra el contenido individual
            for i in range(3,31):
                self.hojaActual.update_cell(i,6,"")
            #Ahora lo coloca en la seccion de totales
        else:
            total=0
        return total

    def corteAlimento(self):#Semantica python, donde se llama a si mismo  
        #Siempre eprueba conexion qantes de continuar
        if(self.conexion()):
            #Obtiene los elementos individuales registrados      
            datos=self.hojaActual.get("F3:F100")#Celdas donde se encuentran los datos
            if(len(datos)>0):#Hay por lo menos un registro
                total=.0
                for item in self.convertirDineroADecimal(datos):
                    total+=float(item)
                self.sans("El total ha sido de: "+str(total))

                #Ubica la quincena del momento y coloca el valor correspoondiente
                #Es más tres porque ocupara una posición más abajo ademas de los 2 espacios que no se utilizan
                datos=self.hojaActual.get("E3:E100")
                self.hojaActual.update_cell(len(datos)+3,5, str(int(total)) + " Quincena "+str(len(datos)+1))
                #Borra el contenido individual
                for i in range(3,31):
                    self.hojaActual.update_cell(i,6,"")
                #Ahora lo coloca en la seccion de totales
            else:
                self.clear()
                self.sans("Para realizar un corte, requiere haber datos.")
                time.sleep(1)
                self.clear()

    def establecerConcentrado(self):
        #TODO decir cuando fue la ultima modificacion
        self.sans("Te mostraré la información que debes llenar, atento. \nPara omitir, pulsa \"Enter\"")
        time.sleep(2)
        self.clear()
        total=0.
        cont=0#contador
        for i in self.CONCEPTOS:            
            self.sans("En "+i+" registrado es: ")
            #Oneline if
            #expr1 if condition1 else expr2 if condition2 else exp
            coordenadas="A5" if cont==0 else "A6" if cont==1 else "B3" if cont==2 else "B4" if cont==3 else "B7"
            #Es usada de auxiliar para sumar todas las cantidades
            cantidades=self.getHojaActual().get(coordenadas)[0]
            self.sans(str(cantidades[0])+"\n")
            resp=self.ingresarCifra()
            if resp["isNumber"]:
                #TODO comprobar conecion antes de continuar
                cantidades=resp["respuesta"]
                #Valida si es A o B y conserva el numero de la derecha                
                self.hojaActual.update_cell(int(coordenadas[1:2]),1 if coordenadas[0:1]=="A" else 2, resp["respuesta"])#substring (string[start:end:step])
                self.hojaActual.update_cell(10,2, date.today().strftime("%d/%m/%Y")) #Fecha
                total+=float(cantidades)
            else:
                total+=float(self.convertirDineroADecimal(cantidades)[0])
            self.clear()
            cont+=1
        self.sans("El ajuste total quedaría de: $"+str(round(total,2)))
        time.sleep(5)
        self.clear()
        #TODO preguntar si lo quiere una vez mas o no

    #TODO reducir en concentrado el registro de un gusto y/o comida
#Fin de clase finanzas



class CFE(GoogleSheet):
    #Características
    KEY=""
    noHojas=1

    #Constructor
    def __init__(self, sonido):
        self.sonido=sonido


    #métodos
#Fin de clase finanzas
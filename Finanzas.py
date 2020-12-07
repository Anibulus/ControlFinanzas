from GoogleSheets import GoogleSheet
import time
from datetime import date
                

#Hace herencia de sheetsGoogle
class Finanzas(GoogleSheet):
    #Características
    #TODO Lo registrado tiene que quedar tambien en el sheet de concentrado
    acciones={"Flujo":("Registrar"),"Concentrado":("Concentrado","Corte", "Aportación", ),"Activos":(),"Obligaciones":()}
    conceptos=("Saldo de tarjeta de Nómina", "Ahorro del mes","Alcancía", "Cartera", "Saldo de tarjeta de Crédito")
    DIAS_CORTE=(14,29)#Das en los que hago corte

    #Constructor
    def __init__(self, key):
        super().__init__(key)    
        
    #métodos
    #TODO ver si hacerlo para fechas especificas o hacerlo por si solo
    def corteAlimento(self):#Semantica python, donde se llama a si mismo  
        #Siempre eprueba conexion qantes de continuar
        if(self.conexion()):
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
                for item in self.ConvertirDineroADecimal(datos):
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
        for i in self.conceptos:            
            self.sans("En "+i+" registrado es: ")
            #Oneline if
            #expr1 if condition1 else expr2 if condition2 else exp
            coordenadas="A5" if cont==0 else "A6" if cont==1 else "B3" if cont==2 else "B4" if cont==3 else "B7"
            #Es usada de auxiliar para sumar todas las cantidades
            cantidades=self.hojaActual.get(coordenadas)[0]
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
                total+=float(self.ConvertirDineroADecimal(cantidades)[0])
            self.clear()
            cont+=1
        self.sans("El ajuste total quedaría de: $"+str(round(total,2)))
        time.sleep(5)
        self.clear()
        #TODO preguntar si lo quiere una vez mas o no

    #TODO reducir en concentrado el registro de un gusto y/o comida
#Fin de clase finanzas

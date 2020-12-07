import json
import os
from GoogleSheets import GoogleSheet
from Finanzas import Finanzas
from Luz import CFE

#Carga de datos previo a iniciar el programa

#Leer archivo
with open(os.getcwd()+"/ControlFinanzas/claves.json", "r") as myfile:
    data=myfile.read()
# Parse file
CLAVES = json.loads(data)
CREDENCIALES=CLAVES["Credenciales"]

#Inicializacion de objetps
control=GoogleSheet()
control.setSonido(str(CLAVES["Sound"]))
fin=Finanzas(CLAVES["Finanzas"]["key"])
fin.setSonido(str(CLAVES["Sound"]))
luz=CFE(CLAVES["CFE"]["key"])
luz.setSonido(str(CLAVES["Sound"]))
control.clear()

#Muestra los sheets disponibles actualmente
#TODO hacer funcion de google sheets
sheets=("Finanzas Personales","CFE-Seguimiento")
print("Sheets disponibles:")
control.mostrarOpciones(sheets)

eleccion=control.decisionNumerica("Selecciona el sheet deseas modificar: ")
if eleccion == 0:
    control.sans("Saliendo...")
elif eleccion == 1:#Finanzas
    #Obtiene el acceso y contiene el objeto de las hojas
    fin.hojas=fin.acceso(CREDENCIALES)
    if fin.hojas!=False:
        #TODO hacer funcion buscar sheets y luego buscar acciones
        #Selecciona una hoja del monton
        eleccion=control.decisionNumerica("Seleccione la hoja que desea: ")#Para seleccionar la opcion deseada
        if eleccion==0:
            pass #salir
        elif eleccion<0:
            pass #Se sale
        else:
            #Define la hoja sobre la que se va a trabajar
            fin.hojaActual=fin.hojas.get_worksheet(eleccion-1)            
            #Crea un ciclo en el que se pueden ejecutar las acciones en una hoja definida
            opciones=True
            while opciones:
                #Muestra las acciones que se pueden ejecutar en la hoja que se seleccionó
                for item in fin.acciones.keys():
                    if(item==fin.hojaActual.title): #Decir que opciones tiene
                        control.mostrarOpciones(fin.acciones[item])
                        break
                eleccion=control.decisionNumerica("Se encuentra en "+fin.hojaActual.title+" \n¿Qué accion deseas realizar?")
                #TODO hacer seleccion dinamica
                if eleccion==1:
                    fin.establecerConcentrado()
                elif eleccion==2:
                    fin.corteAlimento()

            

elif eleccion == 2:#CFE
    #TODO poner un try catch que ntambien diga si no hay acceso
    worksheet=CFE.acceso("")
    print("¿A que seccion desea entrar?")
    encabezados=control.removerEspaciosVacios(worksheet.row_values(1))
    control.mostrarOpciones(encabezados)
    eleccion=control.decisionNumerica()
else:
    GoogleSheet.sans("Ya me voy a la verga ....")
    eleccion=0
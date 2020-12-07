import json
import os
import time
import gspread
from GoogleSheets import GoogleSheet

#Carga de datos previo a iniciar el programa

#Leer archivo
with open(os.getcwd()+"/ControlFinanzas/claves.json", "r") as myfile:
    data=myfile.read()
# Parse file
CLAVES = json.loads(data)
CREDENCIALES=CLAVES["Credenciales"]

#Inicializacion de objetps
control=GoogleSheet(CLAVES["Finanzas"]["key"],CLAVES["Sound"])
control.clear()

#Muestra los sheets disponibles actualmente
#TODO hacer funcion de google sheets
control.acceso(CREDENCIALES)
#Internamente llena una variable
if control.getHojas()!=None: #TODO ver s se puede colocar getHojas por si solo
    eleccion=control.decisionNumerica("Elige una opcion de las sheets que encontre ")
    if eleccion == 0 or eleccion<0:
        control.sans("Saliendo...")
        #TODO hacer funcion buscar sheets y luego buscar acciones
        #Selecciona una hoja del monton
    else :#Menu principal
        while eleccion!=0:            
            if eleccion==1:#Flujo
                print("Aun no entro en funcionamiento")
            elif eleccion==2:#Concentrado
                control.concentrado.setHojaActual(control.getHojas(),eleccion)
                if(control.concentrado.getHojaActual()!=None):#Si no se perdio la conexion
                    eleccion=control.concentrado.mostrarAcciones()
                    if eleccion==1:
                        control.concentrado.establecerConcentrado()
                    elif eleccion==2:
                        control.concentrado.corteAlimento()
                else:#Se perdio la conexion
                    control.clear()
                    control.sans("Se ha perdido la conexion")
                    #TODO quieres volver a intentarlo?
            elif eleccion==3:
                pass
            elif eleccion==4:
                pass
            elif eleccion==5:
                pass
            elif eleccion==6:
                pass
            control.mostrarOpciones(control.ConvertirSheetsALista(control.getHojas().worksheets()))
            eleccion=control.decisionNumerica("Elige una opcion de las sheets que encontre ")
        control.sans("Nos vemos, pero recuerda... \nTe estaré observando")
else: #Validacion de conexion a internet
    time.sleep(2)
    control.clear()
    control.sans("Pos ahí nos vidrios krnal, no encontre nada")
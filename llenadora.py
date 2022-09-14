#*******************************************************************************
#* INTERFACE GRAFICA DE CONTROL DE LLENADO DE CUBETAS
#* DESARROLLADOR: Necrovalle
#* VERSION: 0.9alpha
#* REPOSITORIO:
#* URL: https://github.com/Necrovalle/llenadora
#* Notas: libreria del serial: pip install pyserial
#*******************************************************************************

#********************************************************************* LIBRERIAS
from tkinter import *		# Widgets estandar
from tkinter import ttk		# Widgets nuevos del 8.5+
from tkinter import messagebox
import time
import datetime
import serial
import subprocess

#*********************************** DECLARACIONES E INICIALIZACION DE VARIABLES
ser = serial.Serial('COM4')  # open serial port
f_config = open('times.cnf','r')
date_time=""#fecha y hora actual
ENT = 'O'   #buffer de la lectura serial
T_A = 5     #Tiempo en segundos de llenado de la linea A
T_B = 5     #Tiempo en segundos de llenado de la linea B
T_a = 8     #Tiempo en segundos de descarga de la linea A
T_b = 8     #Tiempo en segundos de descarga de la linea B
Ta = 0      #Tiempo actual
Tfin = 0    #Tiempo actual guardado en pausa
ACT = False #Estado del sistema
INIT= False #Inicailización
FIN = False #Apagado del sistema (Pausa)
RT  = 0     #Estado de interrupcion de operacion 
CONT= 0     #Contador general de cubetas llenadas
HistF=""    #Archivo de historial


#************************************************************* FUNCIONES PROPIAS
def CargarCNF():
    global T_A
    global T_B
    global T_a
    global T_b
    Data = f_config.read()
    DT = Data.split('\n')
    T_A = int(DT[0])
    T_B = int(DT[1])
    T_a = int(DT[2])
    T_b = int(DT[3])
    f_config.close()
    
def regitro_cubeta():
    lbl4.config(text = str(CONT))
    HistF.write(date_time)
    HistF.write(", ")
    HistF.write(str(CONT))
    HistF.write("\n")

def crear_historia():
    global HistF
    DAT_NAM = date_time.replace("/","_")
    DAT_NAM = DAT_NAM.replace(" ","-")
    DAT_NAM = "H-" + DAT_NAM.replace(":","_") + ".txt"
    HistF = open(DAT_NAM,'w')
    HistF.write("Histórico de llenado de cubetas Deprochem \n")
    HistF.write("  Fecha  -  Hora, Número\n")
    #HistF.close()
    
    
    
    
def Conexion(): 
    ser.write(b'I')
    CON = 1
    time.sleep(1)
    ENT = 'O'
    if ser.inWaiting()>0:
        ENT = ser.read()
        if ENT != b'I':
            messagebox.showinfo(message="El hardware no coincide", title="Error")
        #else:
            #print("Conectado")
    else:
        messagebox.showinfo(message="Sin conexión con el hardware", title="Error")

def clock():
    global ACT
    global T_A
    global T_B
    global Ta
    global Ta_a
    global Ta_b
    global INIT
    global RT
    global Tfin
    global FIN
    global CONT
    global date_time
    global HistF
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lbl5.config(text = date_time)
    if ser.inWaiting()>0:
        ENT = ser.read()
        if ENT == b'1':
            if ACT == False:
                ACT = True
                Ta = 0
                crear_historia()
                lbl2.config(fg = "green")
                lbl2.config(text = "Activo")
        elif ENT == b'0':
            #revisar multicierre
            lbl2.config(fg = "red")
            lbl2.config(text = "Inactivo")
            ACT = False
            FIN = True
            HistF.close()
        elif ENT == b'F':
            lbl0.config(text = "Apagando sistema")
            subprocess.run('shutdown -s')
            ser.close()
            
    else:
        ENT = 'O'
    if ACT == True:
        if INIT == False:
            ser.write(b'A')
            Ta += 1
            if Ta == T_A:
                ser.write(b'X')
                INIT = True
                Ta = 0
        else:
            if FIN == True:
                Ta = Tfin
                if RT == 1:
                    ser.write(b'a')
                    time.sleep(0.1)
                    ser.write(b'B')
                if RT == 2:
                    ser.write(b'Y')
                if RT == 3:
                    ser.write(b'A')
                    time.sleep(0.1)
                    ser.write(b'b')
                if RT == 4:
                    ser.write(b'X')
                FIN = False
            if Ta == 0:
                ser.write(b'a')
                CONT = CONT + 1
                regitro_cubeta()
                time.sleep(0.1)
                ser.write(b'B')
            if Ta == T_B:
                ser.write(b'Y')
            if Ta == T_a:
                ser.write(b'A')
                time.sleep(0.1)
                ser.write(b'b')
                CONT = CONT + 1
                regitro_cubeta()
            if Ta == T_a +T_A:
                ser.write(b'X')
            Ta += 1
            if Ta == T_a + T_b:
                Ta = 0
    else:
        if FIN == True:
            Tfin = Ta
            ser.write(b'X')
            ser.write(b'Y')
            if Ta > 0 and Ta <= T_B:
                RT = 1
            elif Ta > T_B and Ta <= T_a:
                RT = 2
            elif Ta > T_a and Ta <= T_a +T_A:
                RT = 3
            elif Ta > T_a + T_A:
                RT = 4
            #print(RT)
    lbl5.after(1000, clock)

#******************************************************** CREACION DE LA VENTANA
window = Tk()
window.geometry('1024x590+0+0')
window.resizable(False, False)
window.title('Control de llenadora')
window.iconbitmap('Icons_Elec.ico')
img = PhotoImage(file="logoDeprochem.png")

lbl0 = Label(window, text='Control de llenado de cubetas')
lbl0.config(font=("Verdana 42 bold"))
lbl1 = Label(window, text='Sistema:')
lbl1.config(font=("Verdana 40 bold"))
lbl2 = Label(window, text='Inactivo')
lbl2.config(font=("Verdana 40 bold"), fg="red")
lbl3 = Label(window, text='Numero de cubetas:')
lbl3.config(font=("Verdana 40 bold"))
lbl4 = Label(window, text='0')
lbl4.config(font=("Verdana 40 bold"), fg="red")
lbl_img = Label(window, image=img)
lbl5 = Label(window, text="00/00/0000 00:00:00")
lbl5.config(font=("Verdana 34"))


lbl0.place(x=30, y=10)
lbl1.place(x=240, y=140)
lbl2.place(x=520, y=140)
lbl3.place(x=30, y=270)
lbl4.place(x=640, y=270)
lbl_img.place(x=515, y=440)
lbl5.place(x=30, y=410)

#************************************************************* MANEJO DE VENTANA
CargarCNF()
time.sleep(2)
Conexion()
clock()
window.mainloop()

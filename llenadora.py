#*******************************************************************************
#* INTERFACE GRAFICA DE CONTROL DE LLENADO DE CUBETAS
#* DESARROLLADOR: Necrovalle
#* VERSION: 0.1alpha
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

#*********************************** DECLARACIONES E INICIALIZACION DE VARIABLES
ser = serial.Serial('COM19')  # open serial port
f_config = open('times.cnf','r')
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
    #print(DT[0])
    
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
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lbl5.config(text = date_time)
    if ser.inWaiting()>0:
        ENT = ser.read()
        if ENT == b'1':
            if ACT == False:
                ACT = True
                Ta = 0
                #calcular tiempos
        elif ENT == b'0':
            ACT = False
            FIN = True
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
                    ser,write(b'Y')
                if RT == 3:
                    ser.write(b'A')
                    time.sleep(0.1)
                    ser.write(b'b')
                if RT == 4:
                    ser.write(b'X')
                FIN = False
            if Ta == 0:
                ser.write(b'a')
                time.sleep(0.1)
                ser.write(b'B')
            if Ta == T_B:
                ser.write(b'Y')
            if Ta == T_a:
                ser.write(b'A')
                time.sleep(0.1)
                ser.write(b'b')
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
window.geometry('1250x550')
window.resizable(False, False)
window.title('Control de llenadora')
img = PhotoImage(file="logoDeprochem.png")

lbl0 = Label(window, text='Control de llenado de cubetas con datalogger')
lbl0.config(font=("Verdana 36 bold"))
lbl1 = Label(window, text='Sistema:')
lbl1.config(font=("Verdana 36 bold"))
lbl2 = Label(window, text='Inactivo')
lbl2.config(font=("Verdana 36 bold"), fg="red")
lbl3 = Label(window, text='Numero de cubetas:')
lbl3.config(font=("Verdana 36 bold"))
lbl4 = Label(window, text='0')
lbl4.config(font=("Verdana 36 bold"), fg="red")
lbl_img = Label(window, image=img)
lbl5 = Label(window, text="00/00/0000 00:00:00")
lbl5.config(font=("Verdana 32"))


lbl0.place(x=10, y=10)
lbl1.place(x=400, y=150)
lbl2.place(x=640, y=150)
lbl3.place(x=94, y=300)
lbl4.place(x=640, y=300)
lbl_img.place(x=740, y=410)
lbl5.place(x=10, y=467)

#************************************************************* MANEJO DE VENTANA
CargarCNF()
time.sleep(2)
Conexion()
clock()
window.mainloop()

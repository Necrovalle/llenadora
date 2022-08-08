#*******************************************************************************
#* INTERFACE GRAFICA DE CONTROL DE LLENADO DE CUBETAS
#* DESARROLLADOR: Necrovalle
#* VERSION: 0.1alpha
#* REPOSITORIO:
#* <URL de gitHub>
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
ser = serial.Serial('COM4')  # open serial port
ENT = 'O'   #buffer de la lectura serial
T_A = 6     #Tiempo en segundos de llenado de la linea A
T_B = 6     #Tiempo en segundos de llenado de la linea B
Ta_A = 0    #Tiempo actual en la linea A
Ta_B = 0    #Tiempo actual en la linea A
ACT = False #Estado del sistema

#************************************************************* FUNCIONES PROPIAS
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
    global Ta_A
    global Ta_B
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    lbl5.config(text = date_time)
    if ser.inWaiting()>0:
        ENT = ser.read()
        if ENT == b'1':
            if ACT == False:
                ACT = True
                Ta_A = 0
                Ta_B = 0
                #calcular tiempos
        elif ENT == b'0':
            ACT = False
    else:
        ENT = 'O'
    if ACT == True:
        if Ta_A == 0:
            ser.write(b'a')
        elif Ta_A == T_A:
            ser.write(b'A')
        Ta_A += 1
        if Ta_A > 2*T_A:
            Ta_A = 0
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
time.sleep(2)
Conexion()
clock()
window.mainloop()

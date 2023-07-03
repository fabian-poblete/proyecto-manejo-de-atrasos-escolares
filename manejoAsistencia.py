import os
import mysql.connector
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
# import ctypes


# Obtener los nuevos valores de las variables de entorno
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

try:
    # Conectarse a la nueva base de datos utilizando los nuevos valores de las variables de entorno
    conexion = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = conexion.cursor()

    def mostrar_datos(nombre, curso, hora_actual):
        messagebox.showinfo("Datos del estudiante", f"Nombre: {nombre}\nCurso: {curso}\nHora actual: {hora_actual}")

    def obtener_datos_estudiante(rut):
        consulta = "SELECT rut, nombre_completo, curso FROM estudiantes WHERE rut = %s"
        cursor.execute(consulta, (rut,))
        resultado = cursor.fetchone()

        if resultado:
            rut, nombre, curso = resultado
            hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mostrar_datos(nombre, curso, hora_actual)
        else:
            messagebox.showerror("Error", "No se encontró ningún estudiante con el RUT ingresado.")

    def obtener_datos():
        rut = rut_entry.get()
        obtener_datos_estudiante(rut)

    # Crear la interfaz gráfica
    ventana = tk.Tk()
    ventana.title("Consulta de datos de estudiante")
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Establecer las dimensiones de la ventana
    ancho_ventana = 400
    alto_ventana = 400

    # Calcular la posición x, y para centrar la ventana
    posicion_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    posicion_y = int((alto_pantalla / 2) - (alto_ventana / 2))

    # Configurar la geometría de la ventana para centrarla en la pantalla
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

    ventana.resizable(False, False)
    ruta_logo = "C:/Users/usuario/Desktop/pdf/respaldo/logo.jfif"  # Reemplaza con la ruta de tu imagen de logo
    logo = Image.open(ruta_logo)
    logo = logo.resize((100, 100))  # Ajusta el tamaño del logo según tus necesidades
    logo = ImageTk.PhotoImage(logo)

    # Mostrar el logo en la interfaz
    logo_label = tk.Label(ventana, image=logo)
    logo_label.pack(pady=10)

    # Agregar campo de entrada de RUT
    rut_label = tk.Label(ventana, text="RUT:")
    rut_label.pack(pady=10)
    rut_entry = tk.Entry(ventana)
    rut_entry.pack()

    # Agregar botón para obtener los datos
    obtener_datos_button = tk.Button(ventana, text="Obtener Datos", command=obtener_datos)
    obtener_datos_button.pack(pady=10)

    # Ejecutar el bucle de eventos de la interfaz gráfica
    ventana.mainloop()

    conexion.close()

except mysql.connector.Error as error:
    print("Error al conectarse a la base de datos:", error)

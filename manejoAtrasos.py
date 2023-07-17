import os
import mysql.connector
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Obtener los nuevos valores de las variables de entorno
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

try:
    # Conectarse a la nueva base de datos utilizando los nuevos valores de las
    # variables de entorno
    conexion = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = conexion.cursor()

    def mostrar_datos(nombre, curso, hora_actual):
        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now()

        # Obtener el número del mes con cero antecedente si es necesario
        numero_mes = str(fecha_actual.month).zfill(2)

        # Configurar la fuente Arial
        fuente_arial = ("Arial", 12)

        # Crear una ventana personalizada
        ventana_personalizada = tk.Toplevel()
        ventana_personalizada.title("Datos del estudiante")
        ventana_personalizada.geometry("400x300")

        # Configurar la fuente de la ventana personalizada
        ventana_personalizada.option_add("*Font", fuente_arial)

        # Crear el mensaje con el formato deseado
        mensaje = f"Fundación Chaminade\nInstituto Linares\n\n"
        mensaje += "AUTORIZACIÓN".center(50) + "\n\n"  # Centrar el mensaje "AUTORIZACIÓN"
        mensaje += f"Autorizo a:{nombre}\n\n"
        mensaje += f"Curso: {curso}\n\n"
        mensaje += f"Ingresar a clase a las: {hora_actual}\n"
        mensaje += f"Retirarse de Clases a las: {hora_actual}\n\n"
        mensaje += f"Firma y Timbre\nLinares: {fecha_actual.day} de {numero_mes} de {fecha_actual.year}"


        # Mostrar el mensaje en la ventana personalizada
        etiqueta_mensaje = tk.Label(ventana_personalizada, text=mensaje)
        etiqueta_mensaje.grid(row=0, column=0, padx=10, pady=10)

        # Cargar el logo
        ruta_logo = "C:/Users/usuario/Desktop/Proyectos/Instituto-Linares/Programa-Instituto/logo.jfif"  # Reemplaza con la ruta correcta de tu logo
        logo = Image.open(ruta_logo)
        logo = logo.resize((50, 50))
        logo = ImageTk.PhotoImage(logo)

        # Mostrar el logo en la esquina derecha
        contenedor_logo = tk.Frame(ventana_personalizada)
        contenedor_logo.grid(row=0, column=1, padx=0.5, pady=0.5, sticky="ne")  # sticky="ne" para alinear en la esquina derecha

        etiqueta_logo = tk.Label(contenedor_logo, image=logo)
        etiqueta_logo.pack(padx=10, pady=20)  # Ajusta el valor de padx y pady para aumentar la separación

        # Ejecutar el bucle de eventos de la ventana personalizada
        ventana_personalizada.mainloop()

    def obtener_datos_estudiante(rut):
        consulta = "SELECT rut, nombre_completo, curso FROM estudiantes WHERE rut = %s"
        cursor.execute(consulta, (rut,))
        resultado = cursor.fetchone()

        if resultado:
            rut, nombre, curso = resultado
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            mostrar_datos(nombre, curso, hora_actual)
        else:
            messagebox.showerror(
                "Error", "No se encontró ningún estudiante con el RUT ingresado.")

    def obtener_datos():
        rut = rut_entry.get()
        obtener_datos_estudiante(rut)

    # Configurar la fuente Arial
    fuente_arial = ("Arial", 12)

    # Crear la interfaz gráfica
    ventana = tk.Tk()
    ventana.title("Autorización")
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Establecer las dimensiones de la ventana
    ancho_ventana = 300
    alto_ventana = 300

    # Calcular la posición x, y para centrar la ventana
    posicion_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    posicion_y = int((alto_pantalla / 2) - (alto_ventana / 2))

    # Configurar la geometría de la ventana para centrarla en la pantalla
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

    ventana.resizable(False, False)
    # Reemplaza con la ruta de tu imagen de logo
    ruta_logo = "C:/Users/usuario/Desktop/Proyectos/Instituto-Linares/Programa-Instituto/logo.jfif"
    logo = Image.open(ruta_logo)
    # Ajusta el tamaño del logo según tus necesidades
    logo = logo.resize((50, 50))
    logo = ImageTk.PhotoImage(logo)

    # Mostrar el logo y el texto en un mismo contenedor
    contenedor_logo_texto = tk.Frame(ventana)
    contenedor_logo_texto.pack(pady=10)

    # Mostrar el texto en el contenedor
    texto_label = tk.Label(
        contenedor_logo_texto,
        text="Fundación Chaminade\nInstituto Linares",
        justify="center",
        font=fuente_arial)
    texto_label.pack()

    # Agregar la línea
    canvas = tk.Canvas(
        contenedor_logo_texto,
        width=200,
        height=2,
        bd=0,
        highlightthickness=0,
        relief='ridge')
    canvas.create_line(0, 2, 200, 2)
    canvas.pack()

    # Mostrar el logo en el contenedor
    logo_label = tk.Label(contenedor_logo_texto, image=logo)
    logo_label.pack(pady=20)  # Ajusta el valor de pady para aumentar la separación

    # Agregar campo de entrada de RUT
    rut_label = tk.Label(ventana, text="RUT:", font=fuente_arial)
    rut_label.pack(pady=10)
    rut_entry = tk.Entry(ventana, font=fuente_arial)
    rut_entry.pack()

    # Agregar botón para obtener los datos
    obtener_datos_button = tk.Button(
        ventana,
        text="Obtener Datos",
        command=obtener_datos,
        font=fuente_arial)
    obtener_datos_button.pack(pady=10)

    # Ejecutar el bucle de eventos de la interfaz gráfica
    ventana.mainloop()

    conexion.close()

except mysql.connector.Error as error:
    print("Error al conectarse a la base de datos:", error)

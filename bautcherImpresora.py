#Este codigo tengo que probarlo con la impresora. De ahí ir revisando.

import os
import mysql.connector
import datetime
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from PIL import ImageTk
from escpos.printer import Usb

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

    def generar_imagen(nombre, curso, hora_actual):
        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now()

        # Obtener el número del mes con cero antecedente si es necesario
        numero_mes = str(fecha_actual.month).zfill(2)

        # Configurar la fuente y el tamaño del texto
        fuente = ImageFont.truetype("arial.ttf", 12)

        # Configurar el tamaño de la imagen
        width, height = 400, 300

        # Crear una imagen blanca con el tamaño especificado
        imagen = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(imagen)

        # Configurar el texto del mensaje
        mensaje = "Fundación Chaminade\nInstituto Linares"
        x, y = 10, 10
        draw.text((x, y), mensaje, fill="black", font=fuente)

        # Configurar el texto del autorizo
        autorizo_texto = f"Autorizo a: {nombre}\n\nCurso: {curso}\n\nIngresar a clase a las: {hora_actual}\n"
        x, y = 10, 100
        draw.text((x, y), autorizo_texto, fill="black", font=fuente)

        # Configurar el texto de la firma y el timbre
        firma_timbre_texto = f"Linares: {fecha_actual.day} de {numero_mes} de {fecha_actual.year}"
        x, y = 10, 200
        draw.text((x, y), firma_timbre_texto, fill="black", font=fuente)

        # Cargar el logo
        ruta_logo = "logo.jfif"  # Reemplaza con la ruta correcta de tu logo
        logo = Image.open(ruta_logo)
        logo = logo.resize((50, 50))

        # Crear una imagen blanca del mismo tamaño que el logo
        logo_con_fondo = Image.new("RGBA", logo.size, "white")

        # Pegar el logo en la imagen blanca para que tenga fondo blanco
        logo_con_fondo.paste(logo, (0, 0), mask=logo)

        # Pegar el logo en la esquina derecha de la imagen
        x, y = width - logo_con_fondo.width - 10, 10
        imagen.paste(logo_con_fondo, (x, y))

        # Guardar la imagen generada
        imagen.save("autorizacion.png")

        # Imprimir la imagen en la impresora térmica
        printer = Usb(0x04b8, 0x0e15)  # Reemplaza los valores de vid y pid según tu impresora
        printer.image("autorizacion.png")
        printer.cut()

    def obtener_datos_estudiante(rut):
        consulta = "SELECT rut, nombre_completo, curso FROM estudiantes WHERE rut = %s"
        cursor.execute(consulta, (rut,))
        resultado = cursor.fetchone()

        if resultado:
            rut, nombre, curso = resultado
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            generar_imagen(nombre, curso, hora_actual)
        else:
            print("No se encontró ningún estudiante con el RUT ingresado.")

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

    # Agregar botón para obtener datos
    obtener_datos_button = tk.Button(ventana, text="Obtener Datos", command=obtener_datos)
    obtener_datos_button.pack(pady=10)

    ventana.mainloop()

    conexion.close()

except mysql.connector.Error as error:
    print("Error al conectarse a la base de datos:", error)

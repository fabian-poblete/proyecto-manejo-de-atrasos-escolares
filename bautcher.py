import os
import mysql.connector
import datetime
from PIL import Image, ImageDraw, ImageFont

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

    # Obtener el RUT del estudiante desde la línea de comandos
    rut = input("Ingrese el RUT del estudiante: ")
    obtener_datos_estudiante(rut)

    conexion.close()

except mysql.connector.Error as error:
    print("Error al conectarse a la base de datos:", error)

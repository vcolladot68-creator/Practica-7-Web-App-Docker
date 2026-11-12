

from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)


def conectar_db():
    for intento in range(10):
        try:
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            return conexion

        except mysql.connector.Error as error:
            print(f"Intento {intento + 1}: {error}")
            time.sleep(3)

    return None


@app.route("/")
def inicio():
    conexion = conectar_db()

    if conexion:
        cursor = conexion.cursor()

        cursor.execute("SELECT DATABASE()")
        resultado = cursor.fetchone()
        nombre_bd = resultado[0]

        cursor.close()
        conexion.close()

        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Mi aplicación Docker</title>

            <style>
                body {{
                    font-family: Arial;
                    background: #eef2f7;
                    text-align: center;
                    padding: 80px;
                }}

                .contenedor {{
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    display: inline-block;
                }}

                h1 {{ color: #198754; }}
            </style>
        </head>

        <body>
            <div class="contenedor">
                <h1>¡Hola Mundo!</h1>
                <h2>Mi aplicación funciona con Docker.</h2>
                <p>Conexión a MySQL exitosa.</p>
                <p>Base de datos: {nombre_bd}</p>
            </div>
        </body>
        </html>
        """

    else:
        return "No se pudo conectar a MySQL", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

usuario = os.getenv('usuario')
contraseña = os.getenv('contrasena')
servidor = os.getenv('servidor')  
base_datos = os.getenv('base_datos')

# Crear la cadena de conexión
cadena_odbc = (
    f"DRIVER=ODBC Driver 17 for SQL Server;"
    f"SERVER={servidor};"
    f"DATABASE={base_datos};"
    f"UID={usuario};"
    f"PWD={contraseña};"
    f"TrustServerCertificate=yes;"
)
cadena_conexion = quote_plus(cadena_odbc)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={cadena_conexion}")

df_producto = pd.read_sql("SELECT * FROM dbo.Producto" , engine)


precio_menor = df_producto['precio'].min()

df_producto_menor = pd.read_sql(
    f"SELECT * FROM dbo.Producto WHERE precio = {precio_menor}",
    engine
)

print(df_producto_menor)

df_producto_prom = df_producto['precio'].mean()

df_producto_prom = round(df_producto_prom, 2)
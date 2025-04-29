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

#creacion de dataframes 

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={cadena_conexion}")

df_producto = pd.read_sql("SELECT * FROM dbo.Producto" , engine)


precio_menor = df_producto['precio'].min()

df_producto_menor = pd.read_sql(
    f"SELECT * FROM dbo.Producto WHERE precio = {precio_menor}",
    engine
)


df_producto_prom = df_producto['precio'].mean()

df_producto_prom = round(df_producto_prom, 2)
# devolucion del precio de los productos
print(f"El precio promedio es: {df_producto_prom}") 

#lectura de los roles de los usuarios
df_role = pd.read_sql("SELECT * FROM dbo.Rol" , engine)

#lectura de los usuarios 
df_usuario = pd.read_sql("SELECT * FROM dbo.Empleado" , engine)
# localización del id del rol mesero
df_role_mesero = df_role.loc[df_role['Rol'] == 'Mesero', 'id'].tolist()
print(f"El id del rol mesero es: {df_role_mesero}")
# lectura de los usuarios con el rol de mesero
df_usuario_mesero = df_usuario.loc[df_usuario['rol_id'] == df_role_mesero[0]]
print(f"Los usuarios con el rol de mesero son: {df_usuario_mesero}") 

df_categoria = pd.read_sql("SELECT * FROM dbo.Categoria" , engine)
# lectura de los productos con la categoria de entradas
df_categoria_entradas = df_categoria.loc[df_categoria['nombre'] == 'Entradas', 'id'].tolist()
print(f"El id de la categoria entradas es: {df_categoria_entradas}")
# lectura de los productos con la categoria de entradas
df_producto_entradas = df_producto.loc[df_producto['id_categoria'] == df_categoria_entradas[0]]
print(f"Los productos con la categoria entradas son: {df_producto_entradas}")

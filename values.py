""" 
Fecha: 08/05/2023
Realizado por: Jefry Stevan Cardenas
Realizado por: Jose  Luis Alfonso
"""
#Importacion de una libreria de python en SQL
import pymssql 

#Conexion a base de datos 
conection = pymssql.connect(                
    server='Ip servidor', # Ip del servidor de la BD
    user='user', #Usuario de SQL
    password='passwod', #Contraseña del usuario SQL
    database='Db' #Base de datos a la cual se conecta
)
#Conexion de la BD y trae los datos.
cursor = conection.cursor(as_dict=True)  
#Funcion para llamar los datos por parametros
def doQuery(cursor, query: str, params: tuple) -> dict: 
    try:
        cursor.execute(query, params)
        if "SELECT" in query.upper():
            resultado = cursor.fetchall() #Trae la lista o tupla de los datos solicitados de la BD
        elif "UPDATE" in query.upper() or "INSERT" in query.upper() or "DELETE" in query.upper(): #Realiza la modificacion de los datos de la BD
            resultado = cursor.rowcount #Muestra las columnas que fueron afectadas
        return resultado
    except Exception as e:
        return {"error": str(e)}

#Consulta Uno
Seleccion = "select Id_Shift,sum (Total) as total from Tb_Billing where  cast (InvoiceDate as date) between 'fecha inicial'  and 'fecha final' and Id_Device = 'dispositivo' group by Id_Device, Id_Shift order by Id_Shift asc"
query = doQuery(cursor, Seleccion,())  
print(query)

#en la consulta uno,se selecciona por medio de un query de SQL los datos que van a traerse y los rangos de fecha y las columnas a modificar

for rec in query: #Este for se hace con la finalidad de recorrer la lista, tupla o como tal la consulta uno
  #Consulta Dos
  print(f' Turno : {rec}')
  Seleccion2 = "SELECT TotalShift from Tb_Shift where  Id_Device = 'dispositivo' and Id_Shift = %d "
  query2 = doQuery(cursor, Seleccion2,(rec["Id_Shift"])) #Hace la seleccion de la columna que desee 
  print(f'Shit: {query2}')
  if (len(query2) != 0) :
    if (rec["total"]!=query2[0]["TotalShift"] ):#Se busca las columnas que sean distintas a cero
      #Reemplazar dato 
      print(f' * ERROR Turno {rec["Id_Shift"]} Incorrecto ')     
      remplazo =("update Tb_Shift SET TotalShift = %d where Id_Device = 'dispositivo' and Id_Shift = %d ")
      retorno = doQuery(cursor, remplazo,(rec["total"],rec["Id_Shift"])) #Realiza el reemplazo de la columna total, por el valor de la columna id_shift
      conection.commit()
    else: 
      print(f' * Turno {rec["Id_Shift"]} Correcto !!!!')  
  else:
    print(f' * Turno {rec["Id_Shift"]} no exite !!!!')

cursor.close()

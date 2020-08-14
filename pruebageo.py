import requests
import json
import pandas as pd
#variables globales
key = '<Insertar API KEY de Google>'
base = 'https://maps.googleapis.com/maps/api/geocode/json'
excel_origen = 'direcciones.xlsx'
excel_salida = 'direcciones_geo.xlsx'
#para un mejor resultado la direccion debe tener el siguiente formato
#<calle> <nro>, <distrito>, <Pais>
def obtenerGeoDireccion(direccion):
    url =f"{base}?address={direccion}&key={key}"
    r = requests.get(url)
    if r.status_code == 200:
        obj=r.json()
        geo = obj["results"][0]["geometry"]["location"]
        return geo
    else:
        return None

def obtenerLatitud(direccion):
    geo = obtenerGeoDireccion(direccion)
    return geo["lat"]

def obtenerLongitud(direccion):
    geo = obtenerGeoDireccion(direccion)
    return geo["lng"]


#obtener excel origen
xls = pd.ExcelFile(excel_origen)
print(xls.sheet_names)
df = xls.parse('Hoja1')

#formatear direccion
df['dir_format'] = df['direccion']+', '+df['distrito']+', '+df['pais']

#obtener latitud
df['lat_long'] = df.apply(lambda row: json.dumps(obtenerGeoDireccion(row.dir_format)), axis = 1) 
df['latitud'] = df.apply(lambda row: json.loads(row.lat_long)["lat"], axis = 1)
df['longitud'] = df.apply(lambda row: json.loads(row.lat_long)["lng"], axis = 1)

#guardar en excel
df.to_excel(excel_salida)

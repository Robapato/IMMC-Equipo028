from random import randrange
import numpy as np

#variables
num_carros=350
media_carros = 15
desv_tipica = 7
tiempo_escaneo_producto = 1
caja_ocupada = 0
tiempo_total_caja=4000
tiempo_espera_total = 0
tarjeta_porcentaje=70
num_cajas=4

# crea las colas de cajas
lista_colas=[]
for caja in range(num_cajas):
    new_caja={"num_caja":caja,"carros_en_cola":[],"carro_en_caja":0}
    lista_colas.append(new_caja)
#print(lista_colas)

# generar lista carros
lista_de_carros=[]
## Generate a normal distribution with the specified mean and standard deviation
distribution = np.random.normal(media_carros, desv_tipica, num_carros)  
distribution = np.round(distribution).astype(int) # Round the values to integers
for producto in range(num_carros): # eliminamos numeros de carros < 1
    if distribution[producto] < 1:
        distribution[producto] = 1
# asignamos resto de datos a cada carro
for carro_to_create in range(num_carros):
    carr={}
    #carr["num_productos"]=distribution[carro_to_create]
    carr["num_productos"]=20
    carr["num_carro"]= carro_to_create+1
    carr["tiempo_llegada"]=randrange(3600)
    random_number=randrange(100)
    if random_number > tarjeta_porcentaje:
        carr["pago_tarjeta"] ="no"
        tiempo_pago=30
    else:
        carr["pago_tarjeta"] ="si"
        tiempo_pago=10
    carr["tiempo_cola"]=0
    carr["tiempo_proceso_rest"]= carr["num_productos"]*tiempo_escaneo_producto+tiempo_pago
    carr["procesado_en_caja"]=0
    lista_de_carros.append(carr)


# generamos la simulacion
#bucle por segundos
for seconds in range(3600):
    # buscar si ha entrado un nuevo carro y ponerlo en una cola (aleatoria)
    for carro in (lista_de_carros):
        if carro["tiempo_llegada"] == seconds:
             cola_asignada=randrange(num_cajas)
             for cajai in lista_colas:
                 if cajai["num_caja"] == cola_asignada:
                    cajai["carros_en_cola"].append(carro["num_carro"])
                    carro["procesado_en_caja"]=cola_asignada

    # añadir 1 segundo a los carros en la cola
    for colai in lista_colas:
        for carro_col in colai["carros_en_cola"]:
            for carroc in lista_de_carros:
                if carroc.get("num_carro") == carro_col:
                    carroc["tiempo_cola"] += 1
                    tiempo_espera_total += 1
    # quitar un segundo al carro en caja

    for colaii in lista_colas:                
        if colaii["carro_en_caja"] != 0:
            for carroc in lista_de_carros:
                if carroc.get("num_carro") == colaii["carro_en_caja"]:
                    carroc["tiempo_proceso_rest"] += -1
                    if carroc["tiempo_proceso_rest"] == 0:
                        colaii["carro_en_caja"]  = 0
        else:   # si hay caja vacia coge el primer carro de la cola
            if len(colaii["carros_en_cola"]) > 0:
                colaii["carro_en_caja"] = colaii["carros_en_cola"][0]
                colaii["carros_en_cola"].pop(0)
#for carrod in lista_de_carros:
#    print("Tienmpo en cola:", "[",carrod["num_carro"],"]", carrod["tiempo_cola"] , carrod["procesado_en_caja"] )
print(tiempo_espera_total)

#falta programar para más de 1 caja
#falta prrogramar las 4 opciones de caja:
#Muchas cajas normales (Se va a una aleatoria)
#Se va a la caja con menos clientes
#Hay cajas para con tarjeta y para efectivo
#Hay una caja para compras inferiores a x poductos
#Se compara la caja con menos tiempo total de espera, y elegimos ese para escfribir el informe
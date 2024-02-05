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
num_cajas_efectivo=1
num_cajas_tarjeta=3

# funciones
def asigna_caja(lista_de_colas, num_carr):
    min_en_cola = num_carr
    # calcula el numero minimo de carros en cola
    for cajae in lista_de_colas:
        if len(cajae["carros_en_cola"]) < min_en_cola:
            min_en_cola = len(cajae["carros_en_cola"])

    # si hay varias con el mismo numero aleatorio
    cajas_min = []
    for cajac in lista_de_colas:
        if len(cajac["carros_en_cola"]) == min_en_cola:
            cajas_min.append(cajac["num_caja"])
    random_number=randrange(len(cajas_min))
    return(cajas_min[random_number])




# crea las colas de cajas
lista_colas_efectivo=[]
for caja in range(num_cajas_efectivo):
    new_caja={"num_caja":caja,"carros_en_cola":[],"carro_en_caja":0}
    lista_colas_efectivo.append(new_caja)
#print(lista_colas_efectivo)

lista_colas_tarjeta=[]
for caja in range(num_cajas_tarjeta):
    new_caja={"num_caja":caja,"carros_en_cola":[],"carro_en_caja":0}
    lista_colas_tarjeta.append(new_caja)
#print(lista_colas_tarjeta)

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
    # buscar si ha entrado un nuevo carro y ponerlo en una cola
    for carro in (lista_de_carros):
        if carro["tiempo_llegada"] == seconds:
            if carro["num_productos"] > 10:
                cola_asignada = asigna_caja(lista_colas_tarjeta, num_carros)
                #print("caja_tarjeta")
                for cajai in lista_colas_tarjeta:
                    if cajai["num_caja"] == cola_asignada:
                        cajai["carros_en_cola"].append(carro["num_carro"])
                        carro["procesado_en_caja"]=cola_asignada

            else:
                cola_asignada=asigna_caja(lista_colas_efectivo, num_carros)
                #print("caja_efecttivo")
                for cajai in lista_colas_efectivo:
                    if cajai["num_caja"] == cola_asignada:
                        cajai["carros_en_cola"].append(carro["num_carro"])
                        carro["procesado_en_caja"]=cola_asignada

    # añadir 1 segundo a los carros en la cola
    for colai in lista_colas_efectivo:
        for carro_col in colai["carros_en_cola"]:
            for carroc in lista_de_carros:
                if carroc.get("num_carro") == carro_col:
                    carroc["tiempo_cola"] += 1
                    tiempo_espera_total += 1
    
    for colai in lista_colas_tarjeta:
        for carro_col in colai["carros_en_cola"]:
            for carroc in lista_de_carros:
                if carroc.get("num_carro") == carro_col:
                    carroc["tiempo_cola"] += 1
                    tiempo_espera_total += 1
    # quitar un segundo al carro en caja

    for colaii in lista_colas_efectivo:                
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
    
    for colaii in lista_colas_tarjeta:                
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
print(tiempo_espera_total)

#for carrod in lista_de_carros:
#    print("Tienmpo en cola:", "[",carrod["num_carro"],"]", carrod["tiempo_cola"] , carrod["procesado_en_caja"] )

#falta programar para más de 1 caja
#falta prrogramar las 4 opciones de caja:
#Muchas cajas normales (Se va a una aleatoria)
#Se va a la caja con menos clientes
#Hay cajas para con tarjeta y para efectivo
#Hay una caja para compras inferiores a x poductos
#Se compara la caja con menos tiempo total de espera, y elegimos ese para escfribir el informe
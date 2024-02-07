from faker import Faker
import csv, time

fake = Faker('es_ES')   # cambiamos el locale a español

num = 1 # secuencia para los nombres de los ficheros
while True:

    output = open(f'spool/datosFaker-{num}.csv', 'w')
    mywriter = csv.writer(output, delimiter=";")

    for r in range(100):
        mywriter.writerow([fake.free_email(),
                        fake.password(),
                        fake.name(),
                        fake.job()])
    output.close()

    num = num + 1

    time.sleep(60) # espera 60 segundos y genera un nuevo archivo

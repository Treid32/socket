#!/usr/bin/env python3
import socket

#Dichiarazione indirizzo e porta server
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224

#Funzione per verificare i dati
def riceviComandi(socket):
    while True:
        sock_service, addr_client = socket.accept()
        print("\nConnessione ricevuta da " + str(addr_client))          #Connessione col Client
        print("\nAspetto di ricevere i dati ")
        contConn = 0
        while True:
            dati = sock_service.recv(2048)
            contConn += 1
            if not dati:
                print("Fine dati dal client. Reset")
                break

            dati = dati.decode()
            print("Ricevuto: '%s'" % dati)                              #Ricezione e decodifica dati
            if dati == '0':
                print("Chiudo la connessione con " + str(addr_client))
                break

            dati = dati.split(";")  # operatore;primo numero;secondo numero -> [piu][primo numero][secondo numero]
            risposta = str()

            #Verifica dell'operatore e successivamente dei numeri
            if dati[0] == "piu" or dati[0] == "meno" or dati[0] == "per" or dati[0] == "diviso":
                try:
                    dati[1] = int(dati[1])
                    dati[2] = int(dati[2])
                except ValueError:
                    print("ValueError")
                    risposta = "Non hai inserito i numeri correttamente."

                if risposta == "":  #Valori corretti
                    risultato = int()
 
                    #Calcolo dell'operazione
                    if dati[0] == "piu":
                        risultato = dati[1] + dati[2]
                    elif dati[0] == "meno":
                        risultato = dati[1] - dati[2]
                    elif dati[0] == "per":
                        risultato = dati[1] * dati[2]
                    else:
                        risultato = dati[1] / dati[2]

                    
                    #Costruzione stringa
                    risposta = "Il risultato dell'operazione " + \
                        str(dati[0]) + " tra " + str(dati[1]) + " e " + \
                        str(dati[2]) + " è uguale a " + str(risultato) + "."
            else:
                risposta = "Operazione non valida."

            risposta = risposta.encode()

            sock_service.send(risposta)
        sock_service.close()

#Funzione di avvio Server
def avviaServer(address, port):
    sock_listen = socket.socket()
    sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_listen.bind((address, port))
    sock_listen.listen(5)
    print("Server in ascolto su %s." % str((address, port)))

    riceviComandi(sock_listen)


if __name__ == "__main__":
    avviaServer(SERVER_ADDRESS, SERVER_PORT)

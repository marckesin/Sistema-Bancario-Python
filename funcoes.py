import hashlib
import os
import pyinputplus as pyip

# Função limpa tela
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# Transforma senha informada em uma hash SHA256
def to_hash(password):
    hash_obj = hashlib.sha256(password.encode()).hexdigest()
    return hash_obj


# Verifica se as credenciais informadas estão no banco de dados
def login(collection):
    print("Insira as credenciais da sua conta (nome e senha)")
    nome = input("Qual seu nome? \n")
    senha = pyip.inputPassword("Qual a sua senha? \n")
    resultado = collection.find_one({"nome": nome, "hash": to_hash(senha)})

    if resultado:
        return resultado["_id"]


# Verifica saldo sa conta
def checa_saldo(id_cliente, collection):
    resultado = collection.find_one({"_id": id_cliente}, {
        "_id": 0,
        "movimentacao": 1
    })
    total_depositos = sum(resultado["movimentacao"]["deposito"])
    total_saques = sum(resultado["movimentacao"]["saque"])
    return total_depositos - total_saques

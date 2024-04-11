import hashlib
import os
import pyinputplus as pyip


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def to_hash(password):
	hash_obj = hashlib.sha256(password.encode()).hexdigest()
	return hash_obj


def login(collection):
    print("Insira as credenciais da sua conta (nome e senha)")
    nome = input("Qual seu nome? \n")
    senha = pyip.inputPassword("Qual a sua senha? \n")
    resultado = collection.find_one({"nome": nome, "hash": to_hash(senha)})

    if resultado:
        return resultado["_id"]


def checa_saldo(id_cliente, collection):
    resultado = collection.find_one({"_id": id_cliente}, {
        "_id": 0,
        "movimentacao": 1
    })
    total_depositos = sum(resultado["movimentacao"]["deposito"])
    total_saques = sum(resultado["movimentacao"]["saque"])
    return total_depositos - total_saques
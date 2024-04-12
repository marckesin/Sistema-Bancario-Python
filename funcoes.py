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


# Realiza depósito
def realiza_deposito(id_cliente, collection):
	if id_cliente:
		print("Login realizado com sucesso! \n")
		valor_deposito = pyip.inputNum(
		    "Qual valor você gostaria de depositar? \n")

		collection.update_one(
		    {"_id": id_cliente},
		    {"$push": {
		        "movimentacao.deposito": valor_deposito
		    }})
		clear()
		print(f"Valor depositado: R$ {valor_deposito}")
	else:
		clear()
		print("Nome e/ou senha incorretos! \n")


# Realiza saque
def realiza_saque(id_cliente, collection):
	if id_cliente:
		while True:
		    valor_saque = abs(
		        pyip.inputNum(
		            "Qual valor você gostaria sacar? (Limite de R$ 500.00 por saque) \n"
		        )
		    )
		    if valor_saque > 500:
		        print("O valor limite por operação é de no máximo R$ 500.00")
		    elif valor_saque == 0:
		        clear()
		        print("Nenhum valor foi sacado da sua conta.")
		        break
		    elif valor_saque > checa_saldo(id_cliente, collection):
		        print("Saldo insuficiente.")
		    else:
		        collection.update_one(
		            {"_id": id_cliente},
		            {"$push": {"movimentacao.saque": valor_saque}},
		        )
		        clear()
		        print(f"Valor sacado: R$ {valor_saque:.2f} \n")
		        break
	else:
		clear()
		print("Nome e/ou senha incorretos! \n")


# Checa extrato
def extrato(id_cliente, collection):
    if id_cliente:
        print("Login realizado com sucesso! \n")

        # Busca apenas as movimentações financeiras co cliente
        resultado = collection.find_one(
            {"_id": id_cliente}, {"_id": 0, "movimentacao": 1}
        )

        clear()
        print("=" * 55)
        for tipo in resultado["movimentacao"]["deposito"]:
            print(f"Depósitos realizados: R$ {tipo:.2f}")
        for tipo in resultado["movimentacao"]["saque"]:
            print(f"Saques realizados: R$ {tipo:.2f}")
        print(f"Saldo Total = R$ {checa_saldo(id_cliente, collection):.2f}")
        print("=" * 55)
        print("\n\n")
    else:
        clear()
        print("Nome e/ou senha incorretos! \n")
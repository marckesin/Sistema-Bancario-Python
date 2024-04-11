import os
import re
import pyinputplus as pyip
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient
from art import logo
from funcoes import to_hash, login, clear, checa_saldo


load_dotenv()
URI = os.getenv("URI")


def main():
    try:
        clear()
        client = MongoClient(URI)
        client.admin.command("ping")
        print("Conectado ao MongoDB!")
        # client = MongoClient("localhost", 27017)
        db = client.maindatabase
        collection = db.customers
    except Exception as e:
        print(e)


    while True:
        print(logo)
        print("""Bem vindo ao pyBank! Escolha uma das opções a seguir:
#######################################################		
1- Criar Conta;            
2- Depositar;
3- Realizar saque;
4- Extrato;
5- Sair;
#######################################################
            """)

        opcao = pyip.inputInt("Qual opção desejada? ")

        if opcao == 1:
            while True:
                while True:
                    nome = input("Qual seu nome? \n")
                    verifica_nome = re.match(r'^[a-zA-Z]+[a-zA-Z\s]*[a-zA-Z]+$', nome)
                    if verifica_nome:
                        break
                    print("Nome inválido. Seu nome não deve conter números ou espaços em branco.")
                if collection.find_one({"nome": nome}):
                    print("Nome de usuário já existe!\n")
                else:
                    break

            while True:
                senha = pyip.inputPassword("Digite uma senha: \n")
                confirma_senha = pyip.inputPassword(
                    "Digite sua senha novamente: \n")
                if senha == confirma_senha:
                    senha_hash = to_hash(senha)
                    novo_cliente = {
                        "nome": nome,
                        "movimentacao": {
                            "deposito": [],
                            "saque": []
                        },
                        "hash": senha_hash,
                        "data": datetime.now(tz=timezone.utc),
                    }

                    collection.insert_one(novo_cliente)
                    clear()
                    print(f"""
#########################################################
  Conta criada com sucesso! Bem-vindo ao pyBank {nome}! 
#########################################################
                        """)
                    print("\n\n")
                    break
                else:
                    print("Senha digitada não confere!")
        elif opcao == 2:
            id_cliente = login(collection)

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
        elif opcao == 3:
            id_cliente = login(collection)

            if id_cliente:
                while True:
                    valor_saque = abs(
                        pyip.inputNum(
                            "Qual valor você gostaria sacar? (Limite de R$ 500.00 por saque) \n"
                        ))
                    if valor_saque > 500:
                        print(
                            "O valor limite por operação é de no máximo R$ 500.00")
                    elif valor_saque == 0:
                        clear()
                        print("Nenhum valor foi sacado da sua conta.")
                        break
                    elif valor_saque > checa_saldo(id_cliente, collection):
                        print("Saldo insuficiente.")
                    else:
                        collection.update_one(
                            {"_id": id_cliente},
                            {"$push": {
                                "movimentacao.saque": valor_saque
                            }})
                        clear()
                        print(f"Valor sacado: R$ {valor_saque:.2f} \n")
                        break
            else:
                clear()
                print("Nome e/ou senha incorretos! \n")
        elif opcao == 4:
            id_cliente = login(collection)

            if id_cliente:
                print("Login realizado com sucesso! \n")

                resultado = collection.find_one({"_id": id_cliente}, {
                    "_id": 0,
                    "movimentacao": 1
                })

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
                print("Nome e/ou senha incorretos!")
        elif opcao == 5:
            clear()
            print("Volte sempre! \n")
            break
        else:
            clear()
            print("Opção inválida, selecione novamente a operação desejada. \n")


if __name__ == '__main__':
    main()

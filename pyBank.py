import os
import re
import pyinputplus as pyip
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient
from art import logo
from funcoes import to_hash, login, clear, checa_saldo, realiza_deposito, realiza_saque, extrato

# Carrega as variaveis de ambiente
load_dotenv()
URI = os.getenv("URI")


def main():
    try:
        clear()

        # Conecta ao MongoDB Atlas
        client = MongoClient(URI)
        client.admin.command("ping")
        print("Conectado ao MongoDB!")
        # client = MongoClient("localhost", 27017) # Banco de dados local para testes
        db = client.maindatabase
        collection = db.customers
    except Exception as e:
        print(e)

    while True:
        print(logo)
        print(
            """Bem vindo ao pyBank! Escolha uma das opções a seguir:
#######################################################		
1- Criar Conta;            
2- Depositar;
3- Realizar saque;
4- Extrato;
5- Sair;
#######################################################
            """)

        opcao = pyip.inputInt("Qual opção desejada? ")

        # Cadastro de novos clientes
        if opcao == 1:
            while True:
                while True:
                    nome = input("Qual seu nome? \n")

                    # Verifica se o nome não possui caracteres inválidos
                    verifica_nome = re.match(r"^[a-zA-Z]+[a-zA-Z\s]*[a-zA-Z]+$", nome)
                    if verifica_nome:
                        break
                    print(
                        "Nome inválido. Seu nome não deve conter números ou espaços em branco."
                    )
                if collection.find_one({"nome": nome}):
                    print("Nome de usuário já existe!\n")
                else:
                    break

            # Verifica se as senhas digitadas conferem
            while True:
                senha = pyip.inputPassword("Digite uma senha: \n")
                confirma_senha = pyip.inputPassword("Digite sua senha novamente: \n")
                if senha == confirma_senha:
                    senha_hash = to_hash(senha)
                    novo_cliente = {
                        "nome": nome,
                        "movimentacao": {"deposito": [], "saque": []},
                        "hash": senha_hash,
                        "data": datetime.now(tz=timezone.utc),
                    }

                    collection.insert_one(novo_cliente)
                    clear()
                    print(
                        f"""
#########################################################
  Conta criada com sucesso! Bem-vindo ao pyBank {nome}! 
#########################################################
                        """
                    )
                    print("\n\n")
                    break
                else:
                    print("Senha digitada não confere!")
        # Depositar
        elif opcao == 2:
            id_cliente = login(collection)
            # Realiza o deposito se o cliente for encontrado no banco de dados
            realiza_deposito(id_cliente, collection)
        # Saque
        elif opcao == 3:
            id_cliente = login(collection)
            # Realiza o saque se o cliente for encontrado no banco de dados
            realiza_saque(id_cliente, collection)
        # Verifica extrato da conta
        elif opcao == 4:
            id_cliente = login(collection)
            extrato(id_cliente, collection)
        # Sai do programa
        elif opcao == 5:
            clear()
            print("Volte sempre! \n")
            break
        else:
            clear()
            print("Opção inválida, selecione novamente a operação desejada. \n")


if __name__ == "__main__":
    main()

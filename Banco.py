import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tSair
    """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor <= 0:
        print("Erro: Valor inválido.")
    else:
        saldo += valor
        print(f"Operação bem-sucedida.\nNovo saldo: R${saldo:.2f}.")
        extrato = extrato + f"Depósito: R${valor:.2f}\n"
        
    return saldo, extrato

def sacar(*,saldo,valor,extrato,limite,num_saques, limite_saques): 
    if num_saques >= limite_saques:
        print("Erro: Limite de saques diário atingido.")
        
    elif valor <= 0 or valor > saldo:
        print(f"Erro: Valor inválido. \nSaldo total: R${saldo:.2f}.")
        
    elif valor > limite:
        print(f"Erro: Limite de saque excedido. \nSaldo total: R${saldo:.2f}.")

    else:
        saldo -= valor
        print(f"Operação bem-sucedida.\nNovo saldo: R${saldo:.2f}.")
        num_saques += 1
        extrato = extrato + f"Saque: R${valor:.2f}\n"
    
    return saldo, extrato
    
def exibir_extrato(saldo,/,*,extrato):
    print("************* EXTRATO ***************")
    print("Não foram realizadas movimentações na conta." if not extrato else extrato)
    print("*************************************")
    
def criar_usuario(usuarios):
    cpf = input("Insira seu CPF (apenas números): ")
    usuario = filtrar_usuario(cpf,usuarios)
    if (usuario):
        print("Usuário já existe no banco de dados.")
        return
    
    nome = input("Digite seu nome completo: ")
    data_nas = input("Insira sua data de nascimento (dd-mm-aaaa):")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nas, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    
def criar_conta(agencia, num_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": num_conta, "usuario": usuario}

    print("\nUsuário não encontrado.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

    
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("Operação inválida.")


main()
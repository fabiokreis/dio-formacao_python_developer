import textwrap


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
ENDC = '\033[0m'
FAIL = '\033[91m'
OKCYAN = '\033[96m'

INVALID_OPTION = "Operação inválida, por favor selecione novamente a operação desejada."

DEPOSIT_INITIAL_MESSAGE = "Informe o valor do depósito: "
DEPOSIT_SUCCESS = OKGREEN + "Depósito realizado com sucesso!" + ENDC
DEPOSIT_ERROR = FAIL + "Operação falhou! O valor informado é inválido." + ENDC

WITHDRAW_COUNT_LIMIT = 3
WITHDRAW_VALUE_LIMIT = 500
WITHDRAW_INITIAL_MESSAGE = "Informe o valor do saque: "
BALANCE_EXCEEDED_MESSAGE = FAIL + "Operação falhou! Você não tem saldo suficiente." + ENDC
VALUE_EXCEEDED_MESSAGE = FAIL + "Operação falhou! O valor do saque excede o limite." + ENDC
WITHDRAW_COUNT_MESSAGE = FAIL + "Operação falhou! Número máximo de saques excedido." + ENDC
WITHDRAW_INVALID_VALUE_MESSAGE = FAIL + "Operação falhou! O valor informado é inválido." + ENDC
WITHDRAW_SUCCESS = OKGREEN + "Saque realizado com sucesso!" + ENDC

ADD_NEW_USER_INITIAL_MESSAGE = "Informe o CPF (somente número): "
ADD_NEW_USER_EXISTING_CPF = FAIL + "Já existe usuário com esse CPF!" + ENDC
ADD_NEW_USER_SUCCESS = OKGREEN + "Usuário criado com sucesso!" + ENDC

ADD_NEW_ACCOUNT_INITIAL_MESSAGE = "Informe o CPF do usuário: "
ADD_NEW_ACCOUNT_SUCCESS = OKGREEN + "Conta criada com sucesso!" + ENDC
ADD_NEW_ACCOUNT_FAIL = FAIL + "Usuário não encontrado, fluxo de criação de conta encerrado!" + ENDC

DEPOSIT = "Depósito"
WITHDRAW = "Saque"


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += atualizar_extrato(DEPOSIT, valor)
        print(DEPOSIT_SUCCESS)
    else:
        print(DEPOSIT_ERROR)

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print(BALANCE_EXCEEDED_MESSAGE)

    elif excedeu_limite:
        print(VALUE_EXCEEDED_MESSAGE)

    elif excedeu_saques:
        print(WITHDRAW_COUNT_MESSAGE)

    elif valor > 0:
        saldo -= valor
        extrato += atualizar_extrato(WITHDRAW, valor)
        numero_saques += 1
        print(WITHDRAW_SUCCESS)

    else:
        print(WITHDRAW_INVALID_VALUE_MESSAGE)

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print(HEADER + "\n================ EXTRATO ================" + ENDC)
    print(OKCYAN + "Não foram realizadas movimentações." + ENDC if not extrato else extrato)
    print(f"\n{OKCYAN}Saldo: R$ {saldo:.2f}{ENDC}")
    print(HEADER + "==========================================" + ENDC)


def criar_usuario(usuarios):
    cpf = input(ADD_NEW_USER_INITIAL_MESSAGE)
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(ADD_NEW_USER_EXISTING_CPF)
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print(ADD_NEW_USER_SUCCESS)


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input(ADD_NEW_ACCOUNT_INITIAL_MESSAGE)
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(ADD_NEW_ACCOUNT_SUCCESS)
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print(ADD_NEW_ACCOUNT_FAIL)


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def atualizar_extrato(operation, value):
    global statement
    color = OKBLUE if operation == DEPOSIT else FAIL

    return f"{color}{operation}: R$ {value:.2f}{ENDC}\n"


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

        if opcao == "d":
            valor = float(input(DEPOSIT_INITIAL_MESSAGE))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input(WITHDRAW_INITIAL_MESSAGE))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print(INVALID_OPTION)


main()
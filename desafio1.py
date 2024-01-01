MENU = """
Digite uma opção:

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
ENDC = '\033[0m'
FAIL = '\033[91m'
OKCYAN = '\033[96m'

balance = 0
statement = ""
withdraw_count = 0

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

DEPOSIT = "Depósito"
WITHDRAW = "Saque"


def main():
    show_options()


def show_options():
    while True:
        option = input(MENU)

        match option:
            case "d":
                deposit()
            case "s":
                withdraw()
            case "e":
                bank_statement()
            case "q":
                break
            case _:
                show_invalid_option()


def deposit():
    global balance, statement
    value = float(input(DEPOSIT_INITIAL_MESSAGE))
    valid_value = value > 0

    if valid_value:
        balance += value
        update_statement(DEPOSIT, value)
        print(DEPOSIT_SUCCESS)
    else:
        print(DEPOSIT_ERROR)


def withdraw():
    global withdraw_count, balance, statement

    value = float(input(WITHDRAW_INITIAL_MESSAGE))

    balance_exceeded = value > balance
    value_exceeded = value > WITHDRAW_VALUE_LIMIT
    withdraw_count_exceeded = withdraw_count >= WITHDRAW_COUNT_LIMIT
    valid_value = value > 0

    if balance_exceeded:
        print(BALANCE_EXCEEDED_MESSAGE)
    elif value_exceeded:
        print(VALUE_EXCEEDED_MESSAGE)
    elif withdraw_count_exceeded:
        print(WITHDRAW_COUNT_MESSAGE)
    elif valid_value:
        balance -= value
        update_statement(WITHDRAW, value)
        withdraw_count += 1
        print(WITHDRAW_SUCCESS)
    else:
        print(WITHDRAW_INVALID_VALUE_MESSAGE)


def bank_statement():
    print(HEADER + "\n================ EXTRATO ================" + ENDC)
    print(OKCYAN + "Não foram realizadas movimentações." + ENDC if not statement else statement)
    print(f"\n{OKCYAN}Saldo: R$ {balance:.2f}{ENDC}")
    print(HEADER + "==========================================" + ENDC)


def show_invalid_option():
    print(INVALID_OPTION)


def update_statement(operation, value):
    global statement
    color = OKBLUE if operation == DEPOSIT else FAIL

    statement += f"{color}{operation}: R$ {value:.2f}{ENDC}\n"


main()

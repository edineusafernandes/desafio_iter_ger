class Saque(Transacao):
    def __init__(self, valor: float):
        super().__init__(valor)
        self.tipo = "Saque"

class Deposito(Transacao):
    def __init__(self, valor: float):
        super().__init__(valor)
        self.tipo = "Deposito"

def log_transacao(func):
    def wrapper(clientes, *args, **kwargs):
        transacao = func(clientes, *args, **kwargs)
        if transacao:
            cliente

def menu(): '''
\/o\/o\/o\/o\/o\/o MENU \/o\/o\/o\/o\/o\/o
    1. SAQUE
    2. DEPOSITO
    3. SALDO
    4. EXTRATO
    5. CRIAR NOVA CONTA
    6. NOVO USUÁRIO
    7. SAIR
\/o\/o\/o\/o\/o\/o\/o\/o\/o\/o\/o\/o\/o\/o

=> Escolha uma opção: 
'''

def filtrar_cliente(cpf, clientes):
    cliente = 

def recuperar_conta(cliente):

@log_transacao
def depositar(clientes):

@log_transacao
def sacar(clientes):

@log_transacao
def extrato(clientes):

@log_transacao
def novo_usuario(clientes):

@log_transacao
def nova_conta(clientes):

def listar_contas(contas):
    for conta in contas:
        print(f"{conta['cliente']['nome']} - {conta['numero']}")

class PessoaFisica(cliente):

class Conta:

class ContaCorrente(conta):

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strtftime("%d/%m/%y %H:%M:%S")
            }
        )

class Transacao(ABC):

class Saque(transacao):

class Deposito(transacao):

def log_transacao(func):

def menu():


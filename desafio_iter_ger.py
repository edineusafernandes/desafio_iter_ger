from abc import ABC, abstractmethod
import datetime
import textwrap


class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.contas):
            conta = self.contas[self.index]
            self.index += 1
            return conta
        
        raise StopIteration
        
class Cliente:
    _clientes = [] 
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 5:
            print("\nNúmero máximo de transações diárias.")
            return 
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)  
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(cpf)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco 
class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0008"
        self.cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self.saldo
    
    @property
    def agencia(self):
        return self.agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\nValor de saque inválido.")
            return False
        
        if valor > self.saldo:
            print("Saldo insuficiente para realizar o saque.")
            return False

        self.saldo -= valor
        print(f"\nSaque de R${valor:.2f} realizado com sucesso.")
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self,valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite 
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print("\nO valor do saque excede o valor do limite.")

        elif excedeu_saques:
            print("\nAtingido o número máximo de saques diários.")

        else:
            return super().sacar(valor)
        
        return False 
    
    def __str__(self):
        return f"""
        Agência: \t{self.agencia}
        Conta Corrente: \t{self.numero}
        Títular: \t{self.cliente.nome}
 """

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
                "data": datetime.utcnow().strftime("%d/%m/%y %H:%M:%S"),
            }
        )
        
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lomer() == tipo_transacao.lomer():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d/%m%y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes 
   
class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor 
        
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao: 
            conta.historico.adicionar_transacao(self)
            print(f"\nSaque no valor de R${self.valor:.2f} realizado com sucesso!")
        else:
            print("\nSaque não realizado.")

class Deposito(Transacao):
    def __init(self, valor):
        self.valor = valor

        @property
        def valor(self):
            return self.valor
        
        def registrar(self, conta):
            sucesso_transacao = conta.depositar(self.valor)

            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)
                print(f"\nDepósito no valor de R${self.valor:.2f} realizado com sucesso.")
            else:
                print("\nDepósito não realizado.")

def menu():
    menu = """
    =:=:==:=:==:=:= MENU =:=:==:=:==:=:=
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [sr]\tSair
    =:=:==:=:==:=:=: =:=:==:=:==:=:=:=:=
    ==> Digite a sua opção: 
    """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta(cliente):
    if not cliente.contas:
        print("\nCliente não possui contas cadastradas.")
        return None 
    
    return cliente.conta[0]

def depositar(clientes):
    cpf = input("\nInforme o CPF do títular: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não cadastrado.")
        return
    
    valor = float(input("\nInformeo valor do depósito: R$ "))
    transacao = Deposito(valor)
    conta = recuperar_conta(cliente)
    if not conta:
        return

def sacar(clientes):
    cpf = input("\nInforme o CPF do títular: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não cadastrado.")
        return
    
    valor = float(input("\nInforme o valor do saque: R$ "))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("\nInforme o CPF do títular: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado.")
        return
    
    conta = recuperar_conta(cliente)
    if not conta:
        return
    
    print(f"\n:==:=:=:=: Extrato da conta {conta.numero}:==:=:=:=: ")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas transações"

    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['data']} - {transacao['tipo']} - R$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: \nR$ {conta.saldo:.2f}") 
    print("=:=:=:=:==:=:=:=:==:=:=:=:==:=:=:=:=:=:=:=::=:=:=:")

def numero_conta(clientes, contas):
    cpf = input("\n Informe o CPF do títular: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado")
        return
    
    numero = len(contas) + 1
    conta = ContaCorrente(cliente, numero)
    contas.append(conta)
    cliente.adicionar_conta.append(conta)

    print(f"\nConta {conta.numero} criada com sucesso!")

def listar_contas(clientes):
    if not clientes:
        print("\nNão há clientes cadastrados")
        return
    
    for clientes in clientes:
        print(f"\nCliente: {clientes.nome} - CPF: {clientes.cpf}.")
        for conta in clientes.conta:
            print(f"\nConta: {conta.numero} - Agência: {conta.agencia}.")

def novo_usuario(clientes):
    cpf = input("\nInforme o CPF do títular (apenas números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nCliente com com CPF cadastrado.")
        return
    
    nome = input("\nInforme o nome do títular: ")
    data_nascimento = input("\nInforme a data de nascimento (dd/mm/aaaa): ")
    endereco = input("\nInforme o endereço (logradouro, número, bairro, cidade, estado): ")
    endereco = endereco.split(", ")

    cliente = PessoaFisica(nome = nome, data_nascimento = data_nascimento, cpf = cpf, endereco = endereco)

    clientes.append(cliente)

    print(f"\nCliente {cliente.nome} cadastrado com sucesso!")

def log_transacao(func):
    def wrapper(clientes, *args, **kwargs):
        resultado = func(clientes, *args, **kwargs)
        nome_funcao = func.__name__.replace("+", " ").capitalize()
        print(f"\nTransação realizada: {nome_funcao}.")
        return resultado
    return wrapper

    @log_transacao
    def depositar(clientes):
        cpf = input("\nInforme o CPF do títular: ")
        cliente = filtrar_cliente(cpf, clientes)
        if not cliente:
            print(f"\nCliente não encontrado.")
            return

    @log_transacao
    def sacar(clientes):
        cpf = input("\nInforme o CPF do títular: ")
        cliente = filtrar_cliente(cpf, clientes)
        if not cliente:
            print(f"\nCliente não encontrado.")
            return

    @log_transacao
    def exibir_extrato(clientes):
        cpf = input("\nInforme o CPF do títular: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\nCliente não cadastrado.")
            return
    
        conta = recuperar_conta_ciente(cliente)
        if not conta:
            return
            print(f"\n:==:=:=:=: Extrato da conta {conta.numero}:==:=:=:=: ")
        transacoes = conta.historico.transacoes

        extrato = ""
        tem_transacao = False
        for transacao in conta.historico.gerar_relatorio():
            tem_transacao = True
            extrato += f"\n{transacao['data']} - {transacao['tipo']} - R$ {transacao['valor']:.2f}"

        if not tem_transacao:
         extrato = "Não foram realizadas transações"

        print(extrato)
        print(f"\nSaldo: \nR$ {conta.saldo:.2f}") 
        print("=:=:=:=:==:=:=:=:==:=:=:=:==:=:=:=:=:=:=:=::=:=:=:")
    
    @log_transacao
    def novo_usuario(clientes):
        cpf = input("\nInforme o CPF do títular: ")
        cliente = filtrar_cliente(cpf, clientes)

        if cliente:
            print("\nCliente com CPF cadastrado.")
            return
        
    @log_transacao
    def nova_conta(clientes):
        cpf = input("\nInforme o CPF do títular: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\nCliente não encontrado.")
            return 

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nc":
            numero_conta(clientes)

        elif opcao =="lc":
            listar_contas(clientes)

        elif opcao == "nu":
            novo_usuario(clientes)

        elif opcao == "sr":
            print("\nVolte sempre! Estaremos à sua disposição.")
            break

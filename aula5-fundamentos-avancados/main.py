# EXEMPLO DICIONÁRIO

# Mapas associativos
usuario = {
    "nome": "João Victor",
    "idade": 21,
    "profissao": "Jovem Aprendiz"
}

print(usuario["nome"])
print(usuario["profissao"])

# Tabelas hash
usuarios = {
    1: "João",
    2: "Sophia",
    3: "Raquel"
}

print(usuarios[2])

# FUNÇÕES LAMBDA

# Função comum / Lambda
dobro = lambda numero: numero * 2

print(dobro(20))

# Exemplo com map()
numeros = [1, 2, 3, 4]

dobrados = list(map(lambda numero: numero * 2, numeros))

print(dobrados)

# Exemplo com filter()
numeros = [1, 2, 3, 4, 5, 6]

pares = list(filter(lambda numero: numero % 2 == 0, numeros))

print(pares)

# Exemplo prático: ordenar usuários por idade
usuarios = [
    {"nome": "Ana", "idade": 25},
    {"nome": "Carlos", "idade": 20},
    {"nome": "Marina", "idade": 30}
]

usuarios_ordenados = sorted(usuarios, key=lambda usuario: usuario["idade"])

print(usuarios_ordenados)

# GERADORES

# Exemplo básico
def contador():
    yield 1
    yield 2
    yield 3

for numero in contador():
    print(numero)

# Exemplo prático: gerar números até um limite
def gerar_numeros(limite):
    numero = 1

    while numero <= limite:
        yield numero
        numero += 1

for n in gerar_numeros(5):
    print(n)

# Comparação com lista
lista = [numero for numero in range(1000000)]
gerador = (numero for numero in range(1000000))

print(type(lista))
print(type(gerador))

# CLOSURES

# Exemplo básico
def criar_multiplicador(fator):
    def multiplicar(numero):
        return numero * fator

    return multiplicar

dobrar = criar_multiplicador(2)
triplicar = criar_multiplicador(3)

print(dobrar(10))
print(triplicar(10))

# Exemplo prático: validador de senha
def criar_validador(tamanho_minimo):
    def validar(texto):
        return len(texto) >= tamanho_minimo

    return validar

validar_senha = criar_validador(8)

print(validar_senha("abc"))
print(validar_senha("abc12345"))

# DECORADORES

# Exemplo básico
def meu_decorador(funcao):
    def wrapper():
        print("Antes da função")
        funcao()
        print("Depois da função")

    return wrapper

@meu_decorador
def saudacao():
    print("Olá!")

saudacao()
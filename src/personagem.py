
class Personagem:
    PONTOS_TOTAIS = 25

    def __init__(self, nome: str, raca: str, sexo: str, cor_pele: str, tamanho_cabelo: str):
        self.nome = nome
        self.raca = raca
        self.sexo = sexo
        self.cor_pele = cor_pele
        self.tamanho_cabelo = tamanho_cabelo
        self._cor_cabelo = "#000000"  # Valor padrão preto
        self._cor_olhos = "#000000"   # Valor padrão preto
        self._forca = 0
        self._destreza = 0
        self._inteligencia = 0
        self._carisma = 0

    @property
    def cor_cabelo(self) -> str:
        return self._cor_cabelo

    @cor_cabelo.setter
    def cor_cabelo(self, valor: str):
        if isinstance(valor, str) and valor.startswith('#') and len(valor) == 7:
            self._cor_cabelo = valor
        else:
            raise ValueError("Cor do cabelo deve ser um código hexadecimal (ex: #RRGGBB)")

    @property
    def cor_olhos(self) -> str:
        return self._cor_olhos

    @cor_olhos.setter
    def cor_olhos(self, valor: str):
        if isinstance(valor, str) and valor.startswith('#') and len(valor) == 7:
            self._cor_olhos = valor
        else:
            raise ValueError("Cor dos olhos deve ser um código hexadecimal (ex: #RRGGBB)")

    @property
    def forca(self) -> int:
        return self._forca

    @forca.setter
    def forca(self, valor: int):
        if not isinstance(valor, int):
            raise ValueError("Força deve ser um número inteiro")
        if not 0 <= valor <= 10:
            raise ValueError("Força deve estar entre 0 e 10")
        if not self._validar_pontos(valor, self._forca):
            raise ValueError("Pontos insuficientes para esta força")
        self._forca = valor

    @property
    def destreza(self) -> int:
        return self._destreza

    @destreza.setter
    def destreza(self, valor: int):
        if not isinstance(valor, int):
            raise ValueError("Destreza deve ser um número inteiro")
        if not 0 <= valor <= 10:
            raise ValueError("Destreza deve estar entre 0 e 10")
        if not self._validar_pontos(valor, self._destreza):
            raise ValueError("Pontos insuficientes para esta destreza")
        self._destreza = valor

    @property
    def inteligencia(self) -> int:
        return self._inteligencia

    @inteligencia.setter
    def inteligencia(self, valor: int):
        if not isinstance(valor, int):
            raise ValueError("Inteligência deve ser um número inteiro")
        if not 0 <= valor <= 10:
            raise ValueError("Inteligência deve estar entre 0 e 10")
        if not self._validar_pontos(valor, self._inteligencia):
            raise ValueError("Pontos insuficientes para esta inteligência")
        self._inteligencia = valor

    @property
    def carisma(self) -> int:
        return self._carisma

    @carisma.setter
    def carisma(self, valor: int):
        if not isinstance(valor, int):
            raise ValueError("Carisma deve ser um número inteiro")
        if not 0 <= valor <= 10:
            raise ValueError("Carisma deve estar entre 0 e 10")
        if not self._validar_pontos(valor, self._carisma):
            raise ValueError("Pontos insuficientes para este carisma")
        self._carisma = valor

    def _validar_pontos(self, novo_valor: int, atributo_atual: int) -> bool:
        total_atual = self._forca + self._destreza + self._inteligencia + self._carisma
        return (total_atual - atributo_atual + novo_valor) <= self.PONTOS_TOTAIS

    def pontos_restantes(self) -> int:
        return self.PONTOS_TOTAIS - (self._forca + self._destreza + self._inteligencia + self._carisma)

    def __str__(self) -> str:
        return (f"Personagem(Nome={self.nome}, Raça={self.raca}, "
                f"Força={self.forca}, Destreza={self.destreza}, "
                f"Inteligência={self.inteligencia}, Carisma={self.carisma})")
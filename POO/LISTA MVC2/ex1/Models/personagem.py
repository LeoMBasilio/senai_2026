# Models/personagem.py — classe base dos personagens do mini-RPG
# Usa Single Table Inheritance (STI): TODAS as subclasses (Guerreiro, Mago, Arqueiro)
# são armazenadas na MESMA tabela "personagens". A coluna "tipo" diferencia cada uma.
# Vantagem: uma única tabela simplifica as consultas; desvantagem: colunas de subclasses
# ficam NULL para as outras classes (ex: mago.forca é NULL).

from sqlalchemy import Column, Integer, String
from Models.base import Base


class Personagem(Base):
    __tablename__ = "personagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    hp = Column(Integer, nullable=False, default=100)      # pontos de vida atuais
    hp_max = Column(Integer, nullable=False, default=100)  # vida máxima (para resetar após batalha)
    nivel = Column(Integer, nullable=False, default=1)     # afeta o dano calculado em atacar()

    # "tipo" é o discriminador: o SQLAlchemy lê este campo para saber qual subclasse instanciar
    # quando faz SELECT na tabela. Sem este campo, o polimorfismo não funciona.
    tipo = Column(String(50), nullable=False)

    # Colunas específicas de cada subclasse — nullable=True porque nem toda classe usa todos.
    # Guerreiro usa forca, Mago usa poder_magico, Arqueiro usa precisao.
    forca = Column(Integer, nullable=True)
    poder_magico = Column(Integer, nullable=True)
    precisao = Column(Integer, nullable=True)

    # polymorphic_on: qual coluna diferencia as subclasses
    # polymorphic_identity: valor gravado na coluna "tipo" para esta classe base
    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "personagem",
    }

    def atacar(self, alvo: "Personagem") -> int:
        # NotImplementedError force as subclasses a implementar este método.
        # É o equivalente a um método abstrato — sem @abstractmethod por compatibilidade com ORM.
        raise NotImplementedError("Implemente atacar() na subclasse")

    def esta_vivo(self) -> bool:
        # Encapsula a condição de vida em um método legível — evita comparar hp > 0 espalhado pelo código.
        return self.hp > 0

    def resetar_hp(self):
        # Restaura o hp ao máximo antes de cada batalha para garantir que os personagens
        # começam com vida cheia independente de batalhas anteriores.
        self.hp = self.hp_max

    def __repr__(self):
        return f"{self.tipo.capitalize()}(nome={self.nome!r}, hp={self.hp}/{self.hp_max}, nivel={self.nivel})"

from Models.Database_Model import CriarTabelas
from Controllers.Guilda_Controller import GuildaController
from Views.Menu_View import MenuView

ctrl = GuildaController()
view = MenuView()


def registrar_heroi():
    heroi = ctrl.registrar_heroi(input("Nome: ").strip(), input("Classe: ").strip())
    print(f"Herói '{heroi.nome}' registrado!")


def listar_herois():
    view.exibir_herois(ctrl.listar_herois())


def criar_missao():
    missao = ctrl.criar_missao(
        input("Título: ").strip(),
        input("Descrição: ").strip(),
        int(input("Recompensa XP: ")),
        int(input("ID do herói: "))
    )
    if missao:
        print(f"Missão '{missao.titulo}' criada!")


def concluir_missao():
    if ctrl.concluir_missao(int(input("ID da missão: "))):
        print("Missão concluída! XP adicionado.")


def main():
    CriarTabelas()
    view.executar({
        "1": registrar_heroi,
        "2": listar_herois,
        "3": criar_missao,
        "4": concluir_missao,
    })


if __name__ == "__main__":
    main()

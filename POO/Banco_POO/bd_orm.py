"""Agenda de contatos com SQLAlchemy ORM e interface Rich.

Este módulo demonstra como usar SQLAlchemy para mapear uma classe Python
para uma tabela SQLite e executar operações CRUD básicas em uma sessão.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from rich import print
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.pretty import install

install()
console = Console()

class BD_ORM:
    """Encapsula o engine do SQLAlchemy.

    O engine é o objeto que mantém a configuração de conexão e cria conexões
    físicas com o banco de dados.

    Attributes:
        __engine (Engine): Instância do engine SQLAlchemy usada para criar
            conexões com o SQLite.
    """

    def __init__(self, url: str):
        """Inicializa o engine usando a URL de conexão."""
        self.__engine = create_engine(url)

    def get_engine(self):
        """Retorna o engine criado para ser usado pela sessão."""
        return self.__engine

class Base(DeclarativeBase):
    """Base declarativa usada para definir modelos mapeados."""
    pass

class Contato(Base):
    """Modelo ORM que representa um contato na tabela 'contatos'.

    Esta classe usa mapeamento declarativo do SQLAlchemy. Cada atributo
    anotado com ``Mapped[...]`` corresponde a uma coluna da tabela.

    Attributes:
        __tablename__ (str): Nome da tabela no banco de dados.
        id (int): Chave primária única do contato.
        nome (str): Nome do contato.
        email (str): Endereço de e-mail do contato.
        telefone (int): Telefone do contato.
    """

    __tablename__ = 'contatos'

    # Coluna inteira que identifica unicamente cada registro.
    id: Mapped[int] = mapped_column(primary_key=True)
    # Coluna de texto para armazenar o nome completo.
    nome: Mapped[str]
    # Coluna de texto para armazenar o email.
    email: Mapped[str]
    # Coluna inteira para armazenar o telefone.
    telefone: Mapped[int]


def mostrar_menu() -> None:
    """Exibe o menu principal usando Rich."""
    menu = Table(show_header=False, show_edge=False, pad_edge=False, box=None)
    menu.add_column(style='bold cyan', width=3)
    menu.add_column(style='bold white')
    menu.add_row('1', 'Adicionar contato')
    menu.add_row('2', 'Atualizar contato')
    menu.add_row('3', 'Deletar contato')
    menu.add_row('4', 'Listar contatos')
    menu.add_row('5', 'Buscar contato por ID')
    menu.add_row('0', 'Sair')

    console.print(Panel(menu, title='[bold magenta]Agenda de Contatos[/]', border_style='magenta'))


def solicitar_inteiro(prompt_text: str, default: int | None = None) -> int | None:
    """Solicita um número inteiro ao usuário e trata entradas inválidas."""
    while True:
        resposta = Prompt.ask(f'[bold green]{prompt_text}[/]', default=str(default) if default is not None else None)

        if resposta == '' or resposta is None:
            return None

        try:
            return int(resposta)
        except ValueError:
            console.print('[red]Por favor, digite um número inteiro válido.[/]', justify='left')


def exibir_contatos(contatos: list[Contato]) -> None:
    """Mostra uma tabela de contatos ou uma mensagem quando a lista está vazia."""
    if not contatos:
        console.print(Panel('[yellow]Nenhum contato cadastrado.[/]', title='Lista de Contatos', border_style='yellow'))
        return

    tabela = Table(title='Contatos cadastrados', header_style='bold magenta', border_style='magenta')
    tabela.add_column('ID', style='cyan', justify='right')
    tabela.add_column('Nome', style='green')
    tabela.add_column('Email', style='blue')
    tabela.add_column('Telefone', style='white')

    for contato in contatos:
        tabela.add_row(str(contato.id), contato.nome, contato.email, str(contato.telefone))

    console.print(tabela)


def mostrar_contato(contato: Contato) -> None:
    """Exibe os dados de um único contato em um painel formatado."""
    tabela = Table(box=None)
    tabela.add_column(style='bold white')
    tabela.add_column(style='white')
    tabela.add_row('ID', str(contato.id))
    tabela.add_row('Nome', contato.nome)
    tabela.add_row('Email', contato.email)
    tabela.add_row('Telefone', str(contato.telefone))
    console.print(Panel(tabela, title='Contato Encontrado', border_style='green'))


if __name__ == '__main__':
    """Ponto de entrada do script.

    Cria o banco e administra o loop principal de interação com o usuário.
    """
    bd = BD_ORM('sqlite:///contatos.db')
    Base.metadata.create_all(bd.get_engine())

    with Session(bd.get_engine()) as session:
        console.print(Panel('[bold white]Bem-vindo ao sistema de contatos ORM[/]', title='[bold green]Agenda ORM[/]', border_style='green'))

        while True:
            mostrar_menu()
            opcao = solicitar_inteiro('Escolha uma opção')

            if opcao is None:
                console.print('[yellow]Nenhuma opção selecionada. Tente novamente.[/]')
                continue

            match opcao:
                case 1:
                    nome = Prompt.ask('[bold green]Nome[/]')
                    email = Prompt.ask('[bold green]Email[/]')
                    telefone = solicitar_inteiro('Telefone')

                    if not nome or not email or telefone is None:
                        console.print('[red]Todos os campos são obrigatórios. Tente novamente.[/]')
                        continue

                    # Cria instância do modelo Contato.
                    contato = Contato(nome=nome, email=email, telefone=telefone)
                    # Adiciona o novo objeto ao session e marca para inserção.
                    session.add(contato)
                    # Confirma a transação no banco de dados.
                    session.commit()
                    console.print('[bold green]✅ Contato adicionado com sucesso![/]')

                case 2:
                    contato_id = solicitar_inteiro('ID do contato a ser atualizado')
                    if contato_id is None:
                        console.print('[yellow]Atualização cancelada.[/]')
                        continue

                    # session.get() busca um registro pelo identificador primário.
                    contato = session.get(Contato, contato_id)
                    if not contato:
                        console.print('[red]Contato não encontrado.[/]')
                        continue

                    nome = Prompt.ask('[bold green]Nome[/]', default=contato.nome)
                    email = Prompt.ask('[bold green]Email[/]', default=contato.email)
                    telefone_text = Prompt.ask('[bold green]Telefone[/]', default=str(contato.telefone))

                    contato.nome = nome or contato.nome
                    contato.email = email or contato.email
                    try:
                        contato.telefone = int(telefone_text) if telefone_text else contato.telefone
                    except ValueError:
                        console.print('[red]Telefone inválido. Atualização cancelada.[/]')
                        continue

                    # Alterações em objetos já carregados na sessão são detectadas automaticamente.
                    session.commit()
                    console.print('[bold green]✅ Contato atualizado com sucesso![/]')

                case 3:
                    contato_id = solicitar_inteiro('ID do contato a ser deletado')
                    if contato_id is None:
                        console.print('[yellow]Exclusão cancelada.[/]')
                        continue

                    contato = session.get(Contato, contato_id)
                    if not contato:
                        console.print('[red]Contato não encontrado.[/]')
                        continue

                    confirmar = Confirm.ask('[bold red]Tem certeza que deseja deletar este contato?[/]')
                    if not confirmar:
                        console.print('[yellow]Operação cancelada.[/]')
                        continue

                    # Remove o objeto do banco de dados.
                    session.delete(contato)
                    session.commit()
                    console.print('[bold green]✅ Contato deletado com sucesso![/]')

                case 4:
                    # session.query(Contato).all() retorna todos os registros da tabela contatos.
                    contatos = session.query(Contato).all()
                    exibir_contatos(contatos)

                case 5:
                    contato_id = solicitar_inteiro('ID do contato a ser buscado')
                    if contato_id is None:
                        console.print('[yellow]Busca cancelada.[/]')
                        continue

                    contato = session.get(Contato, contato_id)
                    if contato:
                        mostrar_contato(contato)
                    else:
                        console.print('[red]Contato não encontrado.[/]')

                case 0:
                    console.print('[bold cyan]Saindo... Até logo![/]')
                    break

                case _:
                    console.print('[red]Opção inválida. Tente novamente.[/]')
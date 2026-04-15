"""Manipulação de banco de dados SQLite usando sqlite3.

O arquivo define a classe DataBase para operações CRUD simples em um arquivo
SQLite localizado na pasta data. A documentação foi padronizada para usar
docstrings adequadas em toda a classe e métodos.
"""

import sqlite3


class DataBase:
    """Classe para manipulação de banco de dados SQLite.

    A classe mantém a conexão e o cursor SQLite e fornece métodos para criar
    tabelas, inserir, atualizar, deletar e selecionar registros.
    """

    def __init__(self, banco: str):
        """Inicializa a conexão SQLite e o cursor.

        Args:
            banco: Nome do arquivo do banco de dados SQLite dentro da pasta data.
        """
        self.conn = sqlite3.connect("data/" + banco)
        self.cursor = self.conn.cursor()

    def __str__(self) -> str:
        """Retorna uma lista formatada de tabelas existentes no banco.

        Returns:
            Uma string com os nomes das tabelas encontradas no banco de dados.
        """
        result = """-------\nTabelas\n-------"""

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = self.cursor.fetchall()

        for tabela in tabelas:
            result += f'{tabela[0]}\n'

        return result

    def create_table(self, table: str, columns: dict) -> bool:
        """Cria uma tabela no banco de dados se ela não existir.

        Args:
            table: Nome da tabela a ser criada.
            columns: Dicionário com os nomes das colunas e seus tipos SQL.

        Returns:
            True se a tabela foi criada com sucesso, False caso contrário.
        """
        key = ''
        for i in columns:
            key += f'{i} {columns[i]}, '

        query = f"""
            CREATE TABLE IF NOT EXISTS {table}(
                {key[:-2]}
            );
        """

        if self.cursor.execute(query):
            self.conn.commit()
            return True
        return False

    def inserir(self, table: str, values: dict) -> bool:
        """Insere um registro em uma tabela.

        Args:
            table: Nome da tabela onde os dados serão inseridos.
            values: Dicionário com os nomes das colunas e os valores a inserir.

        Returns:
            True se a inserção for bem-sucedida, False caso contrário.
        """
        try:
            key = ''
            value = ''

            for i in values:
                key += f'{i}, '
                value += f'"{values[i]}", '

            query = f"""
                INSERT INTO {table}({key[:-2]}) VALUES({value[:-2]});
            """

            if self.cursor.execute(query):
                self.conn.commit()
                return True
            return False

        except Exception:
            return False

    def update(self, table: str, values: dict, conditions: dict) -> bool:
        """Atualiza registros existentes em uma tabela.

        Args:
            table: Nome da tabela onde os dados serão atualizados.
            values: Dicionário com os nomes das colunas e os novos valores.
            conditions: Dicionário com as condições para a atualização.

        Returns:
            True se a atualização for bem-sucedida, False caso contrário.
        """
        try:
            key = ''
            condition_parts = []

            for column, value in values.items():
                if value is not None:
                    key += f'{column} = "{value}", '

            for cond_key, cond_value in conditions.items():
                if cond_key == 'where':
                    condition_parts.append(cond_value)

            condition = f"WHERE {' AND '.join(condition_parts)}" if condition_parts else ''
            query = f"UPDATE {table} SET {key[:-2]} {condition}"

            if self.cursor.execute(query):
                self.conn.commit()
                return True
            return False

        except Exception:
            return False

    def delete(self, table: str, condition: dict) -> bool:
        """Deleta registros de uma tabela.

        Args:
            table: Nome da tabela de onde os dados serão deletados.
            condition: Dicionário com as condições para a deleção.

        Returns:
            True se a exclusão for bem-sucedida, False caso contrário.
        """
        try:
            where = ''
            for i in condition:
                where += f' where {condition[i]}' if i == 'where' else ''

            query = f"""
                DELETE FROM {table} {where}
            """

            if self.cursor.execute(query):
                self.conn.commit()
                return True
            return False

        except Exception:
            return False

    def select(self, table: str, conditions: dict = None, columns=None):
        """Seleciona registros de uma tabela com condições.

        Args:
            table: Nome da tabela de onde os dados serão selecionados.
            conditions: Dicionário com as condições para a seleção.
            columns: Lista de colunas a serem selecionadas. Se None, seleciona todas.

        Returns:
            Lista de tuplas com os registros selecionados ou False em caso de erro.
        """
        try:
            condition_parts = []
            if columns is None:
                column = '*'
            else:
                column = ', '.join(columns)

            if conditions:
                for cond_key, cond_value in conditions.items():
                    if cond_key == 'where':
                        condition_parts.append(cond_value)

            condition = f"WHERE {' AND '.join(condition_parts)}" if condition_parts else ''
            query = f"SELECT {column} FROM {table} {condition}"

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Exception:
            return False

    def select_all(self, table: str):
        """Seleciona todos os registros de uma tabela.

        Args:
            table: Nome da tabela de onde os dados serão selecionados.

        Returns:
            Lista com todos os dados da tabela ou False em caso de erro.
        """
        try:
            query = f"""
                SELECT * FROM {table}
            """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Exception:
            return False
        

def imprimir_contatos(contatos):
    """Exibe uma lista de contatos no console."""
    if not contatos:
        print('Nenhum contato encontrado.')
        return

    print('\nContatos:')
    for contato in contatos:
        print(f'ID: {contato[0]} | Nome: {contato[1]} | Email: {contato[2]} | Telefone: {contato[3]}')
    print()


def input_titulo(titulo):
    """Lê um valor de texto do usuário."""
    return input(f'{titulo}: ').strip()


def main():
    """Ponto de entrada principal da agenda de contatos."""
    db = DataBase('agenda.db')
    db.create_table(
        'contatos',
        {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'nome': 'TEXT NOT NULL',
            'email': 'TEXT NOT NULL',
            'telefone': 'TEXT NOT NULL',
        }
    )

    while True:
        print('\n--- Agenda de Contatos ---')
        print('1 - Adicionar contato')
        print('2 - Atualizar contato')
        print('3 - Deletar contato')
        print('4 - Listar contatos')
        print('5 - Buscar contato por ID')
        print('0 - Sair')

        escolha = input('Escolha uma opção: ').strip()

        if escolha == '1':
            nome = input_titulo('Nome')
            email = input_titulo('Email')
            telefone = input_titulo('Telefone')

            if not nome or not email or not telefone:
                print('Todos os campos são obrigatórios.')
                continue

            sucesso = db.inserir('contatos', {'nome': nome, 'email': email, 'telefone': telefone})
            print('Contato adicionado.' if sucesso else 'Falha ao adicionar contato.')

        elif escolha == '2':
            contato_id = input_titulo('ID do contato a atualizar')
            if not contato_id.isdigit():
                print('ID inválido.')
                continue

            registro = db.select('contatos', {'where': f'id = {contato_id}'})
            if not registro:
                print('Contato não encontrado.')
                continue

            registro = registro[0]
            nome = input_titulo(f'Nome [{registro[1]}]') or registro[1]
            email = input_titulo(f'Email [{registro[2]}]') or registro[2]
            telefone = input_titulo(f'Telefone [{registro[3]}]') or registro[3]

            sucesso = db.update('contatos', {'nome': nome, 'email': email, 'telefone': telefone}, {'where': f'id = {contato_id}'})
            print('Contato atualizado.' if sucesso else 'Falha ao atualizar contato.')

        elif escolha == '3':
            contato_id = input_titulo('ID do contato a deletar')
            if not contato_id.isdigit():
                print('ID inválido.')
                continue

            sucesso = db.delete('contatos', {'where': f'id = {contato_id}'})
            print('Contato deletado.' if sucesso else 'Falha ao deletar contato.')

        elif escolha == '4':
            contatos = db.select_all('contatos')
            imprimir_contatos(contatos)

        elif escolha == '5':
            contato_id = input_titulo('ID do contato a buscar')
            if not contato_id.isdigit():
                print('ID inválido.')
                continue

            contato = db.select('contatos', {'where': f'id = {contato_id}'})
            imprimir_contatos(contato)

        elif escolha == '0':
            print('Saindo...')
            break

        else:
            print('Opção inválida. Tente novamente.')


if __name__ == '__main__':
    main()

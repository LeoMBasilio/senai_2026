class Pokemon:
    '''
        construtor - nome e tipo
        método - usar_ataque() - retorna uma string dizendo que o pokemon usou um ataque do tipo X, onde X é o tipo do pokemon
    '''
    def __init__(self, nome, tipo): # construtor sempre tem o nome __init__
        self.nome = nome # self é uma referência ao objeto que está sendo criado, ou seja, o pokemon que estamos criando. O nome do pokemon é passado como argumento para o construtor e é atribuído ao atributo nome do objeto. O mesmo acontece com o tipo do pokemon, que é passado como argumento e atribuído ao atributo tipo do objeto.
        self.tipo = tipo

    def Usar_Ataque(self): # método que retorna uma string dizendo que o pokemon usou um ataque do tipo X, onde X é o tipo do pokemon. O método usa os atributos nome e tipo do objeto para construir a string de retorno.
        return f"{self.nome} usou um ataque do tipo {self.tipo}"
    
if __name__ == '__main__':
    pokemon = Pokemon('pikachu', 'eletrico') # criando um objeto pokemon da classe Pokemon, passando o nome 'pikachu' e o tipo 'eletrico' como argumentos para o construtor. O objeto pokemon é criado com os atributos nome e tipo definidos como 'pikachu' e 'eletrico', respectivamente.

    print(pokemon.Usar_Ataque()) # chamando o método Usar_Ataque() do objeto pokemon, que retorna a string "pikachu usou um ataque do tipo eletrico". A string é impressa na tela usando a função print().
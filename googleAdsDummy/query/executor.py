from googleAdsDummy.engine.world import World


class Executor:
    def __init__(self):
        self.dispatchDict ={
            'from_clause': self.handle_from,
            'select': self.handle_select,
        }
    def consultData(self, world: World, ast: dict) -> dict:
        self.world = world
        self.ast = ast

        for key, value in ast.items():
            print(key, value)
            # tenta usar um dicionário de dispatch
            # se não achar o nó no dicionário levanta um erro
            # se achar o dicionáiro, usa a função.
        return {}
    
    def handle_from(self):
        ...

    def handle_select(self):
        ...

class Action:
    def __init__(self, action_type: str, target_node_id: str = None, distance_traveled: int = 0, action_time: int = 0):
            #EXEMPLO: fuel, move, supply, restock, wait
        self.action_type = action_type
            #EXMPLO: B, F, E; NOTA: apenas ultilizada no "move"
        self.target_node_id = target_node_id
            #EXEMPLO: a distância a ser percorrida em determinada ação; NOTA: apenas ultilizada no "move"
        self.distance_traveled = distance_traveled
            #EXEMPLO: 15, 30, 400; NOTA: esse tempo é o tempo atual + o tempo da ação
        self.action_time = action_time

    def __str__(self):
        return (
            f"Action(type={self.action_type}, "
            f"target_node={self.target_node_id}, "
            f"distance={self.distance_traveled}, "
            f"time={self.action_time})"
        )

    def __repr__(self):
        return str(self)


    """ Exemplo:
            Criar uma ação para reabastecer
            fuel_action = Action(action_type="fuel")
        
            Criar uma ação para mover o veículo para o nó "B"
            move_action = Action(action_type="move", target_node_id="B", distance_traveled=10, action_time=15)
        
            Criar uma ação para entregar suprimentos
            supply_action = Action(action_type="supply")
            
            Criar uma ação de reeabastecer suprimentos
            supply_action = Action(action_type="restock", action_time=15)
            
            Ação de espera
            wait_action = Action(action_type="wait")
    """
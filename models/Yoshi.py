
class Yoshi:
    def __init__(self, world, parent, operator, depth, isMax, heuristic):
        """
        Inicializa una instancia de la clase Yoshi, que representa un nodo
        en los algoritmos de búsqueda.

        Args:
            world (World): El mundo en el que se encuentra el Yoshi.
            parent (Yoshi): El Yoshi padre.
            operator (int): El operador utilizado para llegar a esta instancia.
            depth (int): La profundidad de esta instancia en el árbol de búsqueda.
            cost (float): El costo de esta instancia.
            fuel (int): La cantidad de combustible del Yoshi.
        """
        self.world = world
        self.parent = parent
        self.operator = operator
        self.depth = depth
        self.current_position = world.start_position
        self.isMax = True

    def move(self, new_position):
        """
        Mueve al Yoshi a una nueva posición.

        Args:
            new_position (Position): La nueva posición a la que se moverá el Yoshi.
        """
        self.current_position = new_position

    # Los movimientos tipo caballo para yoshi, usando los métodos de la clase Position
    def move_up_right(self):
        """
        Mueve al Yoshi hacia arriba (2) y hacia la derecha (1).
        """
        new_position = self.current_position.move_up_right()
        if self.world.is_within_bounds(new_position):
            self.move(new_position)

    def move_right_up(self):
        """
        Mueve al Yoshi hacia la derecha (2) y hacia arriba (1).
        """
        new_position = self.current_position.move_right_up()
        if self.world.is_within_bounds(new_position):
            self.move(new_position)

    def move_right_down(self):
        """
        Mueve al Yoshi hacia la derecha (2) y hacia abajo (1).
        """
        new_position = self.current_position.move_right_down()
        if self.world.is_within_bounds(new_position):
            self.move(new_position)

    def move_down_right(self):
        """
        Mueve al Yoshi hacia abajo (2) y hacia la derecha (1).
        """
        new_position = self.current_position.move_down_right()
        if self.world.is_within_bounds(new_position):
            self.move(new_position)

    def move_down_left(self):
        """
        Mueve al Yoshi hacia abajo (2) y hacia la izquierda (1).
        """
        new_position = self.current_position.move_down_left()
        if self.world.is_within_bounds(new_position):
            self.move(new_position)

    def move_left_down(self):
        """
        Mueve al Yoshi hacia la izquierda (2) y hacia abajo (1).
        """
        new_position = self.current_position.move_left_down()
        if self.world.is_within_bounds(new_position):
            self.move(new_position)

    def move_left_up(self):
        """
        Mueve al Yoshi hacia la izquierda (2) y hacia arriba (1).
        """
        new_position = self.current_position.move_left_up()
        if self.world.is_within_bounds(new_position):
            self.move(new_position)

    def move_up_left(self):
        """
        Mueve al Yoshi hacia arriba (2) y hacia la izquierda (1).
        """
        new_position = self.current_position.move_up_left()
        if self.world.is_within_bounds(new_position):
            self.move(new_position)

    # ... rest of your methods ...

    def calculate_cost(self, position):
        """
        Calcula el costo para moverse a una posición específica.

        Args:
            position (Position): La posición a la que se desea mover.

        Returns:
            float: El costo para moverse a la posición especificada.
        """
        if self.in_ship and self.fuel > 0:
            return 0.5
        elif self.world.is_enemy(position):
            return 5
        return 1

    def heuristic(self):
        """
        Calcula la heurística para el problema de búsqueda.
        Args:
        mando_pos (Position): La posición actual del Yoshi.
        grogu_pos (Position): La posición de Grogu.
        ship_pos (Position): La posición de la nave.

        Returns:
        float: La heurística para el problema de búsqueda.
        """
        manhattan_mando_grogu = self.current_position.manhattan_distance(self.world.grogu_position)
        if self.world.ship_position is not None:
            manhattan_mando_nave = self.current_position.manhattan_distance(self.world.ship_position)
            manhattan_nave_grogu = self.world.ship_position.manhattan_distance(self.world.grogu_position)
            if manhattan_nave_grogu <= 10:
                h1 = manhattan_mando_nave + manhattan_nave_grogu * 0.5
            else:
                h1 = manhattan_mando_nave + manhattan_nave_grogu - 5
            return min(h1, manhattan_mando_grogu)
        elif self.in_ship:
            if manhattan_mando_grogu <= 10:
                h1 = manhattan_mando_grogu * 0.5
            else:
                h1 = manhattan_mando_grogu - 5
            return h1
        else:
            return manhattan_mando_grogu

    def simple_heuristic(self):
        """
        Calcula la heurística para el problema de búsqueda.
        Args:
        mando_pos (Position): La posición actual del Yoshi.
        grogu_pos (Position): La posición de Grogu.
        ship_pos (Position): La posición de la nave.

        Returns:
        float: La heurística para el problema de búsqueda.
        """
        return self.current_position.manhattan_distance(self.world.grogu_position)

    def expand(self, algorithm):
        """
        Obtiene los posibles movimientos que puede realizar el Yoshi.

        Returns:
            list[Yoshi]: Lista de instancias de Yoshi que representan los posibles movimientos.
        """
        moves = []
        position = self.current_position
        world = self.world
        new_fuel = 0
        if self.world.in_ship(position):
            self.in_ship = True
            self.fuel = 10
            self.world.remove_ship()
        if self.in_ship:
            new_fuel = self.fuel - 1
        if algorithm == 'bfs' or algorithm == 'ucs' or algorithm == 'dfs':
            heuristic = None
        else:
            heuristic = self.heuristic()
        up_cost = self.cost + self.calculate_cost(position.move_up())
        down_cost = self.cost + self.calculate_cost(position.move_down())
        left_cost = self.cost + self.calculate_cost(position.move_left())
        right_cost = self.cost + self.calculate_cost(position.move_right())
        if world.is_within_bounds(position.move_right()) and not world.is_wall(position.move_right()):
            new_mandalorian = Yoshi(world, self, 0, self.depth + 1, right_cost, new_fuel, heuristic)
            new_mandalorian.current_position = position.move_right()
            new_mandalorian.operator = 4
            moves.append(new_mandalorian)
        if world.is_within_bounds(position.move_left()) and not world.is_wall(position.move_left()):
            new_mandalorian = Yoshi(world, self, 0, self.depth + 1, left_cost, new_fuel, heuristic)
            new_mandalorian.current_position = position.move_left()
            new_mandalorian.operator = 3
            moves.append(new_mandalorian)
        if world.is_within_bounds(position.move_down()) and not world.is_wall(position.move_down()):
            new_mandalorian = Yoshi(world, self, 0, self.depth + 1, down_cost, new_fuel, heuristic)
            new_mandalorian.current_position = position.move_down()
            new_mandalorian.operator = 2
            moves.append(new_mandalorian)
        if world.is_within_bounds(position.move_up()) and not world.is_wall(position.move_up()):
            new_mandalorian = Yoshi(world, self, 0, self.depth + 1, up_cost, new_fuel, heuristic)
            new_mandalorian.current_position = position.move_up()
            new_mandalorian.operator = 1
            moves.append(new_mandalorian)
        return moves

    def found_grogu(self):
        """
        Verifica si el Yoshi ha encontrado a Grogu.

        Returns:
            bool: True si el Yoshi ha encontrado a Grogu, False en caso contrario.
        """
        return self.current_position == self.world.grogu_position

    def solution(self):
        """
        Reconstruye la solución a partir del nodo meta.

        Returns:
            list[Position]: La lista de posiciones en el camino.
        """
        path = []
        current = self
        while current.parent is not None:
            path.append(current.current_position)
            current = current.parent
        path.append(current.current_position)
        path.reverse()
        return path

    def __eq__(self, other):
        """
        Compara si dos instancias de Yoshi son iguales.

        Args:
            other (Yoshi): La otra instancia de Yoshi a comparar.

        Returns:
            bool: True si las instancias son iguales, False en caso contrario.
        """
        if isinstance(other, Yoshi):
            return (self.current_position == other.current_position) and (self.in_ship == other.in_ship)
        return False

    def __hash__(self):
        """
        Calcula el hash de la instancia de Yoshi.

        Returns:
            int: El hash de la instancia de Yoshi.
        """
        return hash((self.current_position, self.in_ship))
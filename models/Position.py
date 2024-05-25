class Position:
    def __init__(self, row, column):
        """
        Crea una nueva instancia de la clase Position.

        Args:
            row (int): La fila de la posición.
            column (int): La columna de la posición.
        """
        self.row = row
        self.column = column

    # Los posibles movimientos tipo 'caballo' en un tablero de ajedrez.
    # Se definen en el sentido de las manecillas del reloj.
    def move_up_right(self):
        """
        Mueve la posición hacia arriba (2) y hacia la derecha (1).

        Returns:
            Position: La nueva posición después del movimiento.
        """
        return Position(self.row - 2, self.column + 1)

    def move_right_up(self):
        """
        Mueve la posición hacia la derecha (2) y hacia arriba (1).

        Returns:
            Position: La nueva posición después del movimiento.
        """
        return Position(self.row - 1, self.column + 2)

    def move_right_down(self):
        """
        Mueve la posición hacia la derecha (2) y hacia abajo (1).

        Returns:
            Position: La nueva posición después del movimiento.
        """
        return Position(self.row + 1, self.column + 2)

    def move_down_right(self):
        """
        Mueve la posición hacia abajo (2) y hacia la derecha (1).

        Returns:
            Position: La nueva posición después del movimiento.
        """
        return Position(self.row + 2, self.column + 1)

    def move_down_left(self):
        """
        Mueve la posición hacia abajo (2) y hacia la izquierda (1).

        Returns:
            Position: La nueva posición después del movimiento.
        """
        return Position(self.row + 2, self.column - 1)

    def move_left_down(self):
        """
        Mueve la posición hacia la izquierda (2) y hacia abajo (1).

        Returns:
            Position: La nueva posición después del movimiento.
        """
        return Position(self.row + 1, self.column - 2)

    def move_left_up(self):
        """
        Mueve la posición hacia la izquierda (2) y hacia arriba (1).

        Returns:
            Position: La nueva posición después del movimiento.
        """
        return Position(self.row - 1, self.column - 2)

    def move_up_left(self):
        """
        Mueve la posición hacia arriba (2) y hacia la izquierda (1).

        Returns:
            Position: La nueva posición después del movimiento.
        """
        return Position(self.row - 2, self.column - 1)

    # ... rest of your methods ...

    def is_within(self, dimension):
        """
        Verifica si la posición está dentro de los límites de una dimensión dada.

        Args:
            dimension (tuple): Una tupla que representa las dimensiones (filas, columnas).

        Returns:
            bool: True si la posición está dentro de los límites, False de lo contrario.
        """
        filas, columnas = dimension
        return 0 <= self.row < filas and 0 <= self.column < columnas
    
    def manhattan_distance(self, other):
        """
        Calcula la distancia de Manhattan entre dos posiciones.

        Args:
            other (Position): La otra posición.

        Returns:
            int: La distancia de Manhattan entre las dos posiciones.
        """
        return abs(self.row - other.row) + abs(self.column - other.column)

    def __eq__(self, other):
        """
        Compara si dos posiciones son iguales.

        Args:
            other (Position): La otra posición a comparar.

        Returns:
            bool: True si las posiciones son iguales, False de lo contrario.
        """
        return isinstance(other, Position) and self.row == other.row and self.column == other.column

    def __hash__(self):
        """
        Calcula el hash de la posición.

        Returns:
            int: El hash de la posición.
        """
        return hash((self.row, self.column))

    def __repr__(self):
        """
        Devuelve una representación en cadena de la posición.

        Returns:
            str: La representación en cadena de la posición.
        """
        return f"({self.row}, {self.column})"
    
import math
from random import randint


class QuadraticEquations():
    def __init__(self) -> None:
        pass

    def solve_quadratic(self, a, b=None, c=None):
        """Решение квадратного уравнения

        Args:
            a (__int__): Член квадратного уравнения
            b (__int__), optional): Член квадратного уравнения.
                                    Defaults to None.
            c (__int__), optional): Член квадратного уравнения.
                                    Defaults to None.

        Returns:
            _tuple_: discriminant, None - Корней нет
            _tuple_: discriminant, x - Один корень
            _tuple_: discriminant, x1, x2 - Полное квадратное уравнение
        """
        if b is None and c is None:  # Если не заданы b и c
            c = a
            a = 1
            b = 0
        elif c is None:  # Если не задан c
            c = b
            b = 0

        discriminant = b**2 - 4*a*c

        if discriminant > 0:  # Два корня
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return discriminant, x1, x2
        elif discriminant == 0:  # Один корень
            x = -b / (2*a)
            return discriminant, x
        else:  # Нет реальных корней
            return discriminant, None

    def get_equations_numbers(self):
        a = randint(1, 2)
        b = randint(-15, 15)
        c = randint(-15, 4)
        return a, b, c

    def get_equation(self) -> tuple:
        while True:
            a, b, c = self.get_equations_numbers()
            if a == 0 or b == 0 or c == 0:
                continue
            result = self.solve_quadratic(a, b, c)
            if result[1] is None:
                root_count = 0
                break
            try:
                if result[1].is_integer() and result[2].is_integer():
                    root_count = 2
                    break
            except Exception:
                if result[1].is_integer():
                    root_count = 1
                    break
        if a == 1:
            a = ''
        if b > 0:
            b = f"+{b}"
        if c > 0:
            c = f"+{c}"
        return f"{a}x²{b}x{c}=0", root_count, result

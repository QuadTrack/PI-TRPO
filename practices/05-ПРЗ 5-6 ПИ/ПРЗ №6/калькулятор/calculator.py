"""
Модуль калькулятора для выполнения базовых арифметических операций.
Используется для обучения написанию модульных тестов.
"""

def add(a, b):
    """
    Сложение двух чисел.
    
    Args:
        a: Первое число
        b: Второе число
    
    Returns:
        Сумма a и b
    """
    return a + b


def subtract(a, b):
    """
    Вычитание двух чисел.
    
    Args:
        a: Уменьшаемое
        b: Вычитаемое
    
    Returns:
        Разность a и b
    """
    return a - b


def multiply(a, b):
    """
    Умножение двух чисел.
    
    Args:
        a: Первый множитель
        b: Второй множитель
    
    Returns:
        Произведение a и b
    """
    return a * b


def divide(a, b):
    """
    Деление двух чисел.
    
    Args:
        a: Делимое
        b: Делитель
    
    Returns:
        Частное a и b
    
    Raises:
        ValueError: Если делитель равен нулю
    """
    if b == 0:
        raise ValueError("Делитель не может быть равен нулю!")
    return a / b


def power(base, exponent):
    """
    Возведение числа в степень (только для целых неотрицательных степеней).
    
    Args:
        base: Основание
        exponent: Показатель степени
    
    Returns:
        base в степени exponent
    
    Raises:
        ValueError: Если показатель степени отрицательный
    """
    if exponent < 0:
        raise ValueError("Показатель степени не может быть отрицательным!")
    
    result = 1
    for _ in range(exponent):
        result *= base
    return result


def calculate(operation, x, y):
    """
    Основная функция калькулятора для выполнения операций.
    
    Args:
        operation: Строка с названием операции ('add', 'subtract', 'multiply', 'divide', 'power')
        x: Первое число
        y: Второе число
    
    Returns:
        Результат операции
    
    Raises:
        ValueError: Если операция неизвестна
    """
    operations = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'power': power
    }
    
    if operation not in operations:
        raise ValueError(f"Неизвестная операция: {operation}")
    
    return operations[operation](x, y)


def is_even(number):
    """
    Проверка, является ли число четным.
    
    Args:
        number: Проверяемое число
    
    Returns:
        True если число четное, иначе False
    """
    return number % 2 == 0


def factorial(n):
    """
    Вычисление факториала числа.
    
    Args:
        n: Неотрицательное целое число
    
    Returns:
        Факториал числа n
    
    Raises:
        ValueError: Если n отрицательное
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел!")
    
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


# Пример использования
if __name__ == "__main__":
    print("🔢 Демонстрация работы калькулятора:")
    
    test_cases = [
        ('add', 5, 3),
        ('subtract', 10, 4),
        ('multiply', 7, 6),
        ('divide', 15, 3),
        ('power', 2, 3)
    ]
    
    for op, x, y in test_cases:
        try:
            result = calculate(op, x, y)
            print(f"{op}({x}, {y}) = {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"{op}({x}, {y}) -> Ошибка: {e}")
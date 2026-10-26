"""
Модульные тесты для калькулятора.
Запуск: pytest test_calculator.py -v
"""

import pytest
from calculator import add, subtract, multiply, divide, power, calculate, is_even, factorial


class TestBasicOperations:
    """Тесты базовых арифметических операций"""
    
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел"""
        assert add(2, 3) == 5
        assert add(10, 5) == 15
    
    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел"""
        assert add(-2, -3) == -5
        assert add(-5, 10) == 5
    
    def test_subtract_numbers(self):
        """Тест вычитания"""
        assert subtract(10, 4) == 6
        assert subtract(5, 8) == -3
    
    def test_multiply_numbers(self):
        """Тест умножения"""
        assert multiply(3, 4) == 12
        assert multiply(-2, 5) == -10
        assert multiply(0, 100) == 0
    
    def test_divide_numbers(self):
        """Тест деления"""
        assert divide(10, 2) == 5
        assert divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        """Тест деления на ноль - должен вызывать исключение"""
        with pytest.raises(ValueError, match="Делитель не может быть равен нулю!"):
            divide(10, 0)


class TestPowerOperation:
    """Тесты операции возведения в степень"""
    
    def test_power_positive_exponent(self):
        """Тест возведения в положительную степень"""
        assert power(2, 3) == 8
        assert power(5, 2) == 25
        assert power(10, 0) == 1  # Любое число в степени 0 = 1
    
    def test_power_negative_exponent(self):
        """Тест возведения в отрицательную степень - должен вызывать исключение"""
        with pytest.raises(ValueError, match="Показатель степени не может быть отрицательным!"):
            power(2, -3)


class TestCalculateFunction:
    """Тесты основной функции calculate"""
    
    def test_calculate_add(self):
        """Тест calculate с операцией сложения"""
        assert calculate('add', 5, 3) == 8
    
    def test_calculate_subtract(self):
        """Тест calculate с операцией вычитания"""
        assert calculate('subtract', 10, 4) == 6
    
    def test_calculate_multiply(self):
        """Тест calculate с операцией умножения"""
        assert calculate('multiply', 3, 4) == 12
    
    def test_calculate_divide(self):
        """Тест calculate с операцией деления"""
        assert calculate('divide', 15, 3) == 5
    
    def test_calculate_power(self):
        """Тест calculate с операцией возведения в степень"""
        assert calculate('power', 2, 3) == 8
    
    def test_calculate_unknown_operation(self):
        """Тест calculate с неизвестной операцией - должен вызывать исключение"""
        with pytest.raises(ValueError, match="Неизвестная операция: unknown"):
            calculate('unknown', 5, 3)
    
    def test_calculate_divide_by_zero_via_calculate(self):
        """Тест деления на ноль через calculate"""
        with pytest.raises(ValueError):
            calculate('divide', 10, 0)


class TestAdditionalFunctions:
    """Тесты дополнительных функций"""
    
    def test_is_even(self):
        """Тест проверки четности числа"""
        assert is_even(4) == True
        assert is_even(7) == False
        assert is_even(0) == True  # 0 считается четным
    
    def test_factorial_positive(self):
        """Тест вычисления факториала для положительных чисел"""
        assert factorial(0) == 1   # 0! = 1
        assert factorial(1) == 1
        assert factorial(5) == 120
    
    def test_factorial_negative(self):
        """Тест факториала для отрицательных чисел - должен вызывать исключение"""
        with pytest.raises(ValueError, match="Факториал определен только для неотрицательных чисел!"):
            factorial(-5)


class TestEdgeCases:
    """Тесты граничных случаев и особых ситуаций"""
    
    def test_floating_point_operations(self):
        """Тест операций с числами с плавающей точкой"""
        # Внимание: из-за точности чисел с плавающей точкой используем приближенное сравнение
        assert add(0.1, 0.2) == pytest.approx(0.3)
        assert subtract(0.3, 0.1) == pytest.approx(0.2)
    
    def test_large_numbers(self):
        """Тест работы с большими числами"""
        assert add(1000000, 2000000) == 3000000
        assert multiply(1000, 1000) == 1000000
    
    def test_zero_operations(self):
        """Тест операций с нулем"""
        assert add(0, 5) == 5
        assert multiply(0, 100) == 0
        assert subtract(5, 0) == 5


# Дополнительные тесты для демонстрации параметризации
@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300)
])
def test_add_parameterized(a, b, expected):
    """Параметризованный тест для сложения"""
    assert add(a, b) == expected


@pytest.mark.parametrize("operation,a,b,expected", [
    ('add', 2, 3, 5),
    ('subtract', 10, 4, 6),
    ('multiply', 3, 4, 12),
    ('divide', 15, 3, 5),
])
def test_calculate_parameterized(operation, a, b, expected):
    """Параметризованный тест для функции calculate"""
    assert calculate(operation, a, b) == expected


if __name__ == "__main__":
    # Запуск тестов напрямую через Python (альтернатива pytest)
    pytest.main([__file__, "-v"])

---

## 5. Дополнительный файл для Mock-тестирования (`test_with_mocks.py`)

```python
"""
Примеры тестов с использованием Mock объектов
"""

import pytest
from unittest.mock import Mock, patch
from calculator import calculate, add


class TestWithMocks:
    """Тесты с использованием Mock объектов"""
    
    def test_calculate_calls_correct_function(self):
        """Тест, что calculate вызывает правильную функцию"""
        # Создаем mock-функцию для сложения
        mock_add = Mock(return_value=10)
        
        # Временно заменяем функцию add на mock
        with patch('calculator.add', mock_add):
            result = calculate('add', 3, 7)
            
            # Проверяем, что mock был вызван с правильными аргументами
            mock_add.assert_called_once_with(3, 7)
            assert result == 10
    
    def test_mock_exception(self):
        """Тест с mock, который вызывает исключение"""
        mock_divide = Mock(side_effect=ValueError("Деление на ноль!"))
        
        with patch('calculator.divide', mock_divide):
            with pytest.raises(ValueError, match="Деление на ноль!"):
                calculate('divide', 10, 0)
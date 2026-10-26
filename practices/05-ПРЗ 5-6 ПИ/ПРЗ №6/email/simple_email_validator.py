"""
Упрощенный валидатор email без внешних зависимостей.
Идеально подходит для базового обучения.
"""

import re
from typing import List, Optional


class SimpleEmailValidator:
    """
    Упрощенный валидатор email для базовой проверки.
    """
    
    # Базовое регулярное выражение
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Список disposable доменов
    DISPOSABLE_DOMAINS = [
        'tempmail.com', '10minutemail.com', 'mailinator.com',
        'throwawaymail.com', 'yopmail.com', 'guerrillamail.com'
    ]

    def __init__(self):
        self.regex = re.compile(self.EMAIL_PATTERN)

    def validate(self, email: str) -> bool:
        """
        Базовая проверка email.
        
        Args:
            email: Email для проверки
            
        Returns:
            bool: True если email валидный
        """
        if not email or not isinstance(email, str):
            return False
        
        # Проверка длины
        if len(email) > 254:
            return False
        
        # Проверка формата
        if not self.regex.match(email):
            return False
        
        # Проверка disposable доменов
        domain = email.split('@')[1].lower()
        if domain in self.DISPOSABLE_DOMAINS:
            return False
        
        return True

    def get_validation_details(self, email: str) -> dict:
        """
        Получение деталей валидации.
        
        Args:
            email: Email для проверки
            
        Returns:
            dict: Детали проверки
        """
        result = {
            'email': email,
            'is_valid': False,
            'has_correct_format': False,
            'has_valid_domain': False,
            'is_disposable': False,
            'errors': []
        }
        
        if not email or not isinstance(email, str):
            result['errors'].append('Email должен быть непустой строкой')
            return result
        
        if len(email) > 254:
            result['errors'].append('Email слишком длинный')
            return result
        
        # Проверка формата
        if not self.regex.match(email):
            result['errors'].append('Неверный формат email')
            return result
        
        result['has_correct_format'] = True
        
        # Проверка домена
        try:
            domain = email.split('@')[1].lower()
            result['is_disposable'] = domain in self.DISPOSABLE_DOMAINS
            
            if result['is_disposable']:
                result['errors'].append('Disposable email не разрешены')
                return result
            
            result['has_valid_domain'] = True
            result['is_valid'] = True
            
        except IndexError:
            result['errors'].append('Не удалось извлечь домен')
        
        return result


# Функции для простого использования
def is_valid_simple_email(email: str) -> bool:
    """
    Простая проверка email.
    
    Args:
        email: Email для проверки
        
    Returns:
        bool: True если email валидный
    """
    validator = SimpleEmailValidator()
    return validator.validate(email)


# Пример использования
if __name__ == "__main__":
    test_emails = [
        "user@example.com",
        "invalid-email",
        "user@tempmail.com",
        "test@gmail.com",
        "verylongemailaddress" + "a"*100 + "@example.com"
    ]
    
    print("🔍 Тестирование упрощенного валидатора email:")
    print("-" * 50)
    
    validator = SimpleEmailValidator()
    
    for email in test_emails:
        result = validator.get_validation_details(email)
        status = "✅ ВАЛИДНЫЙ" if result['is_valid'] else "❌ НЕВАЛИДНЫЙ"
        
        print(f"Email: {email}")
        print(f"Статус: {status}")
        print(f"Формат: {'✅' if result['has_correct_format'] else '❌'}")
        print(f"Домен: {'✅' if result['has_valid_domain'] else '❌'}")
        if result['errors']:
            print(f"Ошибки: {', '.join(result['errors'])}")
        print("-" * 30)
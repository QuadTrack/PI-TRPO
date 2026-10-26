"""
Модуль для валидации email адресов.
Реализует различные стратегии проверки корректности email.
"""

import re
from typing import List, Optional
import dns.resolver
import socket


class EmailValidator:
    """
    Класс для валидации email адресов с различными уровнями проверки.
    """
    
    # Базовое регулярное выражение для проверки формата email
    BASIC_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Список популярных доменов для дополнительной проверки
    POPULAR_DOMAINS = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
        'mail.ru', 'yandex.ru', 'rambler.ru'
    ]
    
    # Спис disposable (временных) email доменов
    DISPOSABLE_DOMAINS = [
        'tempmail.com', '10minutemail.com', 'guerrillamail.com',
        'mailinator.com', 'throwawaymail.com', 'yopmail.com'
    ]

    def __init__(self, check_mx: bool = False, check_disposable: bool = True):
        """
        Инициализация валидатора.
        
        Args:
            check_mx: Проверять MX записи домена
            check_disposable: Проверять на disposable email
        """
        self.check_mx = check_mx
        self.check_disposable = check_disposable
        self._basic_regex = re.compile(self.BASIC_PATTERN)

    def validate_format(self, email: str) -> bool:
        """
        Проверка базового формата email.
        
        Args:
            email: Email для проверки
            
        Returns:
            bool: True если формат корректный
        """
        if not email or not isinstance(email, str):
            return False
        
        # Проверка длины
        if len(email) > 254:  # RFC 5321 ограничение
            return False
        
        # Проверка базового формата
        if not self._basic_regex.match(email):
            return False
        
        # Проверка на несколько точек подряд в доменной части
        if '..' in email.split('@')[1]:
            return False
        
        return True

    def validate_domain(self, email: str) -> bool:
        """
        Проверка доменной части email.
        
        Args:
            email: Email для проверки
            
        Returns:
            bool: True если домен корректный
        """
        if not self.validate_format(email):
            return False
        
        domain = email.split('@')[1]
        
        # Проверка на disposable email
        if self.check_disposable and self._is_disposable_domain(domain):
            return False
        
        # Проверка MX записей
        if self.check_mx:
            return self._check_mx_records(domain)
        
        return True

    def _is_disposable_domain(self, domain: str) -> bool:
        """
        Проверка является ли домен disposable.
        
        Args:
            domain: Домен для проверки
            
        Returns:
            bool: True если домен disposable
        """
        return domain.lower() in self.DISPOSABLE_DOMAINS

    def _check_mx_records(self, domain: str) -> bool:
        """
        Проверка MX записей домена.
        
        Args:
            domain: Домен для проверки
            
        Returns:
            bool: True если MX записи существуют
        """
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return len(mx_records) > 0
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, 
                dns.resolver.NoNameservers, dns.resolver.Timeout):
            return False
        except Exception:
            return False

    def get_email_parts(self, email: str) -> Optional[dict]:
        """
        Разбор email на составные части.
        
        Args:
            email: Email для разбора
            
        Returns:
            dict: Словарь с частями email или None если невалидный
        """
        if not self.validate_format(email):
            return None
        
        local_part, domain = email.split('@')
        
        return {
            'local_part': local_part,
            'domain': domain,
            'is_popular_domain': domain.lower() in self.POPULAR_DOMAINS,
            'is_disposable': self._is_disposable_domain(domain)
        }

    def validate_comprehensive(self, email: str) -> dict:
        """
        Комплексная проверка email.
        
        Args:
            email: Email для проверки
            
        Returns:
            dict: Результаты всех проверок
        """
        result = {
            'email': email,
            'is_valid_format': False,
            'is_valid_domain': False,
            'has_mx_records': False,
            'is_disposable': False,
            'is_popular_domain': False,
            'errors': []
        }
        
        # Проверка формата
        if not self.validate_format(email):
            result['errors'].append('Неверный формат email')
            return result
        
        result['is_valid_format'] = True
        
        # Разбор email
        parts = self.get_email_parts(email)
        if parts:
            result['is_disposable'] = parts['is_disposable']
            result['is_popular_domain'] = parts['is_popular_domain']
        
        # Проверка disposable домена
        if result['is_disposable'] and self.check_disposable:
            result['errors'].append('Disposable email не разрешены')
            return result
        
        # Проверка домена
        if not self.validate_domain(email):
            result['errors'].append('Проблемы с доменом')
            return result
        
        result['is_valid_domain'] = True
        
        # Проверка MX записей
        if self.check_mx:
            domain = email.split('@')[1]
            result['has_mx_records'] = self._check_mx_records(domain)
            if not result['has_mx_records']:
                result['errors'].append('Домен не имеет MX записей')
        
        return result


# Функции для простого использования без создания экземпляра класса
def is_valid_email(email: str, check_mx: bool = False) -> bool:
    """
    Простая проверка валидности email.
    
    Args:
        email: Email для проверки
        check_mx: Проверять MX записи
        
    Returns:
        bool: True если email валидный
    """
    validator = EmailValidator(check_mx=check_mx)
    return validator.validate_domain(email)


def validate_email_detailed(email: str, check_mx: bool = False) -> dict:
    """
    Детальная проверка email.
    
    Args:
        email: Email для проверки
        check_mx: Проверять MX записи
        
    Returns:
        dict: Детальные результаты проверки
    """
    validator = EmailValidator(check_mx=check_mx)
    return validator.validate_comprehensive(email)


# Пример использования
if __name__ == "__main__":
    test_emails = [
        "user@example.com",
        "invalid-email",
        "user@disposable.com",
        "test@gmail.com"
    ]
    
    print("🔍 Тестирование валидатора email:")
    print("-" * 50)
    
    for email in test_emails:
        result = validate_email_detailed(email, check_mx=False)
        status = "✅ ВАЛИДНЫЙ" if result['is_valid_format'] and result['is_valid_domain'] else "❌ НЕВАЛИДНЫЙ"
        
        print(f"Email: {email}")
        print(f"Статус: {status}")
        print(f"Формат: {'✅' if result['is_valid_format'] else '❌'}")
        print(f"Домен: {'✅' if result['is_valid_domain'] else '❌'}")
        if result['errors']:
            print(f"Ошибки: {', '.join(result['errors'])}")
        print("-" * 30)
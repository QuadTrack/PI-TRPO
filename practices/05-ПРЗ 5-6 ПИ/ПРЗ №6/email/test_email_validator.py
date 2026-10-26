"""
Модульные тесты для валидатора email.
Запуск: pytest test_email_validator.py -v
"""

import pytest
from unittest.mock import patch, Mock
from email_validator import EmailValidator, is_valid_email, validate_email_detailed


class TestEmailFormatValidation:
    """Тесты проверки формата email"""
    
    def test_valid_emails(self):
        """Тест валидных email адресов"""
        validator = EmailValidator()
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user@sub.example.com",
            "u@example.com",
            "user@example.co.uk",
            "user@example.museum"
        ]
        
        for email in valid_emails:
            assert validator.validate_format(email) == True, f"Email {email} должен быть валидным"
    
    def test_invalid_emails(self):
        """Тест невалидных email адресов"""
        validator = EmailValidator()
        invalid_emails = [
            "invalid-email",           # Нет @ и домена
            "user@",                   # Нет домена
            "@example.com",            # Нет локальной части
            "user@.com",               # Нет домена
            "user@example..com",       # Двойная точка в домене
            "user@example.c",          # Слишком короткий домен
            "user@-example.com",       # Дефис в начале домена
            "user@example-.com",       # Дефис в конце домена
            "",                        # Пустая строка
            None,                      # None
            "user@example_com",        # Подчеркивание в домене
            "user name@example.com",   # Пробел в локальной части
            "user@example..com",       # Двойная точка
            "a" * 100 + "@example.com" # Слишком длинный email
        ]
        
        for email in invalid_emails:
            if email is not None:  # Пропускаем None для проверки типа
                assert validator.validate_format(email) == False, f"Email {email} должен быть невалидным"
    
    def test_email_length_validation(self):
        """Тест проверки длины email"""
        validator = EmailValidator()
        
        # Слишком длинный email
        long_email = "a" * 250 + "@example.com"
        assert validator.validate_format(long_email) == False
        
        # Максимально допустимая длина
        max_length_email = "a" * 245 + "@ex.com"  # 254 символа
        assert validator.validate_format(max_length_email) == True


class TestDomainValidation:
    """Тесты проверки доменной части"""
    
    def test_disposable_domains(self):
        """Тест disposable доменов"""
        validator = EmailValidator(check_disposable=True)
        
        disposable_emails = [
            "user@tempmail.com",
            "test@mailinator.com",
            "temp@yopmail.com"
        ]
        
        for email in disposable_emails:
            assert validator.validate_domain(email) == False, f"Disposable email {email} должен быть отклонен"
    
    def test_popular_domains(self):
        """Тест популярных доменов"""
        validator = EmailValidator()
        
        popular_emails = [
            "user@gmail.com",
            "test@yahoo.com",
            "email@mail.ru"
        ]
        
        for email in popular_emails:
            parts = validator.get_email_parts(email)
            assert parts['is_popular_domain'] == True, f"Домен {email} должен определяться как популярный"
    
    @patch('email_validator.dns.resolver.resolve')
    def test_mx_records_check(self, mock_dns_resolve):
        """Тест проверки MX записей с mock"""
        # Настраиваем mock для успешной проверки MX
        mock_dns_resolve.return_value = ['mx1.example.com']
        
        validator = EmailValidator(check_mx=True)
        result = validator.validate_domain("user@example.com")
        
        assert result == True
        mock_dns_resolve.assert_called_once_with('example.com', 'MX')
    
    @patch('email_validator.dns.resolver.resolve')
    def test_mx_records_failure(self, mock_dns_resolve):
        """Тест отсутствия MX записей"""
        # Настраиваем mock для ошибки DNS
        mock_dns_resolve.side_effect = Exception("No MX records")
        
        validator = EmailValidator(check_mx=True)
        result = validator.validate_domain("user@example.com")
        
        assert result == False


class TestEmailParts:
    """Тесты разбора email на части"""
    
    def test_get_email_parts_valid(self):
        """Тест разбора валидного email"""
        validator = EmailValidator()
        email = "user.name+tag@gmail.com"
        
        parts = validator.get_email_parts(email)
        
        assert parts is not None
        assert parts['local_part'] == "user.name+tag"
        assert parts['domain'] == "gmail.com"
        assert parts['is_popular_domain'] == True
        assert parts['is_disposable'] == False
    
    def test_get_email_parts_invalid(self):
        """Тест разбора невалидного email"""
        validator = EmailValidator()
        parts = validator.get_email_parts("invalid-email")
        
        assert parts is None


class TestComprehensiveValidation:
    """Тесты комплексной валидации"""
    
    def test_comprehensive_valid_email(self):
        """Тест комплексной проверки валидного email"""
        validator = EmailValidator(check_mx=False)
        result = validator.validate_comprehensive("user@example.com")
        
        assert result['is_valid_format'] == True
        assert result['is_valid_domain'] == True
        assert result['errors'] == []
    
    def test_comprehensive_invalid_format(self):
        """Тест комплексной проверки невалидного формата"""
        validator = EmailValidator()
        result = validator.validate_comprehensive("invalid-email")
        
        assert result['is_valid_format'] == False
        assert result['is_valid_domain'] == False
        assert 'Неверный формат email' in result['errors']
    
    def test_comprehensive_disposable_email(self):
        """Тест комплексной проверки disposable email"""
        validator = EmailValidator(check_disposable=True)
        result = validator.validate_comprehensive("user@tempmail.com")
        
        assert result['is_valid_format'] == True
        assert result['is_valid_domain'] == False
        assert 'Disposable email не разрешены' in result['errors']


class TestUtilityFunctions:
    """Тесты вспомогательных функций"""
    
    def test_is_valid_email_function(self):
        """Тест функции is_valid_email"""
        assert is_valid_email("user@example.com") == True
        assert is_valid_email("invalid-email") == False
    
    def test_validate_email_detailed_function(self):
        """Тест функции validate_email_detailed"""
        result = validate_email_detailed("user@example.com")
        
        assert 'email' in result
        assert 'is_valid_format' in result
        assert 'errors' in result


class TestEdgeCases:
    """Тесты граничных случаев"""
    
    def test_email_with_special_chars(self):
        """Тест email со специальными символами"""
        validator = EmailValidator()
        
        special_emails = [
            "user+tag@example.com",    # Плюс в локальной части
            "user.name@example.com",   # Точка в локальной части
            "user_name@example.com",   # Подчеркивание в локальной части
            "user-name@example.com",   # Дефис в локальной части
        ]
        
        for email in special_emails:
            assert validator.validate_format(email) == True, f"Email {email} должен быть валидным"
    
    def test_case_insensitive(self):
        """Тест нечувствительности к регистру"""
        validator = EmailValidator()
        
        emails = [
            "USER@EXAMPLE.COM",
            "User@Example.Com",
            "user@example.com"
        ]
        
        for email in emails:
            assert validator.validate_format(email) == True


# Параметризованные тесты
@pytest.mark.parametrize("email,expected", [
    ("test@example.com", True),
    ("invalid", False),
    ("user@tempmail.com", False),
    ("", False),
    (None, False),
    ("a@b.c", True),
])
def test_is_valid_email_parameterized(email, expected):
    """Параметризованный тест для функции is_valid_email"""
    if email is None:
        assert is_valid_email(email) == False
    else:
        assert is_valid_email(email) == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
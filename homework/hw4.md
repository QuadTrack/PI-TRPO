# Задание 1: Аналитический анализ кода

### 1 и 2. Нарушения и их классификация

#### 1. Проблемы именования

* **`calc`, `proc**`: Сокращённые и неинформативные имена функций. Имя `calc` не объясняет, что рассчитывается итоговая стоимость со скидкой, а `proc` — что обрабатывается список позиций/заказов.
* **`a`, `b`, `c`, `x**`: Однобуквенные переменные в `calc`. Названия не отражают суть (`price`, `quantity`, `discount_type`, `total_price`).
* **`r`, `data`, `i**`: Переменные в `proc`. `i` выглядит как индекс, хотя является элементом (словарём). `r` — невнятное сокращение от `result` / `processed_prices`.
* **Однобуквенные ключи словаря (`'t'`, `'p'`, `'q'`, `'d'`)**: Магические строки/ключи. Непонятно без контекста (`'type'`, `'price'`, `'quantity'`, `'discount_type'`).

#### 2. Проблемы структуры

* **Использование словарей вместо DTO / dataclass**: Передача неуправляемых словарей со скрытыми ключами (`i['t']`) приводит к рискам `KeyError` во время выполнения.
* **Нарушение Single Responsibility Principle (SRP)**: Функция `calc` совмещает вычисление базoвой стоимости и логику применения скидок.

#### 3. Проблемы логики

* **Магические числа (Magic Numbers)**: Значения `c == 1`, `c == 2`, коэффициенты `0.1`, `0.2` и проверка `x < 0` зашиты в код без пояснений и констант.
* **Необработанный выбор скидки**: Если `c` принимает значение, отличное от `1` или `2` (например, `3` или отрицательное), скидка silently (тихо) не применяется без уведомления/исключения.
* **Мёртвый код (Dead code)**: Проверка `if x < 0: x = 0` бессмысленна, так как произведение положительной цены и количества за вычетом процента скидки не может дать отрицательное число.

#### 4. Отсутствие документации и аннотаций типов

* **Отсутствие type hints**: Не указаны типы аргументов и возвращаемых значений.
* **Отсутствие docstring**: Нет описания назначения функций, структуры входных данных и возможных исключений.
* **Неинформативный комментарий**: Комментарий `# Расчет итоговой цены` внутри тела функции не заменяет правильную документацию.

---

### 3 и 4. Исправленный вариант кода с Docstring

```python
from dataclasses import dataclass
from enum import Enum
from typing import List


class DiscountType(Enum):
    """Типы доступных скидок."""
    NONE = 0
    STANDARD = 1  # Скидка 10%
    PREMIUM = 2   # Скидка 20%


@dataclass(frozen=True)
class OrderItem:
    """Модель элемента заказа."""
    item_type: str
    price: float
    quantity: int
    discount_type: DiscountType = DiscountType.NONE


DISCOUNT_RATES = {
    DiscountType.NONE: 0.0,
    DiscountType.STANDARD: 0.10,
    DiscountType.PREMIUM: 0.20,
}


def calculate_item_total(price: float, quantity: int, discount_type: DiscountType = DiscountType.NONE) -> float:
    """Вычисляет итоговую стоимость позиции с учётом скидки.

    :param price: Цена за единицу товара (должна быть >= 0).
    :param quantity: Количество товара (должно быть >= 0).
    :param discount_type: Тип применимой скидки (DiscountType).
    :return: Итоговая стоимость со скидкой.
    :raises ValueError: Если цена или количество имеют отрицательное значение.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Цена и количество не могут быть отрицательными.")

    discount_rate = DISCOUNT_RATES.get(discount_type, 0.0)
    base_price = price * quantity
    return base_price * (1.0 - discount_rate)


def process_orders(items: List[OrderItem]) -> List[float]:
    """Обрабатывает список товаров и возвращает итоговую стоимость для подходящих позиций.

    Рассчитывает стоимость только для товаров типа 'A'. Для остальных типов возвращает 0.0.

    :param items: Список объектов OrderItem для обработки.
    :return: Список рассчитанных стоимостей для каждой позиции.
    """
    return [
        calculate_item_total(item.price, item.quantity, item.discount_type)
        if item.item_type == 'A' else 0.0
        for item in items
    ]

```

### 5. Оценка цикломатической сложности (Cyclomatic Complexity)

Цикломатическая сложность $M$ рассчитывается по формуле:

$$M = E - N + 2P$$

*(где $E$ — число рёбер, $N$ — число узлов, $P$ — число компонентов связности)* или просто как **$1 + \text{число точек принятия решений (if, elif, for, while, and, or)}$**.

#### Исходный код:

1. **`calc(a, b, c)`**:
* Базовая сложность = 1
* `if c == 1`: +1
* `elif c == 2`: +1
* `if x < 0`: +1
* **Итого M = 4** (средняя сложность).


2. **`proc(data)`**:
* Базовая сложность = 1
* `for i in data`: +1
* `if i['t'] == 'A'`: +1
* **Итого M = 3**.


* Общая суммарная сложность исходного кода: **7**.

#### Исправленный код:

1. **`calculate_item_total(...)`**:
* Базовая сложность = 1
* `if price < 0 or quantity < 0`: +2 (один `if` и логический оператор `or`)
* **Итого M = 3** (сложность ниже, ветвление связано только с валидацией).


2. **`process_orders(...)`**:
* Базовая сложность = 1
* Comprehension loop `for item in items`: +1
* Ternary condition `if item.item_type == 'A'`: +1
* **Итого M = 3**.

**Вывод**: В отрефакторенном коде линейная логика работы со скидками (словарный сопоставитель `DISCOUNT_RATES.get(...)`) полностью устранила ветвления `if/elif` в расчёте цен, сделав код более предсказуемым и простым для тестирования.

# Задание 2: Рефакторинг кода (Интернет-магазин)

### 1 и 2. Рефакторинг с применением SOLID и паттернов

Применённые улучшения:

* **SRP**: Класс `Order` отвечает только за данные заказа, `DiscountCalculator` — за скидки, `DeliveryCalculator` — за доставку, `OrderProcessor` — за процесс обработки.
* **OCP**: Стратегия скидок расширяется добавлением новых элементов/карт без изменения логики процессора.
* **DIP**: Высокоуровневая логика зависит от интерфейсов/абстракций расчёта.

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Protocol


class OrderStatus(Enum):
    NEW = "new"
    PENDING = "pending"
    PROCESSING = "processing"


@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int

    @property
    def total_price(self) -> float:
        return self.price * self.quantity


@dataclass
class User:
    name: str
    is_vip: bool = False


@dataclass
class Order:
    items: List[OrderItem]
    user: User
    promo_code: str | None = None
    total: float = 0.0
    status: OrderStatus = OrderStatus.NEW


class DiscountStrategy:
    """Стратегия расчёта скидок по промокодам."""
    PROMO_DISCOUNTS = {
        "SAVE10": 0.10,
        "SAVE20": 0.20,
        "VIP": 0.30,
    }

    @classmethod
    def apply_discount(cls, total_amount: float, promo_code: str | None) -> float:
        if not promo_code or promo_code not in cls.PROMO_DISCOUNTS:
            return total_amount
        discount_rate = cls.PROMO_DISCOUNTS[promo_code]
        return total_amount * (1.0 - discount_rate)


class DeliveryCalculator:
    """Калькулятор стоимости доставки."""
    FREE_DELIVERY_THRESHOLD = 100.0
    STANDARD_DELIVERY_FEE = 50.0

    @classmethod
    def calculate_delivery(cls, current_total: float) -> float:
        if current_total < cls.FREE_DELIVERY_THRESHOLD:
            return cls.STANDARD_DELIVERY_FEE
        return 0.0


class OrderProcessor:
    """Сервис обработки заказов."""
    
    def process_order(self, order: Order) -> float:
        """Рассчитывает итоговую сумму заказа и обновляет его статус."""
        base_total = sum(item.total_price for item in order.items)
        discounted_total = DiscountStrategy.apply_discount(base_total, order.promo_code)
        delivery_fee = DeliveryCalculator.calculate_delivery(discounted_total)
        
        order.total = discounted_total + delivery_fee
        order.status = OrderStatus.PROCESSING if order.user.is_vip else OrderStatus.PENDING
        
        return order.total


def process_new_orders(orders: List[Order], processor: OrderProcessor) -> List[float]:
    """Обрабатывает только новые заказы из списка."""
    return [
        processor.process_order(order)
        for order in orders
        if order.status == OrderStatus.NEW
    ]

```

---

### 3. Unit-тесты для отрефакторенного кода

```python
import unittest


class TestOrderProcessing(unittest.TestCase):

    def setUp(self):
        self.processor = OrderProcessor()
        self.standard_user = User(name="John", is_vip=False)
        self.vip_user = User(name="Alice", is_vip=True)
        self.item_50 = OrderItem(name="Item 1", price=50.0, quantity=1)
        self.item_120 = OrderItem(name="Item 2", price=120.0, quantity=1)

    def test_order_subtotal_under_threshold_adds_delivery(self):
        # 50 (цена) - 0 (скидка) + 50 (доставка) = 100
        order = Order(items=[self.item_50], user=self.standard_user)
        total = self.processor.process_order(order)
        self.assertEqual(total, 100.0)
        self.assertEqual(order.status, OrderStatus.PENDING)

    def test_order_subtotal_above_threshold_free_delivery(self):
        # 120 (цена) - 0 (скидка) + 0 (доставка) = 120
        order = Order(items=[self.item_120], user=self.standard_user)
        total = self.processor.process_order(order)
        self.assertEqual(total, 120.0)
        self.assertEqual(order.status, OrderStatus.PENDING)

    def test_promo_code_save10_applied(self):
        # 120 * 0.9 = 108 (>100 -> бесплатная доставка)
        order = Order(items=[self.item_120], user=self.standard_user, promo_code="SAVE10")
        total = self.processor.process_order(order)
        self.assertAlmostEqual(total, 108.0)

    def test_vip_user_status_updated_to_processing(self):
        order = Order(items=[self.item_120], user=self.vip_user)
        self.processor.process_order(order)
        self.assertEqual(order.status, OrderStatus.PROCESSING)

    def test_process_only_new_orders_in_list(self):
        order_new = Order(items=[self.item_120], user=self.standard_user, status=OrderStatus.NEW)
        order_pending = Order(items=[self.item_120], user=self.standard_user, status=OrderStatus.PENDING)
        
        results = process_new_orders([order_new, order_pending], self.processor)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 120.0)


if __name__ == '__main__':
    unittest.main()

```

---

### 4. Сравнение метрик кода

| Метрика | Исходный код | Отрефакторенный код | Комментарий |
| --- | --- | --- | --- |
| **Количество строк (LOC)** | ~40 | ~65 | Увеличение LOC обусловлено добавлением строгой типизации, Enum, Dataclass иявным разделением ответственности. |
| **Количество классов** | 1 | 5 (`OrderStatus`, `OrderItem`, `User`, `Order`, `OrderProcessor` + стратегии) | Код разбит на предметные сущности согласно принципу SRP. |
| **Количество методов** | 2 | 4 | Гранулярность выросла, методы стали короче и проще. |
| **Читаемость (субъективно)** | Low (3/10) | High (9/10) | Код self-documented, исключено дублирование, используются типы данных вместо словарей, устранены магические строки/числа. |

---

# Задание 3: Код-ревью (Творческое задание)

### 1 и 2. Разбор функций

#### Функция `f(x)`

* **Что сделано хорошо**: Логика работы верная, фильтрация четных чисел работает корректно.
* **Что улучшить**: Именования (`f`, `x`, `l` не отражают суть); вместо `range(len(x))` стоит итерироваться прямо по элементам; код лаконично переписывается через list comprehension.
* **Нарушенные принципы**: PEP 8 (именование), Pythonic Code practices.

#### Функция `g(y)`

* **Что сделано хорошо**: Алгоритм подсчета частоты элементов верный.
* **Что улучшить**: Использовать `collections.Counter` или метод словаря `d.get(i, 0) + 1`.
* **Нарушенные принципы**: Don't Reinvent the Wheel (Изобретение велосипеда).

#### Функция `h(z)`

* **Что сделано хорошо**: Попытка применить встроенный метод.
* **Что улучшить**: Метод `list.sort()` сортирует список **in-place** (на месте) и возвращает `None`. Функция возвратит `None`, исказив переданный список. Если требуется возвращать новый отсортированный список, нужно использовать `sorted(z)`.
* **Нарушенные принципы**: Корректность работы с мутируемыми объектами (Side Effects / Unexpected return).

---

### 3. Комментарии к Pull Request

```markdown
### PR Review Comments

1. 💬 **File: main.py | Line 1 (`def f(x):`)**
   > Привет! Давай дадим функции и аргументам более выразительные имена. Например, `double_even_numbers(numbers: list[int]) -> list[int]`. Это сильно упростит чтение кода без необходимости вникать в его реализацию.

2. 💬 **File: main.py | Line 3 (`for i in range(len(x)):`)**
   > Использование `range(len(...))` считается непитоничным антипаттерном, когда индекс не нужен напрямую. Лучше итерироваться по элементам напрямую: `for number in numbers:`. 
   > 
   > А ещё лучше записать всю функцию в одну строчку через list comprehension:
   > `return [number * 2 for number in numbers if number % 2 == 0]`

3. 💬 **File: main.py | Line 10 (`def g(y):`)**
   > Отличная задача на подсчёт частоты элементов! В стандартной библиотеке Python для этого уже есть готовый и оптимизированный инструмент — `collections.Counter`. 
   > 
   > Код можно сократить до:
   > ```python
   > from collections import Counter
   > 
   > def count_frequencies(items: list) -> dict:
   >     return dict(Counter(items))
   > ```

4. 💬 **File: main.py | Line 21 (`return z.sort()`)**
   > ⚠️ **Критический баг**: Метод `.sort()` сортирует список на месте (in-place) и возвращает `None`. В текущем виде функция всегда будет возвращать `None`.
   > Если нам нужно вернуть новый отсортированный список, не меняя исходный, используй встроенную функцию `sorted()`: `return sorted(z)`.

5. 💬 **File: main.py | Line 20 (`# TODO: fix this later`)**
   > Постарайся не оставлять TODO перед отправкой кода в PR, если задачу можно решить сразу. Если это блокер — лучше оформить отдельный тикет в Jira/YouTrack и указать ссылку на него в комментарии.

6. 💬 **General Feedback**
   > В целом алгоритмическая логика написана верно, молодец! Обрати внимание на аннотации типов (Type Hints) и добавление docstring к функциям — это хорошая практика для всей нашей команды.

```

---

### 4. Общие советы джуниору по написанию чистого кода

1. **Изучи возможности стандартной библиотеки (Python Standard Library)**.
Прежде чем писать свой цикл или алгоритм (например, подсчет элементов, фильтрацию или группировку), проверь модули `collections`, `itertools`, `functools` и встроенные функции Python. В 90% случаев нужная задача уже эффективно решена за тебя.
2. **Используй понятные имена и Type Hints**.
Код читается значительно чаще, чем пишется. Избегай однобуквенных переменных (кроме счётчиков `i`, `j` в коротких петлях). Называй функции глаголами (`get_user_data`, `calculate_total`), а переменные — существительными (`users_count`, `is_active`). Всегда добавляй аннотации типов.
3. **Следи за побочными эффектами (Side Effects)**.
Чётко разделяй функции, которые возвращают новые данные, и функции, которые модифицируют переданные объекты на месте. Помни о разнице между `list.sort()` (мутирует на месте, возвращает `None`) и `sorted()` (возвращает новый список).

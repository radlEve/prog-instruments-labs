import pytest
from client import Client
from bank import Bank


@pytest.fixture
def empty_bank():
    return Bank()


@pytest.fixture
def client_a():
    return Client("Alice", 1000)


@pytest.fixture
def client_b():
    return Client("Bob", 500)


# Тест 1: Проверка инициализации клиента
def test_client_creation(client_a):
    assert client_a.account['name'] == "Alice"
    assert client_a.account['holdings'] == 1000

    assert isinstance(client_a.account['account_number'], int)
    assert 10000 <= client_a.account['account_number'] <= 99999


# Тест 2: Проверка пополнения счета (Deposit)
def test_deposit(client_a):
    initial_balance = client_a.get_balance()
    client_a.deposit(500)
    assert client_a.get_balance() == initial_balance + 500


# Тест 3: Проверка снятия средств (Withdraw)
def test_withdraw(client_a):
    initial_balance = client_a.get_balance()
    client_a.withdraw(200)
    assert client_a.get_balance() == initial_balance - 200


# Тест 4: Проверка исключения
# пытаемся снять больше, чем есть. (тест пройдет, только если вылетит ошибка ValueError)
def test_withdraw_insufficient_funds(client_a):
    with pytest.raises(ValueError, match="Not enough funds"):
        client_a.withdraw(99999)


# Тест 5: Проверка перевода между клиентами (Interaction)
def test_transfer_success(client_a, client_b):
    # Алиса переводит 200 Бобу
    result = client_a.transfer(client_b, 200)

    assert result is True
    assert client_a.get_balance() == 800  # 1000 - 200
    assert client_b.get_balance() == 700  # 500 + 200


# Тест 6: Проверка атомарности перевода (Interaction + Exception)
# если у Алисы не хватает денег, баланс Боба не должен измениться.
def test_transfer_fail(client_a, client_b):
    initial_b_balance = client_b.get_balance()

    # Алиса пытается перевести 5000 (у нее только 1000)
    with pytest.raises(ValueError, match="Not enough funds"):
        client_a.transfer(client_b, 5000)

    # проверяем, что деньги Боба на месте
    assert client_b.get_balance() == initial_b_balance


# Тест 7: Параметризованный тест
# запускает этот тест 3 раза с разными значениями amount и expected
@pytest.mark.parametrize("amount, expected", [
    (100, 1100),
    (50, 1050),
    (0.01, 1000.01)
])
def test_deposit_parametrized(client_a, amount, expected):
    client_a.deposit(amount)
    assert client_a.get_balance() == expected


# Тест 8: Использование MOCK
# подменяем функцию randint, чтобы предсказуемо тестировать с одним чилом
def test_account_number_mock(mocker):
    mocker.patch('client.randint', return_value=77777)

    c = Client("Lucky Test", 0)
    assert c.account['account_number'] == 77777


# Тест 9: Интеграционный тест банка
def test_bank_authentication(empty_bank, client_a):
    empty_bank.update_db(client_a)

    acc_num = client_a.account['account_number']

    found_client = empty_bank.authentication("Alice", acc_num)
    assert found_client == client_a

    wrong_client = empty_bank.authentication("Alice", 00000)
    assert wrong_client is None

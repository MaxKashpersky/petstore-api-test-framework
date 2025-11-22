import pytest
import requests
from faker import Faker
from api_client import ApiClient


class UserAPITester:
    """Фреймворк для тестирования API пользователей."""

    def __init__(self):
        self.base_url = "https://petstore.swagger.io/v2"
        self.api_client = ApiClient(self.base_url)
        self.fake = Faker()
        self.created_users = []

    def generate_user_data(self, username=None):
        """Генерация тестовых данных пользователя."""
        if username is None:
            username = f"user_{self.fake.random_int(1000, 9999)}"

        return {
            "id": self.fake.random_int(1000, 99999),
            "username": username,
            "firstName": self.fake.first_name(),
            "lastName": self.fake.last_name(),
            "email": self.fake.email(),
            "password": "test123",
            "phone": self.fake.phone_number()[:15],
            "userStatus": 1
        }

    def create_test_user(self):
        """Создать тестового пользователя и вернуть его данные."""
        user_data = self.generate_user_data()
        response = self.api_client.post("/user", data=user_data)

        if response.status_code == 200:
            self.created_users.append(user_data["username"])
            print(f"👤 Создан тестовый пользователь: {user_data['username']}")
            return user_data, True
        print(f"❌ Не удалось создать пользователя: {user_data['username']}")
        return user_data, False

    def cleanup(self):
        """Очистка созданных пользователей."""
        if not self.created_users:
            print("📭 Нет пользователей для очистки")
            return

        print(f"\n🧹 Начинаю очистку {len(self.created_users)} пользователей...")
        cleaned_count = 0

        for username in self.created_users:
            try:
                response = self.api_client.delete(f"/user/{username}")
                if response.status_code == 200:
                    print(f"   ✅ Удален: {username}")
                    cleaned_count += 1
                else:
                    print(f"   ⚠️ Не удалось удалить: {username} (код: {response.status_code})")
            except Exception as e:
                print(f"   ❌ Ошибка удаления {username}: {e}")

        self.created_users = []
        print(f"🧹 Очистка завершена. Удалено: {cleaned_count} пользователей")


# Фикстуры для pytest
@pytest.fixture
def api_tester():
    """Фикстура для создания тестового клиента."""
    tester = UserAPITester()
    yield tester
    # Очистка после каждого теста
    tester.cleanup()


# Тестовые функции
def test_create_user(api_tester):
    """Тест создания пользователя."""
    user_data, success = api_tester.create_test_user()

    assert success is True
    assert user_data["username"] in api_tester.created_users


def test_get_user(api_tester):
    """Тест получения пользователя."""
    user_data, success = api_tester.create_test_user()
    assert success is True

    # Получаем пользователя
    response = api_tester.api_client.get(f"/user/{user_data['username']}")

    assert response.status_code == 200
    user_info = response.json()
    assert user_info["username"] == user_data["username"]
    assert user_info["email"] == user_data["email"]


def test_update_user(api_tester):
    """Тест обновления пользователя."""
    user_data, success = api_tester.create_test_user()
    assert success is True

    # Обновляем данные
    updated_data = user_data.copy()
    updated_data["firstName"] = "UpdatedName"
    updated_data["email"] = "updated@test.com"

    response = api_tester.api_client.put(
        f"/user/{user_data['username']}",
        data=updated_data
    )
    assert response.status_code == 200

    # Проверяем обновление
    get_response = api_tester.api_client.get(f"/user/{user_data['username']}")
    updated_user = get_response.json()
    assert updated_user["firstName"] == "UpdatedName"
    assert updated_user["email"] == "updated@test.com"


def test_delete_user(api_tester):
    """Тест удаления пользователя."""
    user_data, success = api_tester.create_test_user()
    assert success is True

    # Удаляем пользователя
    response = api_tester.api_client.delete(f"/user/{user_data['username']}")
    assert response.status_code == 200

    # Убираем из списка для очистки, так как уже удалили
    if user_data["username"] in api_tester.created_users:
        api_tester.created_users.remove(user_data["username"])

    # Проверяем, что пользователь удален
    response = api_tester.api_client.get(f"/user/{user_data['username']}")
    assert response.status_code == 404


def test_user_login(api_tester):
    """Тест входа пользователя."""
    user_data, success = api_tester.create_test_user()
    assert success is True

    # Логинимся
    response = api_tester.api_client.get(
        "/user/login",
        params={"username": user_data["username"], "password": user_data["password"]}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "logged in" in response_data["message"]


def test_user_logout(api_tester):
    """Тест выхода пользователя."""
    response = api_tester.api_client.get("/user/logout")

    assert response.status_code == 200
    response_data = response.json()
    assert "ok" in response_data["message"]


def test_user_not_found(api_tester):
    """Тест поиска несуществующего пользователя."""
    response = api_tester.api_client.get("/user/nonexistent_user_12345")

    assert response.status_code == 404


def test_create_multiple_users(api_tester):
    """Тест создания нескольких пользователей."""
    success_count = 0
    total_count = 3

    for i in range(total_count):
        user_data = api_tester.generate_user_data(f"multiuser_{i}")
        response = api_tester.api_client.post("/user", data=user_data)

        if response.status_code == 200:
            api_tester.created_users.append(user_data["username"])
            success_count += 1
            print(f"👤 Создан пользователь: {user_data['username']}")

    assert success_count == total_count
import subprocess
import sys
import os
from datetime import datetime


def create_reports_folder():
    """Создать папку для отчетов если ее нет."""
    if not os.path.exists("reports"):
        os.makedirs("reports")
        print("📁 Создана папка 'reports' для хранения отчетов")


def show_menu():
    """Показать главное меню."""
    print("\n" + "=" * 60)
    print("🎯 ФРЕЙМВОРК ДЛЯ ТЕСТИРОВАНИЯ USER API")
    print("=" * 60)
    print("1. 🚀 Запустить ВСЕ тесты с HTML отчетом")
    print("2. 📝 Запустить отдельный тест")
    print("3. 🔍 Запустить тесты с детальным выводом")
    print("4. 🎯 Запустить ВЫБРАННЫЕ тесты с отчетом")
    print("5. 🧹 Очистить отчеты")
    print("6. 🔧 Проверка работоспособности удаления тестовых данных")
    print("7. 🆘 Помощь")
    print("0. ❌ Выход")
    print("=" * 60)


def check_data_cleanup():
    """Проверить работоспособность удаления тестовых данных."""
    print("\n🔧 ПРОВЕРКА РАБОТОСПОСОБНОСТИ УДАЛЕНИЯ ТЕСТОВЫХ ДАННЫХ")
    print("=" * 50)

    # Создаем тестового пользователя для проверки
    from api_client import ApiClient
    from faker import Faker

    api_client = ApiClient("https://petstore.swagger.io/v2")
    fake = Faker()

    test_username = f"test_cleanup_{fake.random_int(1000, 9999)}"
    user_data = {
        "id": fake.random_int(1000, 99999),
        "username": test_username,
        "firstName": "Test",
        "lastName": "Cleanup",
        "email": f"{test_username}@test.com",
        "password": "test123",
        "phone": "123-456-7890",
        "userStatus": 1
    }

    print(f"👤 Создаю тестового пользователя: {test_username}")

    # Создаем пользователя
    response = api_client.post("/user", data=user_data)
    if response.status_code == 200:
        print("✅ Пользователь создан успешно")

        # Проверяем что пользователь существует
        response = api_client.get(f"/user/{test_username}")
        if response.status_code == 200:
            print("✅ Пользователь найден в системе")

            # Удаляем пользователя
            response = api_client.delete(f"/user/{test_username}")
            if response.status_code == 200:
                print("✅ Пользователь удален")

                # Проверяем что пользователь удален
                response = api_client.get(f"/user/{test_username}")
                if response.status_code == 404:
                    print("✅ Подтверждено: пользователь удален из системы")
                    print("🎉 Система удаления тестовых данных работает корректно!")
                else:
                    print("❌ Ошибка: пользователь все еще существует в системе")
            else:
                print(f"❌ Ошибка удаления: код {response.status_code}")
        else:
            print("❌ Ошибка: пользователь не найден после создания")
    else:
        print(f"❌ Ошибка создания пользователя: код {response.status_code}")

    print("=" * 50)


def show_test_menu():
    """Показать меню выбора тестов."""
    print("\n📋 ВЫБЕРИТЕ ТЕСТ ДЛЯ ЗАПУСКА:")
    print("1. 📝 Создание пользователя")
    print("2. 👤 Получение пользователя")
    print("3. ✏️ Обновление пользователя")
    print("4. 🗑️ Удаление пользователя")
    print("5. 🔐 Вход пользователя")
    print("6. 🚪 Выход пользователя")
    print("7. 🔍 Поиск несуществующего пользователя")
    print("8. 👥 Создание нескольких пользователей")
    print("9. ↩️ Назад в главное меню")


def show_multiple_tests_menu():
    """Показать меню выбора нескольких тестов."""
    print("\n🎯 ВЫБЕРИТЕ ТЕСТЫ ДЛЯ ЗАПУСКА (через запятую):")
    print("1. 📝 Создание пользователя")
    print("2. 👤 Получение пользователя")
    print("3. ✏️ Обновление пользователя")
    print("4. 🗑️ Удаление пользователя")
    print("5. 🔐 Вход пользователя")
    print("6. 🚪 Выход пользователя")
    print("7. 🔍 Поиск несуществующего пользователя")
    print("8. 👥 Создание нескольких пользователей")
    print("9. ✅ Завершить выбор и запустить")
    print("0. ↩️ Назад в главное меню")


def run_pytest_command(command):
    """Запустить команду pytest и показать результат."""
    print(f"\n🔧 Выполняю команду: {command}")
    print("=" * 50)

    try:
        # Запускаем команду и сразу видим вывод в консоль
        result = subprocess.run(command, shell=True)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Ошибка при выполнении команды: {e}")
        return False


def run_all_tests_with_html():
    """Запуск всех тестов с HTML отчетом."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = f"reports/report_all_{timestamp}.html"

    command = (
        f'pytest test_user_api.py -v '
        f'--html={html_report} --self-contained-html'
    )

    success = run_pytest_command(command)

    if success:
        print(f"\n✅ Тесты завершены успешно!")
        print(f"📊 HTML отчет сохранен: {html_report}")
        _open_report_in_browser(html_report)
    else:
        print(f"\n❌ Тесты завершены с ошибками")
        print(f"📄 Отчет все равно сохранен: {html_report}")


def run_single_test(test_choice):
    """Запуск одного теста."""
    test_mapping = {
        "1": "test_create_user",
        "2": "test_get_user",
        "3": "test_update_user",
        "4": "test_delete_user",
        "5": "test_user_login",
        "6": "test_user_logout",
        "7": "test_user_not_found",
        "8": "test_create_multiple_users"
    }

    if test_choice in test_mapping:
        test_name = test_mapping[test_choice]
        command = f'pytest test_user_api.py::{test_name} -v'
        run_pytest_command(command)
    else:
        print("❌ Неверный выбор теста!")


def run_multiple_tests_with_report():
    """Запуск выбранных тестов с HTML отчетом."""
    test_mapping = {
        "1": "test_create_user",
        "2": "test_get_user",
        "3": "test_update_user",
        "4": "test_delete_user",
        "5": "test_user_login",
        "6": "test_user_logout",
        "7": "test_user_not_found",
        "8": "test_create_multiple_users"
    }

    test_names = {
        "1": "Создание пользователя",
        "2": "Получение пользователя",
        "3": "Обновление пользователя",
        "4": "Удаление пользователя",
        "5": "Вход пользователя",
        "6": "Выход пользователя",
        "7": "Поиск несуществующего пользователя",
        "8": "Создание нескольких пользователей"
    }

    selected_tests = []

    while True:
        show_multiple_tests_menu()
        print(f"\n📋 Выбрано тестов: {len(selected_tests)}")
        if selected_tests:
            print("✅ Выбранные тесты:")
            for test_num in selected_tests:
                print(f"   - {test_names[test_num]}")

        choice = input("\n🎲 Выберите тест (1-8), 9-запуск, 0-назад: ").strip()

        if choice == "0":
            return
        elif choice == "9":
            if not selected_tests:
                print("❌ Не выбрано ни одного теста!")
                continue
            break
        elif choice in test_mapping:
            if choice in selected_tests:
                selected_tests.remove(choice)
                print(f"❌ Тест '{test_names[choice]}' удален из выбора")
            else:
                selected_tests.append(choice)
                print(f"✅ Тест '{test_names[choice]}' добавлен в выбор")
        else:
            print("❌ Неверный выбор! Попробуйте снова.")

    # Формируем команду для запуска выбранных тестов
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = f"reports/report_selected_{timestamp}.html"

    test_commands = []
    for test_num in selected_tests:
        test_commands.append(test_mapping[test_num])

    tests_string = " ".join([
        f"test_user_api.py::{test}" for test in test_commands
    ])
    command = (
        f'pytest {tests_string} -v '
        f'--html={html_report} --self-contained-html'
    )

    print(f"\n🎯 ЗАПУСК ВЫБРАННЫХ ТЕСТОВ:")
    for test_num in selected_tests:
        print(f"   ✅ {test_names[test_num]}")

    success = run_pytest_command(command)

    if success:
        print(f"\n✅ Выбранные тесты завершены успешно!")
        print(f"📊 HTML отчет сохранен: {html_report}")
        _open_report_in_browser(html_report)
    else:
        print(f"\n❌ Тесты завершены с ошибками")
        print(f"📄 Отчет все равно сохранен: {html_report}")


def _open_report_in_browser(report_path):
    """Открыть отчет в браузере."""
    try:
        # Проверяем существует ли файл
        if not os.path.exists(report_path):
            print(f"❌ Файл отчета не найден: {report_path}")
            return

        # Получаем абсолютный путь для надежности
        absolute_path = os.path.abspath(report_path)

        print(f"📁 Абсолютный путь к отчету: {absolute_path}")

        if sys.platform == "win32":
            # Пробуем разные способы для Windows
            try:
                os.startfile(absolute_path)
                print("🌐 Отчет открыт в браузере через os.startfile")
            except Exception as e:
                print(f"⚠️ Не удалось открыть через os.startfile: {e}")
                # Пробуем через subprocess
                try:
                    subprocess.run(['start', absolute_path], shell=True, check=True)
                    print("🌐 Отчет открыт в браузере через subprocess")
                except Exception as e2:
                    print(f"⚠️ Не удалось открыть через subprocess: {e2}")
                    print(f"💡 Отчет сохранен: {absolute_path}")
                    print("   Откройте его вручную в браузере")

        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", absolute_path])
            print("🌐 Отчет открыт в браузере")
        else:  # linux
            subprocess.run(["xdg-open", absolute_path])
            print("🌐 Отчет открыт в браузере")

    except Exception as e:
        print(f"❌ Ошибка при открытии отчета: {e}")
        print(f"💡 Отчет сохранен: {os.path.abspath(report_path)}")
        print("   Откройте его вручную в браузере")


def run_verbose_tests():
    """Запуск тестов с детальным выводом."""
    command = 'pytest test_user_api.py -v -s'
    run_pytest_command(command)


def cleanup_reports():
    """Очистка старых отчетов."""
    import glob

    # Проверяем существует ли папка reports
    if not os.path.exists("reports"):
        print("📭 Папка 'reports' не существует - нет отчетов для очистки")
        return

    # Ищем все HTML файлы в папке reports
    reports = glob.glob("reports/*.html")

    # Убираем дубликаты и проверяем существование файлов
    unique_reports = list(set([r for r in reports if os.path.exists(r)]))

    if unique_reports:
        print("\n🗑️ Найдены следующие отчеты:")
        for report in unique_reports:
            filename = os.path.basename(report)
            file_size = os.path.getsize(report)
            print(f"  - {filename} ({file_size} bytes)")

        confirm = input("\n❓ Удалить все отчеты? (y/n): ").lower()
        if confirm == 'y':
            for report in unique_reports:
                try:
                    os.remove(report)
                    print(f"✅ Удален: {os.path.basename(report)}")
                except Exception as e:
                    print(f"❌ Ошибка удаления {os.path.basename(report)}: {e}")

            print(f"\n✅ Удалено отчетов: {len(unique_reports)}")
    else:
        print("📭 Отчеты не найдены в папке 'reports'")


def show_help():
    """Показать справку."""
    print("""
    🆘 ПОМОЩЬ:

    Этот фреймворк использует pytest для тестирования User API PetStore.

    📁 СТРУКТУРА ПРОЕКТА:
    - api_client.py      - клиент для работы с API (класс ApiClient)
    - test_user_api.py   - тесты для pytest
    - main.py            - эта программа с меню
    - requirements.txt   - зависимости
    - reports/           - папка с отчетами 📁

    🎯 ВОЗМОЖНОСТИ:
    1. Запуск всех тестов с отчетом
    2. Запуск одного теста
    3. Детальный вывод тестов
    4. Запуск ВЫБРАННЫХ тестов с отчетом ✅
    5. Очистка отчетов
    6. Проверка работоспособности удаления тестовых данных
    7. Справка

    📊 ОТЧЕТЫ:
    HTML отчеты генерируются через pytest-html плагин
    и сохраняются в папку reports/

    📦 УСТАНОВКА:
    pip install -r requirements.txt
    """)


def check_environment():
    """Проверить наличие необходимых файлов и создать папку reports."""
    required_files = ["test_user_api.py", "api_client.py"]
    missing_files = []

    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("❌ Отсутствуют необходимые файлы:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 Убедитесь, что все файлы находятся в одной папке")
        return False

    # Проверим, что тесты есть в файле
    try:
        with open("test_user_api.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "def test_" not in content:
                print("❌ В файле test_user_api.py не найдены тестовые функции")
                return False
    except Exception as e:
        print(f"❌ Ошибка чтения test_user_api.py: {e}")
        return False

    # Создаем папку reports если ее нет
    if not os.path.exists("reports"):
        os.makedirs("reports")
        print("📁 Создана папка 'reports' для хранения отчетов")
    else:
        print("📁 Папка 'reports' уже существует")

    return True


def main():
    """Главная функция программы."""

    # Проверка окружения
    if not check_environment():
        print("\n⚠️  Пожалуйста, исправьте ошибки и перезапустите программу")
        input("↵ Нажмите Enter для выхода...")
        return

    print("✅ Все файлы на месте, можно начинать тестирование!")

    while True:
        show_menu()
        choice = input("\n🎲 Выберите действие (0-6): ").strip()

        if choice == "1":
            run_all_tests_with_html()
            input("\n↵ Нажмите Enter для продолжения...")

        elif choice == "2":
            while True:
                show_test_menu()
                test_choice = input("\n🎲 Выберите тест (1-9): ").strip()

                if test_choice == "9":
                    break
                elif test_choice in [str(i) for i in range(1, 9)]:
                    run_single_test(test_choice)
                    input("\n↵ Нажмите Enter для продолжения...")
                else:
                    print("❌ Неверный выбор! Попробуйте снова.")

        elif choice == "3":
            run_verbose_tests()
            input("\n↵ Нажмите Enter для продолжения...")

        elif choice == "4":
            run_multiple_tests_with_report()
            input("\n↵ Нажмите Enter для продолжения...")

        elif choice == "5":
            cleanup_reports()
            input("\n↵ Нажмите Enter для продолжения...")

        elif choice == "6":
            check_data_cleanup()
            input("\n↵ Нажмите Enter для продолжения...")

        elif choice == "7":
            show_help()
            input("\n↵ Нажмите Enter для продолжения...")

        elif choice == "0":
            print("\n👋 До свидания!")
            break

        else:
            print("❌ Неверный выбор! Попробуйте снова.")
            input("\n↵ Нажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
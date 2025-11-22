# PetStore API Test Framework

A comprehensive Python framework for automated testing of PetStore REST API endpoints. Built with pytest and featuring fake data generation, detailed reporting, and interactive test management.

## ✨ Features

- 🧪 **8 Ready-to-use Tests** - Full coverage of user endpoints
- 🎲 **Smart Data Generation** - Fake test data with Faker library
- 📊 **Detailed HTML Reports** - Comprehensive test execution insights
- 🖥️ **Interactive CLI Menu** - Easy test management without commands
- 🧹 **Auto Cleanup** - Automatic test data cleanup after execution
- 🔧 **Modular Architecture** - Easy to extend and maintain

## 🛠️ Tech Stack

- **Python 3.10+**
- **pytest** - Test framework
- **requests** - HTTP client
- **Faker** - Test data generation
- **pytest-html** - HTML reporting

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/petstore-api-test-framework.git
cd petstore-api-test-framework
```
Install dependencies:

```bash
pip install -r requirements.txt
```
Run the framework:

```bash
python main.py
```
📁 Project Structure
```text
petstore-api-test-framework/
├── api_client.py          # HTTP client for API interactions
├── test_user_api.py       # Test scenarios and business logic
├── main.py               # Interactive CLI menu
├── requirements.txt      # Project dependencies
├── .gitignore           # Git ignore rules
└── reports/             # Generated HTML reports (auto-created)
```
🧪 Test Coverage
Test	Endpoint	Method	Description
test_create_user	/user	POST	Create user with fake data
test_get_user	/user/{username}	GET	Retrieve user information
test_update_user	/user/{username}	PUT	Update user data
test_delete_user	/user/{username}	DELETE	Remove user
test_user_login	/user/login	GET	User authentication
test_user_logout	/user/logout	GET	User logout
test_user_not_found	/user/{username}	GET	Handle non-existent users
test_create_multiple_users	/user	POST	Create multiple users
🎯 Usage
Interactive Menu
Run python main.py to access the interactive menu:

```text
🎯 API TESTING FRAMEWORK MENU
============================================================
1. 🚀 Run ALL tests with HTML report
2. 📝 Run single test
3. 🔍 Run tests with verbose output
4. 🎯 Run SELECTED tests with report
5. 🧹 Cleanup reports
6. 🔧 Test data cleanup verification
7. 🆘 Help
0. ❌ Exit
```

Direct pytest Usage
```bash
# Run all tests
pytest test_user_api.py -v
```
# Run with HTML report
```
pytest test_user_api.py --html=reports/report.html --self-contained-html
```
# Run specific test
```
pytest test_user_api.py::test_create_user -v
```

📊 Reporting
The framework generates detailed HTML reports including:

Test execution status (Passed/Failed)

Execution time for each test

Environment information

Error traces and stack traces

Reports are automatically saved in the reports/ directory with timestamps.

🔧 API Client
The ApiClient class provides a simple interface for HTTP operations:

```python
from api_client import ApiClient

client = ApiClient("https://petstore.swagger.io/v2")
response = client.post("/user", data=user_data)
response = client.get(f"/user/{username}")
```
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
PetStore Swagger for the test API

pytest team for the excellent testing framework

Faker library for test data generation
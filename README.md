# American Eagle Python Automation

## 🧪 UI & API Test Automation Project

Автоматизированное тестирование реального e-commerce сайта [American Eagle](https://www.ae.com/us/en) с использованием **Python 3.12**, **Pytest**, **Selenium WebDriver**, **Requests**, **GitHub Actions** и **Allure Report**.

[![Python](https://img.shields.io/badge/Python-3.12-%233776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.1.1-%230A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.50.0-%2343B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Requests](https://img.shields.io/badge/Requests-2.34.2-%232C5BB4)](https://requests.readthedocs.io/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI-%232671E5?logo=githubactions)](https://github.com/features/actions)
[![Allure](https://img.shields.io/badge/Allure-Report-%23FF6A00?logo=allure)](https://allurereport.org/)

### 📊 Allure Report

После успешного CI-запуска актуальный отчёт публикуется через GitHub Pages по постоянной ссылке:

➡️ **[Open Allure Report](https://ismeneger.github.io/American_Eagle_python_automation/)**

### ✅ Текущее состояние набора тестов

- **50 тестовых сценариев** в текущем наборе;
- **16 API тестов** — 16 passed;
- **33 UI теста** — 28 passed, 4 skipped, 1 xfailed;
- **1 smoke test** конфигурации проекта — passed;
- последний полный локальный прогон: **45 passed, 4 skipped, 1 xfailed, 0 failed**;
- текущий CI-прогон также включает все **50 test cases** в едином Allure Report;
- `skip` используется для сценариев, которые блокируются anti-bot-защитой сайта;
- `xfail` используется для известного дефекта поиска;
- API + project smoke и UI запускаются в отдельных jobs GitHub Actions;
- результаты объединяются в единый Allure Report.

---

<a id="contents"></a>
## 📚 Содержание

- [📌 О проекте](#project)
- [🎯 Почему я сделал Python-версию](#motivation)
- [🛍 Об объекте тестирования](#system-under-test)
- [🧰 Технологический стек](#tech-stack)
- [🏗 Архитектура проекта](#architecture)
- [✅ Покрытие](#coverage)
- [⚠️ Ограничения и anti-bot protection](#limitations)
- [📝 Тест-план](#test-plan)
- [🏷 Pytest markers](#markers)
- [🚀 Локальный запуск](#local-run)
- [🔐 Credentials](#credentials)
- [⚙️ GitHub Actions](#github-actions)
- [📊 Allure Report](#allure)
- [📦 Allure artifacts](#artifacts)
- [🧪 API lifecycle сценарий](#api-e2e)
- [📁 Структура проекта](#project-structure)
- [📈 CI/CD результат](#cicd-result)
- [👤 Автор](#author)

---

<a id="project"></a>
## 📌 О проекте

Этот репозиторий содержит **автоматизированные UI и REST API тесты** для сайта [American Eagle](https://www.ae.com/).

Проект создан мной **самостоятельно, по собственной инициативе**, уже вне рамок учебной программы и выпускной работы.

Ранее я прошёл курс **«Тестировщик ПО» в Университете ИТМО**, где изучал ручное и автоматизированное тестирование на **Python**. Позже в рамках отдельного курса по Java AQA я разработал Java-версию автоматизации American Eagle как выпускной проект.

После завершения обучения я решил самостоятельно реализовать аналогичный полноценный проект на **Python**, чтобы:

- закрепить и расширить практические навыки Python;
- показать, что могу строить AQA-проект не только на Java;
- самостоятельно перенести и переосмыслить архитектуру тестового фреймворка;
- расширить портфолио вторым языком программирования;
- отработать реальные задачи Automation QA на production-сайте;
- самостоятельно настроить API/UI automation, CI и Allure-отчётность.

Python-версия не является учебным заданием или обязательной частью курса. Это отдельный pet project, который я развиваю самостоятельно как продолжение профессионального развития в Automation QA.

Основные цели проекта:

- автоматизация пользовательских UI-сценариев;
- автоматизация REST API тестирования;
- позитивные и негативные проверки;
- работа с динамическими тестовыми данными;
- разделение UI и API уровней;
- использование Page Object Model и reusable Steps;
- работа с нестабильным динамическим DOM;
- автоматический запуск тестов в GitHub Actions;
- раздельный запуск API и UI наборов;
- формирование единого Allure Report;
- публикация отчётности через GitHub Pages.

[⬆️ К содержанию](#contents)

---

<a id="motivation"></a>
## 🎯 Почему я сделал Python-версию

У меня уже был рабочий Java AQA проект для American Eagle, поэтому я сознательно выбрал тот же реальный объект тестирования для Python-версии.

Это позволило сосредоточиться не на придумывании нового учебного кейса, а на сравнении подходов и самостоятельной реализации тех же Automation QA задач на другом стеке.

В Python-проекте я самостоятельно:

- настроил структуру проекта с нуля;
- организовал виртуальное окружение и зависимости;
- реализовал API-клиенты на `requests`;
- реализовал UI-автоматизацию на Selenium WebDriver;
- построил Page Object и Steps слои;
- добавил pytest fixtures;
- реализовал positive / negative / smoke / defect сценарии;
- добавил Allure annotations и результаты;
- настроил headless Chrome для CI;
- настроил GitHub Actions;
- разделил API и UI jobs;
- добавил GitHub Secrets для API credential;
- реализовал публикацию объединённого Allure Report;
- стабилизировал тесты для работы с динамическим DOM, marketing/regional popup-окнами, `StaleElementReferenceException` и `ElementClickInterceptedException`.

Для меня этот проект — демонстрация того, что знания Python из курса ИТМО я могу применять самостоятельно в полноценном AQA-проекте, а не только в рамках учебных упражнений.

[⬆️ К содержанию](#contents)

---

<a id="system-under-test"></a>
## 🛍 Об объекте тестирования

**American Eagle Outfitters, Inc. (American Eagle)** — крупная американская розничная компания по продаже одежды и аксессуаров.

Для автоматизации используется реальный действующий интернет-магазин:

➡️ [https://www.ae.com/](https://www.ae.com/)

С точки зрения автоматизации тестирования это интересный e-commerce продукт, который включает:

- большой каталог товаров и категорий;
- поиск товаров;
- карточки товаров с разными SKU;
- регистрацию и авторизацию;
- пользовательские сессии;
- корзину и изменение её состояния;
- REST API;
- динамический контент;
- всплывающие маркетинговые окна;
- sale / regular prices;
- динамическое обновление DOM;
- anti-bot protection;
- различия поведения сайта при локальном и CI-запуске.

Работа с production-сайтом позволяет решать реальные Automation QA задачи: синхронизацию, динамические данные, нестабильность внешнего окружения, повторное получение элементов после изменения DOM, работу с токенами, состоянием корзины и CI/CD.

[⬆️ К содержанию](#contents)

---

<a id="tech-stack"></a>
## 🧰 Технологический стек

| Технология | Назначение |
|---|---|
| **Python 3.12** | Основной язык проекта |
| **Pytest 9.1.1** | Тестовый фреймворк |
| **Selenium WebDriver 4.50.0** | UI-автоматизация |
| **Requests 2.34.2** | REST API тестирование |
| **Allure Pytest 2.16.2** | Интеграция Pytest с Allure |
| **Decimal** | Точная работа с ценами |
| **Git / GitHub** | Контроль версий |
| **GitHub Actions** | CI |
| **GitHub Pages** | Публикация Allure Report |
| **Chrome / Selenium Manager** | Запуск UI-тестов |
| **PyCharm** | Среда разработки |

[⬆️ К содержанию](#contents)

---

<a id="architecture"></a>
## 🏗 Архитектура проекта

В проекте используются:

- **Page Object Model** для UI-тестов;
- отдельные `Page` и `Component` классы;
- отдельный `Steps` слой для пользовательских бизнес-сценариев;
- API clients;
- pytest fixtures;
- общие constants / config;
- helper / utils слой;
- Allure annotations;
- pytest markers для группировки;
- отдельные UI и API test packages.

### Разделение ответственности

**Page Objects**

Содержат локаторы и прямые действия со страницей.

**Steps**

Содержат переиспользуемые последовательности пользовательских действий.

**Tests**

Содержат тестовые сценарии, assertions и бизнес-проверки.

Пример:

```text
Test
  ↓
Steps
  ↓
Page Object
  ↓
Selenium WebDriver
```

Такое разделение уменьшает дублирование и делает тесты читаемее.

Основные категории тестов:

- `ui`
- `api`
- `smoke`
- `positive`
- `negative`
- `defect`
- `auth`
- `browse`
- `inventory`
- `bag`
- `account`
- `home_page`

[⬆️ К содержанию](#contents)

---

<a id="coverage"></a>
## ✅ Покрытие

### UI

В UI-части проекта проверяются:

- открытие главной страницы;
- header;
- footer;
- account panel;
- shopping bag;
- favorites;
- поиск существующего товара;
- negative search scenario;
- регистрационная форма;
- валидация email;
- обязательные поля регистрации;
- sign-in validation;
- Men's Clothes каталог;
- переход в каталог;
- сортировка `Price: Low to High`;
- фильтрация по диапазону `$25 - $50`;
- открытие товара;
- выбор доступного размера;
- добавление товара в корзину;
- проверка сообщения `Added to bag!`;
- соответствие цены Product Page и Shopping Bag;
- поддержка sale и regular price;
- соответствие выбранного размера;
- изменение количества товара;
- проверка subtotal;
- free shipping threshold;
- максимальное количество товара;
- удаление товара;
- добавление двух разных товаров в корзину;
- проверка нескольких товаров, их размера и цены.

### API

API-набор включает:

- получение guest token;
- проверку `access_token`;
- негативные проверки guest authorization;
- Browse API;
- получение товаров категории;
- получение динамического `productId`;
- несуществующую категорию;
- Browse без авторизации;
- Inventory API;
- получение доступного товара и SKU;
- invalid product;
- Inventory без авторизации;
- Bag API;
- полный lifecycle товара в корзине;
- добавление нескольких разных товаров;
- добавление без авторизации;
- invalid SKU;
- удаление несуществующего item;
- update с нулевым quantity.

Тесты по возможности используют динамические данные, чтобы уменьшить зависимость от одного захардкоженного товара или SKU.

[⬆️ К содержанию](#contents)

---

<a id="limitations"></a>
## ⚠️ Ограничения реального сайта и anti-bot protection

Тесты выполняются на **реальном production-сайте American Eagle**, который использует anti-bot protection.

Из-за этого отдельные сценарии технически невозможно стабильно выполнять автоматически.

### Регистрация

Заполнение формы регистрации автоматизировано, однако финальная отправка может приводить к `Access Denied`.

Поэтому тест успешного создания аккаунта намеренно помечен:

```python
@pytest.mark.skip(
    reason=(
        "Automated account creation is blocked by the site's anti-bot "
        "protection. Registration form filling works, but submission "
        "results in Access Denied."
    )
)
```

### Авторизация

Успешный sign-in вручную работает, но автоматизированный вход блокируется anti-bot protection.

В активном автоматическом наборе оставлены:

- негативные проверки `invalid email` и `empty email`;
- `successful sign-in` как документированный `skip`;
- один representative password-сценарий (`invalid password`) как документированный `skip`.

Дополнительно предусмотрены сценарии:

- `empty password`;
- `short password`;
- `long password`.

Они не дублируются отдельными `skip`-тестами в активном наборе, потому что из-за anti-bot невозможно стабильно перейти к серверной password validation. Эти проверки остаются частью тестового покрытия и зафиксированы в Test Plan.

Такой подход позволяет не раздувать Allure Report несколькими одинаково недоступными сценариями и при этом явно документировать предусмотренную QA-логику.

### Известный defect поиска

American Eagle возвращает товары / рекомендации даже для бессмысленного несуществующего запроса.

Сценарий сохранён в проекте как известный дефект и отмечен:

```python
@pytest.mark.xfail(
    reason=(
        "Known defect: search returns products "
        "for non-existing queries"
    )
)
```

### Нестабильность production-сайта

Поскольку сайт внешний и production, иногда возможны:

- медленная загрузка;
- временная недоступность страницы;
- повторное появление marketing popup;
- региональный popup выбора страны доставки;
- перекрытие интерактивных элементов popup overlays;
- перерисовка DOM;
- `StaleElementReferenceException`;
- `ElementClickInterceptedException`;
- изменение доступных товаров и скидок.

Для таких случаев в проекте используются explicit waits, централизованное закрытие blocking overlays, повторное получение элементов после изменения DOM, fallback-навигация и ограниченная retry-логика там, где это оправдано.

[⬆️ К содержанию](#contents)

---

<a id="test-plan"></a>
## 📝 Тест-план

Для проекта подготовлен отдельный **Automation Test Plan**, адаптированный под Python-версию проекта.

В документе описаны:

- цели автоматизации;
- UI и REST API scope;
- out of scope;
- типы и категории тестов;
- тестовые данные и управление состоянием;
- технологический стек;
- архитектура автоматизации;
- локальное и CI-окружение;
- CI/CD стратегия;
- Allure Reporting;
- anti-bot ограничения;
- password validation scenarios, которые предусмотрены, но не дублируются в активном наборе из-за anti-bot;
- известный `xfail` сценарий поиска;
- риски и меры снижения;
- критерии успешного завершения.

📄 **[Открыть American Eagle Python Test Plan (PDF)](docs/American_Eagle_Python_TestPlan_2026.pdf)**

[⬆️ К содержанию](#contents)

---

<a id="markers"></a>
## 🏷 Pytest markers

В `pytest.ini` зарегистрированы markers для гибкого запуска наборов тестов.

Основные:

```text
ui
api
account
home_page
auth
browse
inventory
bag
smoke
positive
negative
defect
```

Пример запуска:

```powershell
pytest -m api -v
```

или:

```powershell
pytest -m "ui and positive" -v
```

[⬆️ К содержанию](#contents)

---

<a id="local-run"></a>
## 🚀 Локальный запуск

### Клонирование проекта

```powershell
git clone https://github.com/ISmeneger/American_Eagle_python_automation.git
cd American_Eagle_python_automation
```

### Создание виртуального окружения

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Установка зависимостей

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Все тесты

```powershell
pytest -v
```

### API

Перед запуском API-тестов необходимо передать guest credential:

```powershell
$env:AE_GUEST_AUTH="Basic <guest-api-credential>"
pytest tests\api -v
```

> Реальное значение `AE_GUEST_AUTH` не должно храниться в репозитории.

### UI

```powershell
pytest tests\ui -v
```

### Men's Clothes

```powershell
pytest tests\ui\mens_clothes -v
```

### Конкретный тест

```powershell
pytest tests\ui\mens_clothes\test_product_cart.py::test_product_price_matches_cart_price -v
```

### По marker

```powershell
pytest -m smoke -v
pytest -m positive -v
pytest -m negative -v
pytest -m defect -v
```

[⬆️ К содержанию](#contents)

---

<a id="credentials"></a>
## 🔐 Credentials

Секретные значения не хранятся в репозитории.

Для API используется:

- `AE_GUEST_AUTH` — credential для получения guest access token.

Локально значение передаётся через environment variable:

```powershell
$env:AE_GUEST_AUTH="Basic <guest-api-credential>"
```

В GitHub Actions используется **GitHub Repository Secret**:

```text
AE_GUEST_AUTH
```

Workflow получает значение так:

```yaml
env:
  AE_GUEST_AUTH: ${{ secrets.AE_GUEST_AUTH }}
```

Это позволяет запускать API-тесты в CI без публикации credential в Git-истории.

[⬆️ К содержанию](#contents)

---

<a id="github-actions"></a>
## ⚙️ GitHub Actions

Workflow находится в:

```text
.github/workflows/tests.yml
```

Он разделён на независимые jobs:

```text
api-tests (API + smoke) ──► api-allure-results ──┐
                                                 ├──► allure-report ──► GitHub Pages
ui-tests ───────────────► ui-allure-results ─────┘
```

### `api-tests`

- checkout репозитория;
- установка Python 3.12;
- установка зависимостей;
- получение `AE_GUEST_AUTH` из GitHub Secrets;
- запуск:

```bash
pytest tests/api tests/test_smoke.py -v --alluredir=allure-results
```

- запуск **16 API тестов + 1 project smoke test**;
- сохранение `allure-results` как artifact `api-allure-results`.

### `ui-tests`

- checkout репозитория;
- установка Python 3.12;
- установка зависимостей;
- запуск UI-тестов:

```bash
pytest tests/ui -v --alluredir=allure-results
```

- Chrome автоматически запускается в headless-режиме при `CI=true`;
- сохраняется artifact `ui-allure-results`.

### `allure-report`

После завершения API + smoke и UI jobs:

1. скачиваются Allure results из job `api-tests` (API + smoke);
2. скачиваются UI Allure results;
3. результаты всех **50 test cases** объединяются;
4. восстанавливается история предыдущих Allure запусков;
5. формируется единый Allure Report;
6. отчёт публикуется в ветку `gh-pages`;
7. GitHub Pages предоставляет постоянную ссылку на отчёт.

### ▶️ Запуск workflow

Workflow запускается:

- при `push` в `main`;
- при `pull_request` в `main`;
- вручную через `workflow_dispatch`.

Ожидаемая схема выполнения:

```text
api-tests (API + smoke) ✅
ui-tests                 ✅
          ↓
allure-report             ✅
```

[⬆️ К содержанию](#contents)

---

<a id="allure"></a>
## 📊 Allure Report

Job `api-tests` сохраняет результаты API + project smoke, а `ui-tests` — результаты UI. После этого CI объединяет их в единый Allure Report на **50 test cases**.

После включения GitHub Pages актуальный отчёт доступен по ссылке:

➡️ **[Open Allure Report](https://ismeneger.github.io/American_Eagle_python_automation/)**

В отчёте можно посмотреть:

- общий результат запуска;
- API, UI и project smoke suites;
- отдельные test cases;
- feature / story / title;
- шаги выполнения;
- ошибки и stack traces;
- screenshots и URL для упавших UI-тестов;
- browser / environment information;
- историю запусков.

Локально отчёт можно открыть командой:

```powershell
allure serve allure-results
```

или сформировать статический вариант:

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```

[⬆️ К содержанию](#contents)

---

<a id="artifacts"></a>
## 📦 Allure artifacts

Каждый запуск GitHub Actions отдельно сохраняет:

- `api-allure-results` — результаты **16 API + 1 smoke**;
- `ui-allure-results` — результаты **33 UI**.

Затем оба artifacts объединяются на отдельном CI-этапе в общий Allure Report на **50 test cases**.

[⬆️ К содержанию](#contents)

---

<a id="api-e2e"></a>
## 🧪 Пример API lifecycle сценария

Один из основных API-сценариев проверяет полный lifecycle товара в корзине:

```text
получение guest token
        ↓
получение динамического productId
        ↓
получение доступного SKU через Inventory
        ↓
добавление товара в Bag
        ↓
проверка состояния Bag
        ↓
изменение quantity
        ↓
проверка обновлённого состояния
        ↓
удаление товара
        ↓
проверка удаления
```

Дополнительно проверяются negative scenarios и несколько разных товаров в одной корзине.

[⬆️ К содержанию](#contents)

---

<a id="project-structure"></a>
## 📁 Структура проекта

```text
American_Eagle_python_automation
│
├── .github
│   └── workflows
│       └── tests.yml
│
├── docs
│   └── American_Eagle_Python_TestPlan_2026.pdf
│
├── api
│   └── ...
│
├── ui
│   ├── components
│   │   ├── footer_component.py
│   │   └── header_component.py
│   │
│   ├── pages
│   │   ├── account_page.py
│   │   ├── base_page.py
│   │   ├── home_page.py
│   │   ├── jeans_page.py
│   │   ├── mens_clothes_page.py
│   │   ├── product_page.py
│   │   ├── search_results_page.py
│   │   └── shopping_cart_page.py
│   │
│   ├── steps
│   │   ├── product_cart_steps.py
│   │   ├── product_catalog_steps.py
│   │   └── registration_steps.py
│   │
│   ├── config.py
│   └── constants.py
│
├── tests
│   ├── api
│   │   ├── test_bag_api.py
│   │   ├── test_browse_api.py
│   │   ├── test_inventory_api.py
│   │   └── test_token_api.py
│   │
│   ├── ui
│   │   ├── account
│   │   ├── home_page
│   │   └── mens_clothes
│   │
│   ├── conftest.py
│   └── test_smoke.py
│
├── utils
├── pytest.ini
├── requirements.txt
└── README.md
```

Такая структура разделяет:

- API clients / helpers;
- UI Pages;
- UI Components;
- reusable Steps;
- fixtures;
- tests;
- configuration;
- constants;
- utilities;
- CI configuration.

[⬆️ К содержанию](#contents)

---

<a id="cicd-result"></a>
## 📈 CI/CD результат

В проекте реализовано:

- раздельное выполнение **API + smoke** и UI тестов;
- headless Chrome для UI в CI;
- GitHub Secret для API credential;
- сохранение Allure results даже при ошибках тестового job;
- отдельные artifacts для API + smoke и UI;
- объединение результатов;
- отдельный job для формирования Allure Report;
- публикация отчёта через `gh-pages`;
- поддержка ручного запуска workflow;
- автоматический запуск при `push` и `pull_request`.

Отдельное внимание уделено стабильности тестов на реальном production-сайте:

- explicit waits;
- обработка marketing и regional popup overlays;
- централизованное закрытие blocking overlays;
- повторное получение элементов после DOM update;
- обработка `StaleElementReferenceException` и `ElementClickInterceptedException`;
- fallback-навигация при исчезновении временных UI-элементов;
- sale / regular price logic;
- динамический выбор доступного SKU и товара;
- отказ от фиксированных `sleep` в основных сценариях;
- ограниченная retry-логика только для нестабильных взаимодействий с динамическим DOM;
- ответственность Page Objects очищена от дублирующей логики после финального рефакторинга.

[⬆️ К содержанию](#contents)

---

## 🧩 Дополнительно

- ✅ Python 3.12
- ✅ Pytest
- ✅ Selenium WebDriver
- ✅ Requests
- ✅ Page Object Model
- ✅ Components
- ✅ Steps layer
- ✅ REST API automation
- ✅ UI automation
- ✅ Positive / Negative testing
- ✅ Smoke testing
- ✅ Known defect via `xfail`
- ✅ Allure reporting
- ✅ GitHub Actions CI
- ✅ GitHub Pages
- ✅ GitHub Secrets
- ✅ Test Plan
- ✅ Headless Chrome
- ✅ Работа с anti-bot ограничениями production-сайта
- ✅ Самостоятельная реализация вне учебной программы

---

<a id="author"></a>
## 👤 Автор

**Ilya Sidorychev**

GitHub: [ISmeneger](https://github.com/ISmeneger)

Проект разработан самостоятельно как развитие навыков **Python QA Automation** после обучения тестированию ПО в Университете ИТМО и как расширение профессионального AQA-портфолио вторым языком программирования.

[⬆️ К содержанию](#contents)

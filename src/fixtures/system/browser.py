import logging
import logging.config
import pytest
import allure
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="class")
def browser_context(pytestconfig):
    logging.config.fileConfig('logging.ini')

    bn = pytestconfig.getoption("--bn")
    if bn == "None" or bn is None:
        bn = pytestconfig.getini("browser_name") or "chromium"

    browser_type_name = "chromium" if bn == "chrome" else bn

    with allure.step(f"Запуск браузера {browser_type_name}"):
        playwright = sync_playwright().start()
        browser_launcher = getattr(playwright, browser_type_name)
        browser = browser_launcher.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        logging.info(f'Браузер {bn} запустился')

    yield context

    with allure.step("Закрытие браузера"):
        context.close()
        browser.close()
        playwright.stop()
        logging.info(f'Браузер {bn} закрылся')


@pytest.fixture(scope="class")
def page(browser_context):
    """Фикстура для создания новой страницы (вкладки)."""
    page = browser_context.new_page()
    return page
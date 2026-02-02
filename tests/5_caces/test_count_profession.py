import allure
import pytest
from playwright.sync_api import Page, expect


class TestCountProfession:
    @pytest.fixture
    def setup_count_profesion_test(self, page: Page):
        with allure.step("Открываем страницу профессий SkillBox"):
            page.goto("https://skillbox.ru/courses/")
            kolvo = page.locator("//button[contains(@class,'programs-filter-desktop__tab')]//span[contains(text(), 'Профессия')]")
        kolvo.click()
        with allure.step("Находим фильтр Програмирование"):
            esche = page.locator("//button[contains(@class, 'ui-load-more') and contains(., 'Ещё')]")
        return esche

    def test_count_profession(self, setup_count_profesion_test):
        '''Шаги:
-Перейти на сайт https://skillbox.ru/courses/
-Найти блочный элемент с информацией о профессиях.
-Запомнить количество отображаемых профессий — 175.
-Нажать на блок «Профессии».

Ожидаемые результаты:
-В кнопке после профессий отображается надпись
 «Ещё 10 профессий из 144».'''
        esche = setup_count_profesion_test
        with allure.step("Сравниваем подпись на кнопки под курсами"):
            expect(esche).to_contain_text("Ещё 12 программ из 163")

    def test_another_profession(self, setup_count_profesion_test, page: Page):
        '''Тест-кейс №2

        Шаги:
        -Перейти на сайт https://skillbox.ru/
        -Найти блочный элемент с информацией о профессиях.
        -Запомнить количество отображаемых профессий — 175.
        -Нажать на блок «Профессии».
        -Нажать на кнопку «Ещё 12 программ из 163».

        Ожидаемые результаты:
        -Проверить, что добавились новые блоки.
        -Кнопка после профессий отображает текст «Ещё 12 программ из 151».'''
        esche2 = setup_count_profesion_test
        with allure.step("Проверяем количество курсов на кнопке 'Еще 12 программ...'"):
            esche2 = page.locator("//button[contains(@class, 'ui-load-more') and contains(., 'Ещё')]")
            with allure.step("Нажимаем на кнопку 'Ещё'"):
                esche2.click()
            expect(esche2).to_contain_text("Ещё 12 программ из 163")

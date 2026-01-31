import pytest
from allure_commons._allure import step
from playwright.sync_api import Page, expect

class TestFiletrMenu:
    @pytest.mark.parametrize('profession_name, filter_names', [
    ("Программирование", ["Бэкенд-разработка", "Веб-разработка", "Анализ данных", "IT-инфраструктура", "Остальное"]),
    ("Дизайн", ["Цифровой дизайн", "Дизайн Среды", "Мода и Фотография", "Остальное"]),
     ("Маркетинг", ["Бренд-маркетинг", "Электронная коммерция", "Остальное"])
    ])

    def test_filter_menu(self, profession_name, filter_names, page: Page):
        '''Тест-кейс №3
Входные данные (массив):
Python
[
    ["Программирование", ["Бэкенд-разработка", "Веб-разработка", "Анализ данных", "IT-инфраструктура", "Остальное"]],
    ["Дизайн", ["Цифровой дизайн", "Дизайн Среды", "Мода и Фотография", "Остальное"]],
    ["Маркетинг", ["Бренд-маркетинг", "Электронная коммерция", "Остальное"]]
]
Шаги:
-Перейти на сайт https://skillbox.ru/courses/?type=profession
-Нажать на кнопку (название категории) из массива данных.

Ожидаемые результаты:
-Проверить, что в левой части фильтра находятся
 кнопки-фильтры конкретной подпрофессии из списка.'''
        with step('Открытие страницы https://skillbox.ru/code/?type=profession'):
            page.goto("https://skillbox.ru/code/?type=profession")

        with step('Выбор фильтра курсов'):
            page.get_by_role("link", name=profession_name, exact=True).first.click()
        with step("Ожидание появления программ"):
            filter_blocks =  page.query_selector_all('.programs-filter-directions__subitem > a')

        with step('Провверка кнопок фильтрации'):
            for actual_filter, expected_filter in zip(filter_blocks, filter_names):
                assert actual_filter.inner_text() == expected_filter
        assert True
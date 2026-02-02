import re
import playwright.sync_api
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, expect


class TestGithub4Cases:       # 1 Задание
    def test_github (self, page):
        page.goto("https://github.com/microsoft/vscode/issues")
        page.locator("#repository-input").fill("in:title bug")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        title_locator = page.locator("a[data-testid='issue-pr-title-link']")
        print(f"DEBUG: Найдено элементов: {title_locator.count()}")
        title_locator.first.wait_for(state="visible")
        assert title_locator.count() > 0, "Список задач пуст!"
        for issue in title_locator.all():
            clean_title = issue.text_content().lower()
            assert "bug" in clean_title, f"Нет слова 'bug' в заголовке {clean_title}"


    def test_author(self, page):
        page.goto("https://github.com/microsoft/vscode/issues")
        page.get_by_role("button", name="Author").click()
        page.get_by_placeholder("Filter authors").fill("bpasero")
        page.locator(".prc-ActionList-ItemLabel-81ohH", has_text="bpasero").click()
        page.wait_for_timeout(2000)
        issue_authors = page.locator('[data-testid="created-at"]').locator('a[data-hovercard-type="user"]')
        issue_authors.first.wait_for()
        count = issue_authors.count()
        assert count > 0, "Задачи автора bpasero не найдены!"
        for author_el in issue_authors.all():
            name = author_el.text_content().strip()
            if name:
                assert name == "bpasero", f"Найдена задача другого автора: {name}"
            print(f"Подтверждено: автор задачи — {name}")

    def test_advanced(self, page):
        page.goto("https://github.com/search/advanced")
        page.locator("#search_language").select_option("Python")
        stars = page.locator("#search_stars")
        stars.fill(">20000")
        file_name = page.locator("#search_filename")
        file_name.fill("environment.yml")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        stars_list = page.locator("a[href$='/stargazers']").all()
        for star_link in stars_list:
            aria_text = star_link.get_attribute("aria-label")
            if aria_text:
                count = int("".join(filter(str.isdigit, aria_text)))
                print(f"Проверка проекта: {count} звезд")
                assert count > 20000, f"Нашли проект с {count} звезд, что меньше 20000"


    def test_radiobtn(self, page):
        page.goto("https://skillbox.ru/code/")
        page.locator("//button[contains(.,'Профессия')]").click()
        page.locator("//button[contains(.,'Длительность')]").click()
        page.locator("//li[contains(.,'От 6 до 12 мес.')]").click()
        page.locator("//button[contains(.,'Тематика')]").click()
        page.locator("//li[contains(.,'Linux')]").click()
        page.locator("//button[contains(.,'Применить')]").click()
        #page.wait_for_timeout(2000)
        titles_elements = page.locator(".product-card-new__title")
        titles_elements.first.wait_for()
        links = []
        for el in titles_elements.all():
            url = el.get_attribute("href")
            if url:
                links.append(url)
            print(f"Список ссылок:, {len(links)}")
        keywords = ["python", "cyber", "devops", "security", "haker", "sysadmin"]
        for link in links:
            low_link = link.lower()
            if any(word in low_link for word in keywords):
                print(f"Подходит: {link}")
            else:
                print(f"Внимание! Ссылка {link} может не соответствовать фильтру.")

    def test_grafik(self,page):
        page.goto("https://github.com/microsoft/vscode/graphs/commit-activity")
        target_path = page.locator("path[aria-label*='1 Jun 2025']")
        target_path.hover()
        tooltip = page.locator(".highcharts-tooltip strong")
        actual_commits = tooltip.text_content()
        print(f"Найдено коммитов: {actual_commits}")
        assert actual_commits == "328", f"Ожидали 328, но получили {actual_commits}"








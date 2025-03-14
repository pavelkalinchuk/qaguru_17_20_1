import pytest
from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


@pytest.mark.parametrize('android_device_management', ['bstack', 'emulator'], indirect=True)
def test_search(android_device_management):
    with step("Кликаем на кнопке Skip для пропуска страницы приветствия"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")).click()

    with step("Закрываем окно Introducing"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/closeButton")).click()

    with step('Находим и кликаем на строке поиска'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()

    with step('Вводим текст для поиска'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')

    with step('Проверяем результаты поиска'):
        # Получить все элементы с результатами поиска
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))

        # Проверить, что список результатов не пуст
        results.should(have.size_greater_than(0))

        # Проверить, что первый результат содержит текст "Appium"
        results.first.should(have.text('Appium'))
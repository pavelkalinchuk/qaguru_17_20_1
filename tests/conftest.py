import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selene import browser

from utils.allure_attach import *


def find_apk_file(file_name):
    """
    Путь до файла .apk
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Директория текущего файла
    file_path = os.path.join(current_dir, f"../resources/{file_name}")  # Путь до файла
    return file_path


@pytest.fixture(scope='function')
def android_bstack_management():
    """Настройка браузера для работы в browserstack"""
    options = UiAutomator2Options().load_capabilities({
        'platformVersion': '9.0',
        'deviceName': 'Google Pixel 3',
        'app': 'bs://sample.app',
        # Настройки BrowserStack
        'bstack:options': {
            'projectName': 'First Python project',
            'buildName': 'browserstack-build-1',
            'sessionName': 'BStack first_test',
            # Учетные данные для авторизации на BrowserStack
            'userName': settings.BROWSERSTACK_USER_NAME,
            'accessKey': settings.BROWSERSTACK_ACCESS_KEY,
        }
    })
    # Инициализация удаленного драйвера
    with allure.step('Инициализация сессии приложения'):
        browser.config.driver = webdriver.Remote(
            settings.BROWSERSTACK_URL,  # URL BrowserStack
            options=options
        )

    yield browser

    add_screenshot(browser)
    add_xml(browser)
    # Получение ID сессии для прикрепления видео
    session_id = browser.driver.session_id
    add_bstack_video(session_id)

    browser.quit()


@pytest.fixture(scope='function')
def android_emulator_device_management():
    """Настройка браузера для работы в browserstack"""
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        'deviceName': 'emulator-5554',
        "automationName": "UiAutomator2",
        'app': find_apk_file("app-alpha-universal-release.apk"),
        "appWaitActivity": "org.wikipedia.*"
    })

    # Инициализация удаленного драйвера
    with allure.step('Инициализация сессии приложения'):
        browser.config.driver = webdriver.Remote(
            "http://127.0.0.1:4723/wd/hub",  # URL device emulator
            options=options
        )

    yield browser

    add_screenshot(browser)
    add_xml(browser)

    browser.quit()


@pytest.fixture(scope='function')
def web_browser_management():
    """Настройка браузера с прямыми значениями"""
    browser.config.base_url = 'https://www.wikipedia.org'
    browser.config.driver_name = 'chrome'
    browser.config.hold_driver_at_exit = False
    browser.config.window_width = '1024'
    browser.config.window_height = '768'
    browser.config.timeout = 3.0
    yield browser

    # Прикрепление скриншота к отчету Allure
    if browser.driver:
        try:
            add_screenshot(browser)
        except Exception as e:
            print(f"Ошибка при создании скриншота: {e}")
    browser.quit()

from selene import have, browser
from allure import step


def test_search(web_browser_management):
    with step('Запускаем браузер со страницей википедия'):
        browser.open('/')

    with step('Type search'):
        browser.element('#searchInput').type('AppImage')

    with step('Verify content found'):
        results = browser.all('.suggestion-link')
        results.should(have.size_greater_than(0))
        results.first.should(have.text('AppImage'))

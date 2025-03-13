import allure
from allure_commons.types import AttachmentType


from config import settings


def add_screenshot(browser):
    """Получение скриншота страницы сайта"""
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_logs(browser):
    """Получение логов сайта"""
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
    allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')


def add_html(browser):
    """Получение html-кода со страницы"""
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')


def add_xml(browser):
    """Получение xml-ника со страницы"""
    xml = browser.driver.page_source
    allure.attach(xml, name='screen xml dump', attachment_type=allure.attachment_type.XML)


def add_video_selenoid(browser):
    """Прикрепление видео из selenoid"""
    video_url = "https://selenoid.autotests.cloud/video/" + browser.driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>"
    allure.attach(html, 'video_' + browser.driver.session_id, AttachmentType.HTML, '.html')


def add_json_session(browser, session_id):
    """Получение информации о сессии"""
    json = browser.driver.session_id
    allure.attach(json.dumps(json, indent=4), name='session_info', attachment_type=allure.attachment_type.JSON)


def add_bstack_video(session_id):
    """Прикрепление видео из browserstack в allure-отчёт"""
    import requests
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(settings.BROWSERSTACK_USER_NAME, settings.BROWSERSTACK_ACCESS_KEY),
    ).json()
    print(bstack_session)
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import config


class Driver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_elem(self, css, wait=config.WAIT_ATTR):
        try:
            element = WebDriverWait(self, wait).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
            return element
        except TimeoutException:
            self.save_screenshot('error.png')
            raise TimeoutError


def get_driver(proxy=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    options.add_argument('--incognito')
    options.add_argument('--no-first-run')
    options.add_argument('--no-service-autorun')

    if proxy:
        import auth_plugin
        import zipfile
        manifest = auth_plugin.get_manifest()
        background_js = auth_plugin.get_background_js(*proxy)
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest)
            zp.writestr("background.js", background_js)
        options.add_extension(pluginfile)

    driver = Driver(config.PATH_DRIVER, options=options)
    driver.set_page_load_timeout(config.DRIVER_PAGE_LOAD_TIMEOUT)
    return driver

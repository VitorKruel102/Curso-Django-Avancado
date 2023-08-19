import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser

class RecipeBaseFunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = make_chrome_browser('--headless')
    
    def tearDown(self):
        self.browser.quit()

    def sleep(self, seconds=5):
        time.sleep(seconds)


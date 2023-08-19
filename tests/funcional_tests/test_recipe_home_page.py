import time

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = make_chrome_browser()
    
    def tearDown(self):
        self.browser.quit()

    def sleep(self, seconds=5):
        time.sleep(seconds)


class RecipesHomePageFuncionalTest(RecipeBaseFunctionalTest):


    def test_recipe_home_page_without_recipes_error_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No recipes found here', body.text)
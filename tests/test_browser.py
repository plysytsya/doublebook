import unittest
import inspect

from doublebook.browser import Browser


class BrowserTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        """Override TestCase's __init__ and let the base class handle the arguments."""
        super(BrowserTest, self).__init__(*args, **kwargs)

    def test_does_browser_start(self):
        print(f"Running Test Method : {inspect.stack()[0][3]}")
        self.browser = Browser(headless=True)
        self.browser.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=3)

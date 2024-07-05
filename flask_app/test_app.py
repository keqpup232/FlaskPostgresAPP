import random
import unittest
import psycopg2
import requests
import multiprocessing
import testing.postgresql
from app import app
from bs4 import BeautifulSoup
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

multiprocessing.set_start_method('fork')

# TEST ENV
# POSTGRES_DB=flask_db
# POSTGRES_PASSWORD=password
# POSTGRES_USER=sammy
# HOST_ENV=localhost

# Reference to testing.postgresql database instance
db = None
# Connection to the database used to set the database state before running each test
db_con = None
# Map of database connection parameters passed to the functions we're testing
db_conf = None


def slurp(path):
    """ Reads and returns the entire contents of a file """
    with open(path, 'r') as f:
        return f.read()


def converts_db_conf(db_conf):
    """ converts the dictionary configuration into a string for connecting the database """
    conf = ''
    for key, val in db_conf.items():
        if str(key) == 'database':
            key = 'dbname'
        conf = conf + str(key) + '=' + str(val) + ' '
    conf = conf[:-1]
    return conf


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        global db, db_con, db_conf
        db = testing.postgresql.Postgresql()
        db_conf = db.dsn()
        db_con = psycopg2.connect(**db_conf)
        # Commit changes immediately to the database
        db_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with db_con.cursor() as cur:
            cur.execute(slurp('./setup.sql'))

    def tearDown(self):
        db_con.close()
        db.stop()

    def test_200main(self):
        """ Check client is 200 """
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        """ check add user in test database """
        conf = converts_db_conf(db_conf)
        tester = app.test_client(self)
        tester.post("/", data={'db_test': 'test', 'name': 'Ivan', 'email': 'keqpup232@gmail.com', 'db_conf': conf})
        with db_con.cursor() as cur:
            cur.execute('SELECT name, email FROM users;')
            rows = cur.fetchall()
            self.assertEqual(rows, [('Ivan', 'keqpup232@gmail.com')])

    def test_add_unique(self):
        """ check add 2 identical users in test database """
        conf = converts_db_conf(db_conf)
        tester = app.test_client(self)

        tester.post("/", data={'db_test': 'test', 'name': 'Ivan', 'email': 'keqpup232@gmail.com', 'db_conf': conf})
        requests = tester.post("/", data={'db_test': 'test', 'name': 'Ivan', 'email': 'keqpup232@gmail.com',
                                          'db_conf': conf})
        soup = BeautifulSoup(requests.text, 'html.parser')
        error = soup.find_all('div', class_='error_exists', attrs={'style': 'display: flex;'})
        self.assertNotEqual(error, [])


class TestApp(LiveServerTestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_server_availability(self):
        response = requests.get(self.get_server_url())
        assert response.status_code == 200

    def test_empty_fields(self):
        driver = webdriver.Chrome()
        driver.get(self.get_server_url())
        textarea = driver.find_element(By.CSS_SELECTOR, ".name")
        textarea.send_keys("Ivan")
        submit_button = driver.find_element(By.CSS_SELECTOR, ".submit")
        submit_button.click()
        assert '<div class="error_null" style="display: flex;">' in driver.page_source
        driver.quit()

    def test_error_exists(self):
        driver = webdriver.Chrome()
        driver.get(self.get_server_url())
        textarea = driver.find_element(By.CSS_SELECTOR, ".name")
        textarea.send_keys("Ivan")
        textarea = driver.find_element(By.CSS_SELECTOR, ".email")
        textarea.send_keys("keqpup232@gmail.com")
        submit_button = driver.find_element(By.CSS_SELECTOR, ".submit")
        submit_button.click()
        assert '<div class="error_exists" style="display: flex;">' in driver.page_source
        driver.quit()

    def test_last5(self):
        driver = webdriver.Chrome()
        driver.get(self.get_server_url())
        textarea = driver.find_element(By.CSS_SELECTOR, ".name")
        email = "keqpup" + str(random.randint(1, 100)) + "@gmail.com"
        textarea.send_keys("Ivan")
        textarea = driver.find_element(By.CSS_SELECTOR, ".email")
        textarea.send_keys(email)
        submit_button = driver.find_element(By.CSS_SELECTOR, ".submit")
        submit_button.click()
        assert email in driver.page_source


if __name__ == '__main__':
    unittest.main()

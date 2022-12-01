import unittest
import requests
from RESERVATIONS import views
from RESERVATIONS import auth


class MyTestCase(unittest.TestCase):
    # Ensure login behaves correctly given the correct credential
    def test_login(self):
        # Ensure that Flask was set up correctly
        response = requests.get('http://127.0.0.1:5000/loginscreen')
        self.assertEqual(response.status_code, 200)

    def test_correct_login(self):
        response = requests.post('http://127.0.0.1:5000/loginscreen', data={'email': 'james@gmail.com', 'password1': 'quizzing'})
        self.assertTrue('Logged in successfully!' in response.text)

    def test_not_an_user_login(self):
        response = requests.post('http://127.0.0.1:5000/loginscreen', data={'email': 'xxx@gmail.com', 'password1': '12345678'})
        self.assertTrue('Email does not exist.' in response.text)

    def test_wrong_password_login(self):
        response = requests.post('http://127.0.0.1:5000/loginscreen',
                                 data={'email': 'james@gmail.com', 'password1': '1234567890'})
        self.assertTrue('Incorrect password, try again.' in response.text)

    def test_guest_reserve(self):
        response = requests.get('http://127.0.0.1:5000/homescreen')
        self.assertEqual(response.status_code, 200)

    def test_sign_up(self):
        response = requests.get('http://127.0.0.1:5000/registerpage')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginscreen', data={'email': 'james@gmail.com', 'password1': 'quizzing'})

        response = s.get('http://127.0.0.1:5000/logout')
        self.assertTrue('Logged out successfully!' in response.text)

    def test_account_page(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginscreen', data={'email': 'james@gmail.com', 'password1': 'quizzing'})
        response = s.get('http://127.0.0.1:5000/myaccount')
        self.assertEqual(response.status_code, 200)

    def test_get_reserve_page(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginscreen', data={'email': 'james@gmail.com', 'password1': 'quizzing'})
        response = s.get('http://127.0.0.1:5000/reserving')
        self.assertEqual(response.status_code, 200)

    def test_user_payment(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginscreen', data={'email': 'james@gmail.com', 'password1': 'quizzing'})
        response = s.get('http://127.0.0.1:5000/payments')
        self.assertEqual(response.status_code, 200)

    def test_get_user_reservations(self):
        s = requests.Session()
        s.post('http://127.0.0.1:5000/loginscreen', data={'email': 'james@gmail.com', 'password1': 'quizzing'})
        response = s.get('http://127.0.0.1:5000/reservations')
        self.assertEqual(response.status_code, 200)

    def test_Aboutus(self):
        response = requests.get('http://127.0.0.1:5000/aboutpage')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

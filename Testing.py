import os
import unittest
import tempfile

from main import create_app
from helpers.Value_interpreter import Value_interpreter

class TestingClass(unittest.TestCase):
    '''
        Setup and login/out
    '''
    def setUp(self):
        self.client_auth = {"email":"zach@hertzian.co.uk","password":"zac"}
        self.client = create_app()
        self.db_fd, self.client.config['DATABASE'] = tempfile.mkstemp()
        self.client.testing = True
        self.app = self.client.test_client()
    
    def login(self, auth=None):
        if auth is None:
            auth = self.client_auth
        return self.app.post('/login/', content_type='multipart/form-data', data=auth, follow_redirects=True)
        
    def logout(self):
        return self.app.get('/logout/', follow_redirects=True)
    
    def tearDown(self): 
        os.close(self.db_fd)
        os.unlink(self.client.config['DATABASE'])
    
    '''
        Basic page movement and logins.
    '''
    def test_home(self):
        p = self.app.get("/")
        assert b'<title>Home</title>' in p.data
        self.assertEqual(200, p.status_code)
    
    def test_login_and_logout(self):
        lg = self.login()
        assert b'You are logged in.' in lg.data
        self.assertEqual(200, lg.status_code)
        lg = self.logout()
        assert b'You have been logged out.' in lg.data
        self.assertEqual(200, lg.status_code)
        lg = self.login("hErTzIaN321")
        assert b'Password is invalid.' in lg.data
        self.assertEqual(200, lg.status_code)
    
    def test_get_page_logged_in(self):
        with self.client.test_client() as c:
            self.login()
            r = self.app.get('/menu')
            assert b'<title>Menu</title>' in r.data
            self.assertEqual(200, r.status_code)
    
    '''
        Check data pull from DB.
    '''
    def test_conv(self):
        VI = Value_interpreter()
        print( VI.From_ten( 123, 8 ) )
        print( VI.To_ten( "0o123", 8 ) )
        print( VI.Convert_a_to_b( "0o123", 8, 10 ) )
        return None
    
    
    
    
    
        
if __name__ == '__main__':
    unittest.main()
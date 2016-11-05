import app
import unittest


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_correct_http_response(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_correct_delete(self):
        resp = self.app.delete('/api/send/testplan123')
        self.assertEqual(resp.status_code, 204)

    def test_correct_send_one(self):
        resp = self.app.delete('/api/send/testplan123')
        resp = self.app.post('/api/send/testplan123',data='{"coldata": "data1"}',content_type='application/json')
        self.assertEqual(resp.data, b'1')

    def test_correct_send_two(self):
        resp = self.app.delete('/api/send/testplan123')
        resp = self.app.post('/api/send/testplan123',data='{"coldata": "data1"}',content_type='application/json')
        resp = self.app.post('/api/send/testplan123',data='{"coldata": "data2"}',content_type='application/json')
        self.assertEqual(resp.data, b'2')

    def test_correct_get(self):
        resp = self.app.post('/api/send/testplan123',data='{"coldata": "data1"}',content_type='application/json')
        resp = self.app.get('/api/get/testplan123', content_type='application/json')
        #self.assertEqual(resp.data['coldata'], b'testplan123')
        pass

    def test_bad_path(self):
        resp = self.app.get('/api/badcall')
        self.assertEqual(resp.status_code, 404)

    def test_bad_key(self):
        resp = self.app.get('/api/get/testplan456')
        #self.assertEqual(resp.status_code, 1)
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python
import app
import unittest

ct = 'application/json'


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_top_level_http_response(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_get_no_results(self):
        resp = self.app.get('/api/get/testplan123', content_type=ct)
        self.assertEqual(resp.status_code, 404)

    def test_getstatus_no_results(self):
        resp = self.app.get('/api/status/1', content_type=ct)
        self.assertEqual(resp.status_code, 404)

    def test_poststatus_no_results(self):
        d = '{"status": "2"}'
        resp = self.app.post('/api/status/1', data=d, content_type=ct)
        self.assertEqual(resp.status_code, 404)

    def test_delete_no_results(self):
        resp = self.app.delete('/api/send/testplan123')
        self.assertEqual(resp.status_code, 404)

    def test_delete_results(self):
        resp = self.app.delete('/api/send/testplan123')
        d = '{"msgdata": "data1"}'
        resp = self.app.post('/api/send/testplan123', data=d, content_type=ct)
        resp = self.app.delete('/api/send/testplan123')
        self.assertEqual(resp.status_code, 204)

    def test_post_result_one(self):
        resp = self.app.delete('/api/send/testplan123')
        d = '{"msgdata": "data1"}'
        resp = self.app.post('/api/send/testplan123', data=d, content_type=ct)
        self.app.delete('/api/send/testplan123')
        self.assertEqual(resp.data, b'1')

    def test_post_result_two(self):
        resp = self.app.delete('/api/send/testplan123')
        d = '{"msgdata": "data1"}'
        resp = self.app.post('/api/send/testplan123', data=d, content_type=ct)
        d = '{"msgdata": "data2"}'
        resp = self.app.post('/api/send/testplan123', data=d, content_type=ct)
        self.app.delete('/api/send/testplan123')
        self.assertEqual(resp.data, b'2')

    def test_get_results(self):
        resp = self.app.delete('/api/send/testplan123')
        d = '{"msgdata": "data1"}'
        resp = self.app.post('/api/send/testplan123', data=d, content_type=ct)
        resp = self.app.get('/api/get/testplan123', content_type=ct)
        self.app.delete('/api/send/testplan123')
        self.assertEqual(resp.status_code, 200)

    def test_getstatus_results(self):
        resp = self.app.delete('/api/send/testplan123')
        d = '{"msgdata": "data1"}'
        resp = self.app.post('/api/send/testplan123', data=d, content_type=ct)
        resp = self.app.get('/api/status/1', content_type=ct)
        self.app.delete('/api/send/testplan123')
        self.assertEqual(resp.status_code, 200)

    def test_poststatus_results(self):
        resp = self.app.delete('/api/send/testplan123')
        d = '{"msgdata": "data1"}'
        resp = self.app.post('/api/send/testplan123', data=d, content_type=ct)
        d = '{"status": "2"}'
        resp = self.app.post('/api/status/1', data=d, content_type=ct)
        self.app.delete('/api/send/testplan123')
        self.assertEqual(resp.status_code, 200)

    def test_bad_path(self):
        resp = self.app.get('/api/badcall')
        self.assertEqual(resp.status_code, 404)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

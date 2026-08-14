import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app as app_module


class EditSongsAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.original_cwd = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)
        Path('REDergaran.json').write_text(
            json.dumps({'SongNum': {'1': {'key': 'C', 'speed': '100', 'style': 'Test', 'song_type': 'All', 'timeSig': '4/4', 'Comments': ''}}}),
            encoding='utf-8',
        )
        self.original_testing = app_module.app.config['TESTING']
        app_module.app.config.update(TESTING=True)
        self.client = app_module.app.test_client()

    def tearDown(self):
        app_module.app.config['TESTING'] = self.original_testing
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def authenticate(self, csrf_token=None):
        with self.client.session_transaction() as test_session:
            test_session['user'] = {
                'access_token': 'test-access-token',
                'userinfo': {'email': 'editor@example.com'},
            }
            if csrf_token:
                test_session['_csrf_token'] = csrf_token

    def test_anonymous_post_is_unauthorized(self):
        for data in (None, {}, {'unused': 'value'}):
            response = self.client.post('/editsongs', data=data)

            self.assertEqual(response.status_code, 401)

    @patch.object(app_module, 'isUserAllowed', return_value=False)
    def test_authenticated_non_editor_post_is_forbidden(self, _is_user_allowed):
        self.authenticate()

        response = self.client.post('/editsongs')

        self.assertEqual(response.status_code, 403)

    @patch.object(app_module, 'isUserAllowed', return_value=True)
    def test_editor_post_requires_csrf_token(self, _is_user_allowed):
        self.authenticate()

        response = self.client.post('/editsongs', data={'action': 'lookup', 'book': 'REDergaran', 'songNum': '1'})

        self.assertEqual(response.status_code, 400)

    @patch.object(app_module, 'isUserAllowed', return_value=True)
    def test_missing_required_form_data_is_a_bad_request(self, _is_user_allowed):
        self.authenticate('csrf-token')

        response = self.client.post('/editsongs', data={
            'csrf_token': 'csrf-token',
            'action': 'lookup',
        })

        self.assertEqual(response.status_code, 400)

    @patch.object(app_module, 'isUserAllowed', return_value=True)
    def test_invalid_request_is_controlled_before_file_access(self, _is_user_allowed):
        self.authenticate('csrf-token')

        response = self.client.post('/editsongs', data={
            'csrf_token': 'csrf-token',
            'action': 'lookup',
            'book': 'not-a-book',
            'songNum': '1',
        })

        self.assertEqual(response.status_code, 422)

    @patch.object(app_module, 'isUserAllowed', return_value=True)
    def test_authorized_editor_can_save_a_song(self, _is_user_allowed):
        self.authenticate('csrf-token')

        response = self.client.post('/editsongs', data={
            'csrf_token': 'csrf-token',
            'action': 'save',
            'book': 'REDergaran',
            'songNum': '1',
            'key': 'D',
            'speed': '120',
            'style': 'Updated',
            'Song Type': 'Worship Song',
            'Time Signature': '3/4',
            'Comments': 'Updated by test',
        })

        self.assertEqual(response.status_code, 200)
        saved_data = json.loads(Path('REDergaran.json').read_text(encoding='utf-8'))
        self.assertEqual(saved_data['SongNum']['1']['key'], 'D')
        self.assertNotIn('SongNum', saved_data['SongNum'])

    def test_session_cookie_security_configuration(self):
        self.assertTrue(app_module.app.config['SESSION_COOKIE_SECURE'])
        self.assertTrue(app_module.app.config['SESSION_COOKIE_HTTPONLY'])
        self.assertEqual(app_module.app.config['SESSION_COOKIE_SAMESITE'], 'Lax')

        response = self.client.post('/editsongs')
        cookie = response.headers['Set-Cookie']
        self.assertIn('Secure', cookie)
        self.assertIn('HttpOnly', cookie)
        self.assertIn('SameSite=Lax', cookie)


if __name__ == '__main__':
    unittest.main()

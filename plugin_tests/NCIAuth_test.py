from tests import base
from girder.models.user import User
import json
from girder.models.setting import Setting
from girder.constants import SettingKey
from girder.api.rest import getApiUrl


def setUpModule():
    base.enabledPlugins.append('NCIAuth')
    base.startServer()


def tearDownModule():
    base.stopServer()


class NCIAuthTest(base.TestCase):

    def setUp(self):
        base.TestCase.setUp(self)

        # girder.plugins is not available until setUp is running
        global PluginSettings
        from girder.plugins.NCIAuth.constants import PluginSettings

        self.adminUser = User().createUser(
            email='NCIAuthTest@gmail.com',
            login='nciauthtest',
            firstName='nciauth',
            lastName='test',
            password='123456789',
            admin=True
        )

        # Specifies which test account (typically 'new' or 'existing') a
        # redirect to a provider will simulate authentication for
        self.accountType = None

    def testDeriveLogin(self):
        """
        Unit tests the _deriveLogin method of the provider classes.
        """
        from girder.plugins.NCIAuth.rest import NCILogin

        login = NCILogin._deriveLogin('1234@mail.com', 'John', 'Doe')
        self.assertEqual(login, 'johndoe')

        login = NCILogin._deriveLogin('hello#world#foo@mail.com', 'A', 'B')
        self.assertEqual(login, 'helloworldfoo')

        login = NCILogin._deriveLogin('hello.world@mail.com', 'A', 'B', 'user2')
        self.assertEqual(login, 'user2')

        # This should conflict with the saved admin user
        login = NCILogin._deriveLogin('NCIAuthTest@gmail.com', 'nciauth', 'test', 'nciauthtest')
        self.assertEqual(login, 'nciauthtest1')

    def _testSettings(self, providerInfo):
        Setting().set(SettingKey.REGISTRATION_POLICY, 'closed')
        self.accountType = 'new'

        # We should get an empty listing when no providers are set up
        params = {
            'key': PluginSettings.PROVIDERS_ENABLED,
            'value': []
        }
        resp = self.request('/system/setting', user=self.adminUser, method='PUT', params=params)
        self.assertStatusOk(resp)

        resp = self.request('/nciLogin/loginCallback', exception=True)
        self.assertStatusOk(resp)
        self.assertFalse(resp.json)

        # Set up provider normally
        params = {
            'list': json.dumps([
                {
                    'key': PluginSettings.PROVIDERS_ENABLED,
                    'value': [providerInfo['id']]
                }, {
                    'key': PluginSettings.NCI_CLIENT_ID,
                    'value': providerInfo['id']
                }, {
                    'key': PluginSettings.NCI_RETURN_URL,
                    'value': providerInfo['return_url']
                }, {
                    'key': PluginSettings.NCI_LOGIN_URL,
                    'value': providerInfo['login_url']
                }, {
                    'key': PluginSettings.NCI_VALIDATION_URL,
                    'value': providerInfo['validation_url']
                }
            ])
        }
        resp = self.request('/system/setting', user=self.adminUser, method='PUT', params=params)
        self.assertStatusOk(resp)
        # # No need to re-fetch and test all of these settings values; they will
        # # be implicitly tested later
        resp = self.request('/nciLogin/loginCallback', exception=True)
        self.assertStatusOk(resp)
        expect = 'https://bar.com?returnUrl=' + '/'.join((getApiUrl(), 'nciLogin', 'callback'))
        self.assertEqual(resp.json, expect)

    def testRest(self):
        providerInfo = {
            'id': 'foo',
            'return_url': 'https://foo.com',
            'login_url': 'https://bar.com',
            'validation_url': 'qwerasdf'
        }

        self._testSettings(providerInfo)

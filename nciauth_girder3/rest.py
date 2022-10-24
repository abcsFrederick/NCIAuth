from girder.api.rest import Resource,boundHandler
from girder.api.describe import Description, autoDescribeRoute
from girder.api import access
import cherrypy
# from .DMSAuth import DMSAuthentication
import re
import requests
import json

from girder import events
from girder.models.user import User
from girder.models.setting import Setting
from girder.exceptions import RestException, ValidationException
from girder.api.rest import Resource, getApiUrl
from girder.models.token import Token
from girder.settings import SettingKey
from girder.utility import config
from . import constants

class NCILogin(Resource):

  """API Endpoint for users in the NCI account."""
  def __init__(self):
    super(NCILogin, self).__init__()
    self.resourceName = 'nciLogin'

    self.route('GET', ('endpoint',), self.getEndpoint)
    # self.route('GET', ('callback',), self.callback)
    self.route('GET', ('loginCallback',), self.login)
    self.route('GET', ('cors',), self.getToken)

  @access.public
  @autoDescribeRoute(
    Description('GET Current token from cross origin request.'))
  def getToken(self):
    if 'cookie' not in cherrypy.request.headers:
      return None
    token = cherrypy.request.headers['cookie'].split('girderToken=')[-1]
    # print(Token().load(token, force=True, objectId=False))
    return token

  @access.public
  @autoDescribeRoute(
    Description('GET Current NIH Login url.'))
  def login(self):
    # https://stsstg.nih.gov/ dev
    # https://sts.nih.gov/ pro
    print(cherrypy.request.params)
    code = cherrypy.request.params['code']
    data = {'grant_type': 'authorization_code',
            'code': code,
            # 'client_id': 'cilogon:/client_id/' + Setting().get('NCIAuth.NCI_client_id'),
            'client_id': Setting().get('NCIAuth.NCI_client_id'),
            'client_secret': Setting().get('NCIAuth.NCI_client_secret'),
            'redirect_uri': Setting().get('NCIAuth.NCI_api_url') + '/nciLogin/loginCallback'
          }
    # res = json.loads(requests.post('https://cilogon.org/oauth2/token', data).content) # /auth/oauth/v2/token
    res = json.loads(requests.post('https://stsstg.nih.gov/auth/oauth/v2/token', data).content)

    id_token = res['id_token']
    access_token = res['access_token']
    expire = res["expires_in"]
    data = {'access_token': access_token}
    userinfo = requests.post('https://stsstg.nih.gov/openid/connect/v1/userinfo', data)
    # userinfo = requests.post('https://cilogon.org/oauth2/userinfo', data) # /openid/connect/v1/userinfo
    user = json.loads(userinfo.content)

    email = user["email"]
    firstName = user["first_name"]
    lastName = user["last_name"]
    username = user["userid"]
    user = User().findOne({'email': email})

    setId = not user
    dirty = False
    if not user:
      policy = Setting().get(SettingKey.REGISTRATION_POLICY)

      if policy == 'closed':
        ignore = Setting().get(PluginSettings.IGNORE_REGISTRATION_POLICY)
        if not ignore:
          raise RestException(
            'Registration on this instance is closed. Contact an '
            'administrator to create an account for you.')
      login = self._deriveLogin(email, firstName, lastName, userName=username)
      user = User().createUser(
        login=login, password=None, firstName=firstName, lastName=lastName, email=email)
    else:
      # Migrate from a legacy format where only 1 provider was stored
      if isinstance(user.get('oauth'), dict):
        user['oauth'] = [user['oauth']]
        dirty = True
      # Update user data from provider
      if email != user['email']:
        user['email'] = email
        dirty = True
      # Don't set names to empty string
      if firstName != user['firstName'] and firstName:
        user['firstName'] = firstName
        dirty = True
      if lastName != user['lastName'] and lastName:
        user['lastName'] = lastName
        dirty = True

      if setId:
        user.setdefault('NCI_credential', []).append(
          {
            'provider': 'NCI'
          })
        dirty = True
      if dirty:
        user = User().save(user)

    girderToken = self.sendAuthTokenCookie(user)

    # cherrypy.response.cookie['girderToken']['path'] = Setting().get('NCIAuth.NCI_return_url')
    # cherrypy.response.cookie['girderToken'] = str(girderToken['_id'])
    raise cherrypy.HTTPRedirect(Setting().get('NCIAuth.NCI_return_url'))

  @access.public
  @autoDescribeRoute(
    Description('GET Current NIH Login url.'))

  def getEndpoint(self):
    api_url = Setting().get(constants.PluginSettings.NCI_API_URL)
    if Setting().get(constants.PluginSettings.PROVIDERS_ENABLED):
      # callbackUrl = "https://cilogon.org/authorize/?" \
      # "response_type=code&scope=openid%20email%20profile" \
      # "&client_id=cilogon:/client_id/{}" \
      # "&state=h4u9b4D-0ogWpAD_j-g3hc7bVyE" \
      # "&redirect_uri={}/nciLogin/CIloginCallback" \
      # "&skin=nih".format(Setting().get('NCIAuth.NCI_client_id'), api_url)
      
      authorization_endpoint = 'https://stsstg.nih.gov/auth/oauth/v2/authorize?' \
      'client_id={}' \
      '&response_type=code' \
      '&redirect_uri={}/nciLogin/loginCallback' \
      '&scope=phone+email+profile+openid'.format(Setting().get('NCIAuth.NCI_client_id'), api_url)
      return authorization_endpoint
      # return Setting().get('NCIAuth.NCI_login_url') + '?returnUrl=' + '/'.join((url, 'nciLogin', 'callback'))
    else:
      return []
  # @access.public
  # @autoDescribeRoute(
  #   Description('API Endpoint for users in the NCI account.'))

  # @classmethod
  # DMS method
  # def callback(self):
  #   # print cherrypy.request.params['token']
  #   token = cherrypy.request.params['token']

  #   validation = DMSAuthentication("ncifivgSvc", "%/2L4?*Q&{rQ3g~", 2)
  #   userInfo = validation.validateToken(token)

  #   #validation with service 
  #   NCIemail = userInfo["email"]
  #   NCIfirstName = userInfo["first_name"]
  #   NCIlastName = userInfo["last_name"]
  #   NCIid = userInfo["userID"]

    
  #   user = User().findOne({'email': NCIemail})

  #   setId = not user
  #   dirty = False
  #   if not user:
  #     policy = Setting().get(SettingKey.REGISTRATION_POLICY)

  #     if policy == 'closed':
  #       ignore = Setting().get(PluginSettings.IGNORE_REGISTRATION_POLICY)
  #       if not ignore:
  #         raise RestException(
  #           'Registration on this instance is closed. Contact an '
  #           'administrator to create an account for you.')
  #     login = self._deriveLogin(NCIemail, NCIfirstName, NCIlastName,NCIid)

  #     user = User().createUser(
  #       login=login, password=None, firstName=NCIfirstName, lastName=NCIlastName, email=NCIemail)
  #   else:
  #     # Migrate from a legacy format where only 1 provider was stored
  #     if isinstance(user.get('oauth'), dict):
  #       user['oauth'] = [user['oauth']]
  #       dirty = True
  #     # Update user data from provider
  #     if NCIemail != user['email']:
  #       user['email'] = NCIemail
  #       dirty = True
  #     # Don't set names to empty string
  #     if NCIfirstName != user['firstName'] and NCIfirstName:
  #       user['firstName'] = NCIfirstName
  #       dirty = True
  #     if NCIlastName != user['lastName'] and NCIlastName:
  #       user['lastName'] = NCIlastName
  #       dirty = True

  #   if setId:
  #     user.setdefault('NCI_credential', []).append(
  #       {
  #         'provider': 'NCI'
  #       })
  #     dirty = True
  #   if dirty:
  #     user = User().save(user)

  #   girderToken = self.sendAuthTokenCookie(user)

  #   raise cherrypy.HTTPRedirect(Setting().get('NCIAuth.NCI_return_url'))

  #   # try:
  #   #   redirect = redirect.format(girderToken=str(girderToken['_id']))
  #   # except KeyError:
  #   #   pass  # in case there's another {} that's not handled by format

  #   # raise cherrypy.HTTPRedirect(redirect)

  @classmethod
  def _deriveLogin(self, email, firstName, lastName, userName=None):
    """
    Attempt to automatically create a login name from existing user
    information from OAuth2 providers. Attempts to generate it from the
    username on the provider, the email address, or first and last name. If
    not possible, returns None and it is left to the caller to generate
    their own login for the user or choose to fail.

    :param email: The email address.
    :type email: str
    """
    # Note, the user's OAuth2 ID should never be used to form a login name,
    # as many OAuth2 services consider that to be private data

    for login in self._generateLogins(email, firstName, lastName, userName):
      login = login.lower()

      if self._testLogin(login):
        return login

    raise Exception('Could not generate a unique login name for %s (%s %s)'
            % (email, firstName, lastName))

  @classmethod
  def _generateLogins(self, email, firstName, lastName, userName=None):
    """
    Generate a series of reasonable login names for a new user based on
    their basic information sent to us by the provider.
    """
    # If they have a username on the other service, try that
    if userName:
      yield userName
      userName = re.sub(r'[\W_]+', '', userName)
      yield userName

      for i in range(1, 6):
        yield '%s%d' % (userName, i)

    # Next try to use the prefix from their email address
    prefix = email.split('@')[0]
    yield prefix
    yield re.sub(r'[\W_]+', '', prefix)

    # Finally try to use their first and last name
    yield '%s%s' % (firstName, lastName)

    for i in range(1, 6):
      yield '%s%s%d' % (firstName, lastName, i)

  @classmethod
  def _testLogin(self, login):
    """
    When attempting to generate a username, use this to test if the given
    name is valid.
    """
    try:
      User()._validateLogin(login)
    except ValidationException:
      # Still doesn't match regex, we're hosed
      return False

    # See if this is already taken.
    user = User().findOne({'login': login})

    return not user


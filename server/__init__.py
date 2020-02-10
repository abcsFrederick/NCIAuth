
from girder.constants import SettingKey, SettingDefault
from girder.utility import config, setting_utilities
from . import rest, constants

@setting_utilities.validator(constants.PluginSettings.PROVIDERS_ENABLED)
def validateProvidersEnabled(doc):
    if not isinstance(doc['value'], (list, tuple)):
        raise ValidationException('The enabled providers must be a list.', 'value')

@setting_utilities.validator(constants.PluginSettings.IGNORE_REGISTRATION_POLICY)
def validateIgnoreRegistrationPolicy(doc):
    if not isinstance(doc['value'], bool):
        raise ValidationException('Ignore registration policy setting must be boolean.', 'value')
@setting_utilities.validator({
    constants.PluginSettings.NCI_CLIENT_ID,
    constants.PluginSettings.NCI_API_URL,
    constants.PluginSettings.NCI_RETURN_URL,
    constants.PluginSettings.NCI_LOGIN_URL,
    constants.PluginSettings.NCI_VALIDATION_URL
})
def validateOtherSettings(event):
    pass

	
def load(info):
	
	info['apiRoot'].nciLogin = rest.NCILogin()

	SettingDefault.defaults[constants.PluginSettings.PROVIDERS_ENABLED] = []
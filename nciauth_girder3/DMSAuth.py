# import requests
# import getpass
# from requests_ntlm import HttpNtlmAuth
# from xml.etree import ElementTree
# from girder.models.setting import Setting
# class DMSAuthentication:
#     "A Python class for utilizing DMS's Authentication service."
#     """Instantiate class with service account username and password as arguments.
#     If you are using Python 2, pass a third paramater to constructor that is not equal to 3.
#     Pass the authentication validation token returned from login to validateToken().  
#     User information will be stored in attribute SSO_USER_ATTRIBUTES.  
    
#     Production Login: https://ncifrederick.cancer.gov/SignIn/NihLoginIntegration.axd
#     DEV Login: https://ncif-f5.ncifcrf.gov/SignIn/NihLoginIntegration.axd?returnUrl=RETURN_URL
    
#     Make sure the appropriate (dev or production) SSO_DMS_TOKEN_CONSUMER_URL definition is uncommented."""

#     def __init__(self, SSO_SERVICE_ACCOUNT_USERNAME, SSO_SERVICE_ACCOUNT_PASSWORD, python_version=3):
#         self.python_version = python_version
#         self.SSO_SERVICE_ACCOUNT_USERNAME = SSO_SERVICE_ACCOUNT_USERNAME
#         self.SSO_SERVICE_ACCOUNT_PASSWORD = SSO_SERVICE_ACCOUNT_PASSWORD
#         # print Setting().get('NCIAuth.NCI_Validation_url')
#         #Development Token Consumer Service
#         self.SSO_DMS_TOKEN_CONSUMER_URL = Setting().get('NCIAuth.NCI_validation_url')

#         #Production Token Consumer Service
#         #self.SSO_DMS_TOKEN_CONSUMER_URL = 'https://services.ncifcrf.gov/FederatedAuthentication/v1.0/TokenConsumer.svc'
#         self.SSO_USER_ATTRIBUTE = "{http://schemas.datacontract.org/2004/07/Dms.Css.Core.FederatedAuthentication.Services}"
#         self.SSO_USER_PrincipalName = self.SSO_USER_ATTRIBUTE + "UserPrincipalName"
#         self.SSO_USER_FIRSTNAME = self.SSO_USER_ATTRIBUTE + "FirstName"
#         self.SSO_USER_LASTNAME = self.SSO_USER_ATTRIBUTE + "LastName"
#         self.SSO_USER_EMAIL = self.SSO_USER_ATTRIBUTE + "Email"
#         self.SSO_PRE_TOKEN_SERVICE_DATA = """<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing">
#           <s:Header>
#             <a:Action s:mustUnderstand="1">http://tempuri.org/ITokenConsumer/ConsumeToken</a:Action>
#             <a:ReplyTo>
#               <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
#             </a:ReplyTo>
#             <a:To s:mustUnderstand="1">""" + self.SSO_DMS_TOKEN_CONSUMER_URL + """</a:To>
#           </s:Header>
#           <s:Body>
#             <ConsumeToken xmlns="http://tempuri.org/">
#               <token>"""
#         self.SSO_POST_TOKEN_SERVICE_DATA = """</token>
#             </ConsumeToken>
#           </s:Body>
#         </s:Envelope>
#         """
#         self.SSO_CONSUME_TOKEN_RESULT = "{http://www.w3.org/2003/05/soap-envelope}Body/{http://tempuri.org/}ConsumeTokenResponse/{http://tempuri.org/}ConsumeTokenResult"
#         self.SSO_USER_ATTRIBUTES = {
#             "first_name": "",
#             "last_name": "",
#             "email": ""
#         }

#     def validateToken(self,token):
#         data = self.SSO_PRE_TOKEN_SERVICE_DATA + token + self.SSO_POST_TOKEN_SERVICE_DATA
#         headers = {
#             "Content-Type": 'application/soap+xml;charset=UTF-8',
#             "Expect": "100-continue"}
#         if self.python_version == 3:
#             data_arg = bytes(data,"utf-8")
#         else:
#             data_arg = bytes(data)

#         token_service_response = requests.post(self.SSO_DMS_TOKEN_CONSUMER_URL, data_arg, auth=HttpNtlmAuth(self.SSO_SERVICE_ACCOUNT_USERNAME, self.SSO_SERVICE_ACCOUNT_PASSWORD), headers=headers, verify=False)

#         response_xml = ElementTree.fromstring(token_service_response.content)
#         token_result = response_xml.find(self.SSO_CONSUME_TOKEN_RESULT)
#         self.SSO_USER_ATTRIBUTES["userID"] = token_result.find(self.SSO_USER_PrincipalName).text[:token_result.find(self.SSO_USER_PrincipalName).text.index('@')]
#         self.SSO_USER_ATTRIBUTES["first_name"] = token_result.find(self.SSO_USER_FIRSTNAME).text
#         self.SSO_USER_ATTRIBUTES["last_name"] = token_result.find(self.SSO_USER_LASTNAME).text
#         self.SSO_USER_ATTRIBUTES["email"] = token_result.find(self.SSO_USER_EMAIL).text

#         return self.SSO_USER_ATTRIBUTES
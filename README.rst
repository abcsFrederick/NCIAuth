===============
NCIAuth-girder3
===============

Girder Plugin for NIH AD authentication.
Version for Girder V3 adapted by KnowledgeVis from original here: https://github.com/abcsFrederick/NCIAuth

--------

Request you own CIlogon id and secret at:
https://cilogon.org/oauth2/register 

#### Example of register form

Client Name: fr-s-your-server

Contact Email: youremail@nih.gov

Home URL: https://fr-s-your-server

Callback URLs: https://fr-s-your-server/api/v1/nciLogin/CIloginCallback

`You can add more Callback urls later, but 'api/v1/nciLogin/CIloginCallback' is necessary.`

Client Type: Confidential

Scopes: All for detail info

Refresh Tokens: No

After you have client Id and secret (recommand to save it somewhere), go to https://fr-s-your-server/#plugins/NCIAuth/config to fill and save configuration.

If you use [LoginView](https://github.com/girder/girder/blob/2.x-maintenance/clients/web/src/views/layout/LoginView.js) that provides by girder, you will see the NCI logo for clicking and sign-in.
import { registerPluginNamespace } from '@girder/core/pluginUtils';

import * as NCI_Login_plugin from '.';

import './routes';
registerPluginNamespace('NCI_Login_plugin', NCI_Login_plugin);

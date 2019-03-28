/* eslint-disable import/first */

import events from 'girder/events';
import router from 'girder/router';
import { exposePluginConfig } from 'girder/utilities/PluginUtils';

exposePluginConfig('NCIAuth', 'plugins/NCIAuth/config');

import ConfigView from './views/ConfigView';
router.route('plugins/NCIAuth/config', 'NCIAuth', function () {
    events.trigger('g:navigateTo', ConfigView);
});

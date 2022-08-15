/* eslint-disable import/first */

import events from '@girder/core/events';
import router from '@girder/core/router';
import { exposePluginConfig } from '@girder/core/utilities/PluginUtils';

exposePluginConfig('nciauth_girder3', 'plugins/NCIAuth/config');

import ConfigView from './views/ConfigView';
router.route('plugins/NCIAuth/config', 'NCIAuth', function () {
    events.trigger('g:navigateTo', ConfigView);
});

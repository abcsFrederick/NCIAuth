import LoginView from 'girder/views/layout/LoginView';
import { wrap } from 'girder/utilities/PluginUtils';

import NCIAuthLoginView from './NCIAuthLoginView';


wrap(LoginView, 'render', function (render) {
    render.call(this);
    new NCIAuthLoginView({
        el: this.$('.modal-body'),
        parentView: this,
        enablePasswordLogin: this.enablePasswordLogin
    }).render();
    return this;
});

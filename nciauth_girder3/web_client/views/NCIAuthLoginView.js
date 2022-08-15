import $ from 'jquery';
import _ from 'underscore';

import View from '@girder/core/views/View';
import { restRequest } from '@girder/core/rest';
import { splitRoute } from '@girder/core/misc';

import OAuthLoginViewTemplate from '../templates/oauthLoginView.pug';
import '../stylesheets/oauthLoginView.styl';

var NCIAuthLoginView = View.extend({
    events: {
        'click .g-oauth-button-NCI': function (event) {
            var providerId = $(event.currentTarget).attr('g-provider');
            var provider = _.findWhere(this.providers, {id: providerId});
            window.location = provider.url;
        }
    },

    initialize: function (settings) {
        var redirect = settings.redirect || splitRoute(window.location.href).base;
        this.modeText = settings.modeText || 'log in';
        this.providers = null;
        this.enablePasswordLogin = _.has(settings, 'enablePasswordLogin') ? settings.enablePasswordLogin : true;

        restRequest({
            method: 'GET',
            url: 'nciLogin/endpoint',
        }).done(_.bind((res)=>{
            if(res.length){
                this.providers = [{
                    id: 'NCI',
                    name: 'NCI',
                    hasAuthorizedOrigins: true,
                    instructions: 'NCI support'
                }];
                this.providers[0].url = res;
                this.render();
            }
            
        },this));
    },  

    render: function () {
        console.log(this.providers)
        if (this.providers === null) {
            return this;
        }
        var buttons = [];
        _.each(this.providers, function (provider) {
            var btn = this._buttons[provider.id];

            if (btn) {
                btn.providerId = provider.id;
                btn.text = provider.name;
                buttons.push(btn);
                console.log(buttons)
            } else {
                console.warn('Unsupported OAuth2 provider: ' + provider.id);
            }
        }, this);

        if (buttons.length) {
            this.$el.append(OAuthLoginViewTemplate({
                modeText: this.modeText,
                buttons: buttons,
                enablePasswordLogin: this.enablePasswordLogin
            }));
        }

        return this;
    },

    _buttons: {
        NCI: {
            icon: 'gplus',
            class: 'g-oauth-button-NCI'
        }
    }
});

export default NCIAuthLoginView;

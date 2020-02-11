import $ from 'jquery';
import _ from 'underscore';

import PluginConfigBreadcrumbWidget from 'girder/views/widgets/PluginConfigBreadcrumbWidget';
import View from 'girder/views/View';
import { getApiRoot, restRequest } from 'girder/rest';
import events from 'girder/events';

import ConfigViewTemplate from '../templates/configView.pug';
import '../stylesheets/configView.styl';

var ConfigView = View.extend({
    events: {
        'submit .g-oauth-provider-form': function (event) {
            event.preventDefault();
            var providerId = $(event.target).attr('provider-id');
            this.$('#g-oauth-provider-' + providerId + '-error-message').empty();

            this._saveSettings(providerId, [{
                key: 'NCIAuth.' + providerId + '_api_url',
                value: this.$('#g-oauth-provider-' + providerId + '-api-url').val().trim()
            }, {
                key: 'NCIAuth.' + providerId + '_return_url',
                value: this.$('#g-oauth-provider-' + providerId + '-return-url').val().trim()
            }, {
                key: 'NCIAuth.' + providerId + '_login_url',
                value: this.$('#g-oauth-provider-' + providerId + '-login-url').val().trim()
            }, {
                key: 'NCIAuth.' + providerId + '_validation_url',
                value: this.$('#g-oauth-provider-' + providerId + '-validation-url').val().trim()
            }]);
        },

        'change .g-ignore-registration-policy': function (event) {
            restRequest({
                method: 'PUT',
                url: 'system/setting',
                data: {
                    key: 'NCIAuth.ignore_registration_policy',
                    value: $(event.target).is(':checked')
                }
            }).done(() => {
                events.trigger('g:alert', {
                    icon: 'ok',
                    text: 'Setting saved.',
                    type: 'success',
                    timeout: 3000
                });
            });
        }
    },

    initialize: function () {
        this.providers = [{
            id: 'NCI',
            name: 'NCI',
            icon: 'gplus',
            hasAuthorizedOrigins: true,
            instructions: 'NCI support'
        }];
        this.providerIds = _.pluck(this.providers, 'id');

        var settingKeys = ['NCIAuth.ignore_registration_policy'];
        _.each(this.providerIds, function (id) {
            settingKeys.push('NCIAuth.' + id + '_api_url');
            settingKeys.push('NCIAuth.' + id + '_return_url');
            settingKeys.push('NCIAuth.' + id + '_login_url');
            settingKeys.push('NCIAuth.' + id + '_validation_url');
        }, this);

        restRequest({
            method: 'GET',
            url: 'system/setting',
            data: {
                list: JSON.stringify(settingKeys)
            }
        }).done((resp) => {
            this.settingVals = resp;
            this.render();
        });
    },

    render: function () {
        var origin = window.location.protocol + '//' + window.location.host,
            _apiRoot = getApiRoot();

        if (_apiRoot.substring(0, 1) !== '/') {
            _apiRoot = '/' + _apiRoot;
        }

        this.$el.html(ConfigViewTemplate({
            origin: origin,
            apiRoot: _apiRoot,
            providers: this.providers
        }));

        if (!this.breadcrumb) {
            this.breadcrumb = new PluginConfigBreadcrumbWidget({
                pluginName: 'NCI login',
                el: this.$('.g-config-breadcrumb-container'),
                parentView: this
            }).render();
        }

        if (this.settingVals) {
            _.each(this.providerIds, function (id) {
                this.$('#g-oauth-provider-' + id + '-api-url').val(
                    this.settingVals['NCIAuth.' + id + '_api_url']);
                this.$('#g-oauth-provider-' + id + '-return-url').val(
                    this.settingVals['NCIAuth.' + id + '_return_url']);
                this.$('#g-oauth-provider-' + id + '-login-url').val(
                    this.settingVals['NCIAuth.' + id + '_login_url']);
                this.$('#g-oauth-provider-' + id + '-validation-url').val(
                    this.settingVals['NCIAuth.' + id + '_validation_url']);
            }, this);

            var checked = this.settingVals['NCIAuth.ignore_registration_policy'];
            this.$('.g-ignore-registration-policy').attr('checked', checked ? 'checked' : null);
        }

        return this;
    },

    _saveSettings: function (providerId, settings) {
        settings.push({
            key: 'NCIAuth.providers_enabled',
            value: _.filter(this.providerIds, function (id) {
                return !!this.$('#g-oauth-provider-' + id + '-return-url').val();
            }, this)
        });

        restRequest({
            method: 'PUT',
            url: 'system/setting',
            data: {
                list: JSON.stringify(settings)
            },
            error: null
        }).done(() => {
            events.trigger('g:alert', {
                icon: 'ok',
                text: 'Settings saved.',
                type: 'success',
                timeout: 3000
            });
        }).fail((resp) => {
            this.$('#g-oauth-provider-' + providerId + '-error-message').text(
                resp.responseJSON.message);
        });
    }
});

export default ConfigView;

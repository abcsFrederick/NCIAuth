import View from 'girder/views/View';
import LoginTemplate from '../templates/loginTemplate.pug';


var loginPage = View.extend({
	initialize:function(setting){
		this.$el.html(LoginTemplate({
			url:setting.returnUrl
		}));
	}
});

export default loginPage;
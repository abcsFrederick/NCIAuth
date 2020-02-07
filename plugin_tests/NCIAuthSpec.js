girderTest.importPlugin('NCIAuth');
girderTest.startApp();

describe('Test the SSR plugin', function () {
    it('should support async execution of test preparation and expectations', function () {
        runs(function () {
            $('.g-oauth-button-NCI').click();
        });
        waitsFor(function () {
            console.log(window.location.href);
            expect(window.location.href).toBe('https://');
        }, 'Redirect to ', 750);
    });
});

from tornado.web import UIModule


class UiModule(UIModule):
    def render(self, *args, **kwargs):
        return 'I am ui module'


class Advertisement(UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('06html.html')

    def css_files(self):
        return "/static/css/King_Chance_Layer7.css"

    def javascript_files(self):
        return [
            "/static/js/jquery_1_7.js",
            "/static/js/King_Chance_Layer.js",
            "/static/js/King_layer_test.js", ]
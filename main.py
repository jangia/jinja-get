#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo
import time


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        params = {"sporocilo": "Tukaj sem tudi jaz, MainHandler"}

        return self.render_template("hello.html", params=params)

    def post(self):
        dodatno = "Uporabnik je vpisal: "
        rezultat = self.request.get("vnos")

        sporocilo = Sporocilo(vnos=rezultat)
        sporocilo.put()

        skupaj = dodatno + rezultat
        params = {'skupaj': skupaj}
        return self.render_template("hello.html", params=params)

class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Sporocilo.query(Sporocilo.izbrisan == False).fetch()
        params = {"seznam": seznam}

        return self.render_template("seznam_sporocil.html", params=params)


class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)


class RezultatHandler(BaseHandler):
    def post(self):
        dodatno = "Uporabnik je vpisal: "
        rezultat = self.request.get("vnos")
        skupaj = dodatno + rezultat
        return self.write(skupaj)


class ProjektiHandler(BaseHandler):

    def get(self):
        self.render_template('projekti.html')


class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        vnos = self.request.get("vnos")
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.vnos = vnos
        sporocilo.put()
        time.sleep(0.1)
        return self.redirect_to("seznam-sporocil")

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("izbrisi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        # sporocilo.key.delete()
        sporocilo.izbrisan = True
        sporocilo.put()
        time.sleep(0.1)
        return self.redirect_to("seznam-sporocil")

class BlogHandler(BaseHandler):

    def get(self):
        return self.render_template('blog.html')

    def post(self):
        # self.neki()
        return self.response.write('Post Details of ninja!')

    def put(self):
        return self.response.write('Put Details of ninja!')

    def neki(self):
        return self.response.write('Neki Details of ninja!')

    def delete(self):
        return self.response.write('delete Details of ninja!')

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/projekti', ProjektiHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler, name="seznam-sporocil"),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/uredi', UrediSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/izbrisi', IzbrisiSporociloHandler),
], debug=True)

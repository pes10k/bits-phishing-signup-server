import tornado.web
from tornado import gen
import lepl.apps.rfc3696
import datetime
import config

email_validator = lepl.apps.rfc3696.Email()

class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        # If we're not in debugging mode (ie we're in "production"),
        # send down HTTP Strict Transport Security header to make sure
        # we're only visited via https
        if not config.debug:
            self.set_header('Strict-Transport-Security',
                            'max-age=16070400; includeSubDomains')
        super(BaseHandler, self).prepare()

class MainHandler(BaseHandler):
    TEMPLATE = "main.html"

    def get(self):
        self.render(MainHandler.TEMPLATE)

class SignupHandler(BaseHandler):

    TEMPLATE = "signup.html"
    VALID_DATE_LOCATIONS = (
        '2014-09-30--11--seo-1325',
        '2014-09-30--15--seo-1000',
        '2014-10-01--13--seo-1000',
        '2014-10-02--10--seo-1325',
        '2014-10-02--11--seo-1325',
        '2014-10-02--12--seo-1325',
        '2014-10-02--13--seo-1325',
        '2014-10-02--16--seo-1325',
        '2014-10-03--10--seo-1325',
        '2014-10-03--12--seo-1325',
        '2014-10-03--13--seo-1325',
        '2014-10-03--14--seo-1325',
        '2014-10-03--16--seo-1325',
    )

    def get(self):
        self.render(SignupHandler.TEMPLATE, errors=False, complete=False)

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        errors = []

        try:
            email = self.get_argument("email")
            if not email_validator(email):
                errors.append("Invalid email address")
        except tornado.web.MissingArgumentError:
            errors.append("'Email' field is required")

        try:
            date_location = self.get_argument("date_location")
            if date_location not in SignupHandler.VALID_DATE_LOCATIONS:
                errors.append("Invalid date / location submitted")
        except tornado.web.MissingArgumentError:
            errors.append("'Date / Location' field is required")

        are_errors = len(errors) > 0

        if are_errors:
            self.render(SignupHandler.TEMPLATE, errors=errors, complete=False)
            return

        db = self.settings['db']
        doc = {"email": email, "location": date_location, "timestamp": datetime.datetime.now()}
        yield db.registrations.insert(doc)
        self.render(SignupHandler.TEMPLATE, errors=False, complete=True)


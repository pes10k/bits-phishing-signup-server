import tornado.web
from tornado import gen
import lepl.apps.rfc3696
import datetime

email_validator = lepl.apps.rfc3696.Email()

class MainHandler(tornado.web.RequestHandler):
    TEMPLATE = "main.html"

    def get(self):
        self.render(MainHandler.TEMPLATE)

class SignupHandler(tornado.web.RequestHandler):

    TEMPLATE = "signup.html"
    VALID_DATE_LOCATIONS = (
        '2014-09-30--11--seo-1325',
        '2014-09-30--15--seo-1000',
        '2014-10-01--13--seo-1000',
        '2014-10-02--11--seo-1325',
        '2014-10-02--13--seo-1325',
        '2014-10-02--16--seo-1325',
        '2014-10-03--13--seo-1325',
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


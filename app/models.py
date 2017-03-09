from . import db

class UserProfile(db.Model):
    userid = db.Column(db.String(8), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    biography = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    created_on = db.Column(db.DateTime())
    profile_image = db.Column(db.String(80))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.userid)  # python 2 support
        except NameError:
            return str(self.userid)  # python 3 support

    def __repr__(self):
        return '<User %r %r>' % (self.username)
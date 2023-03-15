from exts import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.name


class Apis(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    method = db.Column(db.String(10))
    path = db.Column(db.String(100), index=True)

    def __repr__(self):
        return '<Api %r>' % self.title


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id'))
    payload = db.Column(db.Text())
    response = db.Column(db.Text())
    response_type = db.Column(db.String(10), default='str')

    def __repr__(self):
        return '<Result %r>' % self.id


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100))
    method = db.Column(db.String(10))
    payload = db.Column(db.Text())
    response = db.Column(db.Text())
    creation_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __repr__(self):
        return '<Record %r>' % self.id

from application import db, create_app
app = create_app(config='settings')
db.app = app

db.create_all()

from application import create_app

app = create_app(config='settings')
app.run()

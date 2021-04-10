from app import create_app

app = create_app()
app.config["SECRET_KEY"] = "you-will-never-guess"

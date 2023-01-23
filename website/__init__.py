from flask import Flask



def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "yeet yeet baby delete"

    from .views import views
    from .chapter_1 import chapter_1
    from .chapter_2 import chapter_2
    from .chapter_3 import chapter_3
    from .chapter_4 import chapter_4

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(chapter_1, url_prefix="/")
    app.register_blueprint(chapter_2, url_prefix="/")
    app.register_blueprint(chapter_3, url_prefix="/")
    app.register_blueprint(chapter_4, url_prefix="/")

    return app

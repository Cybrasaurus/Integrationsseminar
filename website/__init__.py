"""
The MIT License (MIT)

Copyright (c) <2023> Cybrasaurus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
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

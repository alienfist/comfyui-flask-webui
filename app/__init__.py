from flask import Flask, render_template
from flask_migrate import Migrate
import logging
from ext import db

migrate = Migrate()


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)

    from .index import index
    from .stickers import stickers
    from .txt2img import txt2img
    from .img2img import img2img
    from .art_photo import art_photo
    from .change_face import change_face
    from .style_fusion import style_fusion
    from .id_photo import id_photo
    from .couple import couple
    from .setting import setting
    from .about import about

    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(stickers, url_prefix='/stickers')
    app.register_blueprint(txt2img, url_prefix='/txt2img')
    app.register_blueprint(img2img, url_prefix='/img2img')
    app.register_blueprint(art_photo, url_prefix='/art_photo')
    app.register_blueprint(change_face, url_prefix='/change_face')
    app.register_blueprint(style_fusion, url_prefix='/style_fusion')
    app.register_blueprint(id_photo, url_prefix='/id_photo')
    app.register_blueprint(couple, url_prefix='/couple')
    app.register_blueprint(setting, url_prefix='/setting')
    app.register_blueprint(about, url_prefix='/about')

    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.exception('An exception occurred: %s', e)
        return render_template("error.html", message=str(e)), 500

    @app.errorhandler(404)
    def page_not_found(e):
        logging.exception('An exception occurred: %s', e)
        return render_template('404.html'), 404

    return app

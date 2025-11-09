from flask import Flask
from flask_security import Security

from flask_restful import Api

from controllers.database import db
from controllers.config import Config
from controllers.user_datastore import user_datastore

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    security = Security(app, user_datastore)

    api = Api(app, prefix='/api')

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_role = user_datastore.find_or_create_role(name='user', description='Regular user')

        admin_user = user_datastore.find_user(email="admin@gmail.com")
        if not admin_user:
            user_datastore.create_user(
                username="admin",
                email="admin@gmail.com",
                password="admin123",
                roles=[admin_role]
            )
        else:
            if not admin_user.has_role('admin'):
                user_datastore.add_role_to_user(admin_user, admin_role)

        db.session.commit()

    return app, api

app, api = create_app()

# @app.route('/')
# def index():
#     return {
#         "message": "Welcome to the Flask Application!",
#         "status": True
#     }, 200


from authentication_apis import LoginAPI, LogoutAPI, RegisterAPI
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RegisterAPI, '/register')



if __name__ == "__main__":
    app.run(debug=True)
from flask_security import SQLAlchemyUserDatastore
from controllers.database import db

from controllers.models import User, Role, UserRoles

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
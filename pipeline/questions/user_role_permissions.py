from pipeline.config import Config
from pipeline import db
from pipeline.db import Permission, User

def check_permissions(permission,userid):
    desired_permission = db.db.session.query(Permission).filter(Permission.title==permission).first()
    user_permissions = []
    query = db.db.session.query(db.User).filter(db.User.id==userid).first()
    roles = query.user_role
    for role in roles:
        user_permissions += role.permission_role
    if desired_permission in user_permissions:
        return True
    else:
        return False    

def check_role(role,userid):
    user = db.db.session.query(db.User).filter(db.User.id==userid).first()
    roles = user.user_role
    roles_users = []
    for row in roles:
        roles_users.append(row.title)
    if role in roles_users:
        return True
    else:
        return False
# auth.py
users = ["user1", "user2", "admin"]
user_roles = {
    "user1": ["alpha"],
    "user2": ["beta"],
    "admin": ["alpha", "beta"]
}

def authenticate_user(user):
    """
    Authenticates the user by checking if the user exists in the list of valid users.
    Returns True if the user is valid, False otherwise.
    """
    return user in users

def check_permissions(user, permission):
    """
    Checks if the user has the required permission.
    Returns True if the user has the permission, False otherwise.
    """
    roles = user_roles.get(user, [])
    return permission in roles

def can_invoke_runtime(user, runtime):
    """
    Determines if the user can invoke the specified runtime based on their permissions.
    Returns True if the user can invoke the runtime, False otherwise.
    """
    if runtime == "RuntimeAlpha":
        return check_permissions(user, "alpha")
    elif runtime == "RuntimeBeta":
        return check_permissions(user, "beta")
    else:
        return False
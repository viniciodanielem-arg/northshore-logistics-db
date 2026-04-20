def has_role(current_user, allowed_roles):
    if not current_user:
        return False
    return current_user.get("role_name") in allowed_roles


def require_role(current_user, allowed_roles):
    if not has_role(current_user, allowed_roles):
        raise PermissionError("You do not have permission to perform this action.")
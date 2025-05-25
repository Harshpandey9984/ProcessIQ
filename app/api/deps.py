"""
Dependencies for API endpoints.
"""

from enum import Enum
from typing import Generator, Dict, Optional, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.endpoints.auth import get_current_active_user, get_current_user

# Permission types
class Permission(str, Enum):
    """Permission types for different operations."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

# Role-based permissions mapping
ROLE_PERMISSIONS = {
    "admin": [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
    "manager": [Permission.READ, Permission.WRITE],
    "user": [Permission.READ, Permission.WRITE],
    "viewer": [Permission.READ],
}

# Resource-specific permissions (for more granular control)
RESOURCE_PERMISSIONS = {
    "digital_twin": {
        "admin": [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
        "manager": [Permission.READ, Permission.WRITE, Permission.DELETE],
        "user": [Permission.READ, Permission.WRITE],
        "viewer": [Permission.READ],
    },
    "simulation": {
        "admin": [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
        "manager": [Permission.READ, Permission.WRITE],
        "user": [Permission.READ, Permission.WRITE],
        "viewer": [Permission.READ],
    },
    "model": {
        "admin": [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
        "manager": [Permission.READ, Permission.WRITE],
        "user": [Permission.READ],
        "viewer": [Permission.READ],
    },
}

# Reusable dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def get_current_user_dependency() -> Dict:
    """
    Dependency to get the current authenticated user.
    """
    return Depends(get_current_user)

def get_current_active_user_dependency() -> Dict:
    """
    Dependency to get the current active authenticated user.
    """
    return Depends(get_current_active_user)

def get_admin_user_dependency() -> Dict:
    """
    Dependency to get the current active authenticated admin user.
    """
    async def get_admin_user(current_user: Dict = Depends(get_current_active_user)) -> Dict:
        if current_user["role"] != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized. Admin privileges required."
            )
        return current_user
    
    return Depends(get_admin_user)

def check_permission(permission: Permission, resource_type: Optional[str] = None):
    """
    Check if a user has the given permission for the specified resource type.
    
    Args:
        permission: The permission to check
        resource_type: Optional resource type for more specific permission checking
    """
    async def permission_checker(current_user: Dict = Depends(get_current_active_user)) -> Dict:
        user_role = current_user.get("role", "user")
        
        # Check resource-specific permissions first if a resource type is provided
        if resource_type and resource_type in RESOURCE_PERMISSIONS:
            role_permissions = RESOURCE_PERMISSIONS[resource_type].get(user_role, [])
            if permission in role_permissions:
                return current_user
        
        # Fall back to general role permissions
        role_permissions = ROLE_PERMISSIONS.get(user_role, [])
        if permission in role_permissions:
            return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. {permission} access required."
        )
    
    return Depends(permission_checker)

# Convenience functions for common permission checks
def require_read(resource_type: Optional[str] = None):
    """Require read permission for a resource."""
    return check_permission(Permission.READ, resource_type)

def require_write(resource_type: Optional[str] = None):
    """Require write permission for a resource."""
    return check_permission(Permission.WRITE, resource_type)

def require_delete(resource_type: Optional[str] = None):
    """Require delete permission for a resource."""
    return check_permission(Permission.DELETE, resource_type)

def require_admin():
    """Require admin permission."""
    return check_permission(Permission.ADMIN)

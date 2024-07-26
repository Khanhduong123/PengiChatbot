from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

RESOURCES_FOR_ROLES = {
    'admin': {
        'resource1': ['read', 'write', 'delete'],
        'resource2': ['read', 'write'],
    },
    'user': {
        'resource1': ['read'],
        'resource2': ['read', 'write'],
    }
}
USERS = {
    'user1': {'username': 'user1', 'password': 'password', 'role': 'user'},
    'admin1': {'username': 'admin1', 'password': 'adminpassword', 'role': 'admin'}
}
EXLUDED_PATHS = ['docs', 'openapi.json']

def translate_method_to_action(method: str) -> str:
    method_permission_mapping = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'update',
        'DELETE': 'delete',
    }
    return method_permission_mapping.get(method.upper(), 'read')

def has_permission(user_role, resource_name, required_permission):
    if user_role in RESOURCES_FOR_ROLES and resource_name in RESOURCES_FOR_ROLES[user_role]:
        return required_permission in RESOURCES_FOR_ROLES[user_role][resource_name]
    return False
class RBACMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
      request_method = str(request.method).upper()
      action = translate_method_to_action(request_method)
      resource = request.url.path[1:]
      if not resource in EXLUDED_PATHS:
            admin1 = USERS['admin1'] # Switch between user and admin by commenting out this or the next line
            #user1 = USERS['user1'] 
            if not has_permission(admin1['role'], resource, action):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
      response = await call_next(request)
      return response
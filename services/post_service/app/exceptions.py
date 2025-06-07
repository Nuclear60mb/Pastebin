
class AppException(Exception):
    status_code = 400 
    detail = "Application error"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.detail
        super().__init__(self.detail)


class NotFoundException(AppException):
    status_code = 404
    detail = "Resource not found"


class PostNotFoundError(NotFoundException):
    def __init__(self, post_id):
        super().__init__(f"Post with ID {post_id} not found")


class UserNotFoundError(NotFoundException):
    def __init__(self, user_id):
        super().__init__(f"User with ID {user_id} not found")


class ForbiddenException(AppException):
    status_code = 403
    detail = "Access denied"


class UnauthorizedException(AppException):
    status_code = 401
    detail = "Unauthorized access"


class ValidationException(AppException):
    status_code = 422
    detail = "Validation failed"

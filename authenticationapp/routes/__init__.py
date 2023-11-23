"""Contains routes for the authentication app."""

# Third party imports
from django.http import HttpRequest
from ninja import Router

# Local application imports
from ..database import ClientRepository, UserRepository
from ..schemas.input import NewUser, UserCredentials
from ..schemas.output import ErrorSchema, SuccessSchema

auth_router = Router(tags=["Authentication"])

USER_REPO = UserRepository()
CLIENT_REPO = ClientRepository()


@auth_router.post("/register", response={201: SuccessSchema, 400: ErrorSchema})
def register(
    request: HttpRequest, payload: NewUser
) -> tuple[int, SuccessSchema | ErrorSchema]:
    """
    Register a user/create a new user.

    Create a new user with the given credentials.

    Args:
        request (HttpRequest): The request object.
        payload (NewUser): The payload containing the credentials.

    Returns:
        (int, SuccessSchema | ErrorSchema): The status code and the response as a schema.
    """
    if USER_REPO.is_authenticated(request.user):  # type: ignore
        return 400, ErrorSchema(detail="User is already authenticated.")

    username = payload.username
    email = payload.email
    password = payload.password
    password_confirmation = payload.password_confirmation
    first_name = payload.first_name
    last_name = payload.last_name

    try:
        USER_REPO.create_user(
            username=username,
            email=email,
            password=password,
            password_confirmation=password_confirmation,
            first_name=first_name,
            last_name=last_name,
        )
    except ValueError as e:
        return 400, ErrorSchema(detail=str(e))

    return 201, SuccessSchema(message="User successfully registered.")


@auth_router.post("/login", response={200: SuccessSchema, 400: ErrorSchema})
def login(
    request: HttpRequest, payload: UserCredentials
) -> tuple[int, SuccessSchema | ErrorSchema]:
    """
    Login a user.

    Login a user with the given credentials.

    Args:
        request (HttpRequest): The request object.
        payload (LoginSchema): The payload containing the credentials.

    Returns:
        (int, SuccessSchema | ErrorSchema): The status code and the response as a schema.
    """
    if USER_REPO.is_authenticated(request.user):  # type: ignore
        return 400, ErrorSchema(detail="User is already authenticated.")

    username = payload.username
    password = payload.password
    login_was_successful = USER_REPO.login_user(request, username, password)

    if login_was_successful:
        status_code = 200
        response_message = "User successfully logged in."
        return status_code, SuccessSchema(message=response_message)
    else:
        status_code = 400
        response_message = "Invalid credentials."
        return status_code, ErrorSchema(detail=response_message)


@auth_router.get("/logout", response={200: SuccessSchema, 400: ErrorSchema})
def logout(request: HttpRequest) -> tuple[int, SuccessSchema | ErrorSchema]:
    """
    Logout a user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        (int, SuccessSchema | ErrorSchema): The status code and the response as a schema.
    """
    logout_was_successful = USER_REPO.logout_user(request)

    if logout_was_successful:
        return 200, SuccessSchema(message="User successfully logged out.")
    else:
        return 400, ErrorSchema(detail="User is not authenticated.")


@auth_router.get("/token", response={200: SuccessSchema, 400: ErrorSchema})
def token(request: HttpRequest) -> tuple[int, SuccessSchema | ErrorSchema]:
    """
    Get token of a user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        (int, SuccessSchema | ErrorSchema): The status code and the response as a schema.
    """
    if not USER_REPO.is_authenticated(request.user):  # type: ignore
        return 400, ErrorSchema(detail="User is not authenticated.")

    user_api_token = CLIENT_REPO.generate_token(request.user)  # type: ignore
    return 200, SuccessSchema(message=user_api_token)

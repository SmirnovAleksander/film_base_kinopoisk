from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    # TODO Update url
    tokenUrl="auth/jwt/token"
)
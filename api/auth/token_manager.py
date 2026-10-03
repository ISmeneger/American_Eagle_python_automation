from api.client.token_client import TokenClient


class TokenManager:

    def __init__(self):
        self.token_client = TokenClient()
        self._guest_token = None

    def get_guest_token(self) -> str:
        if self._guest_token is None:
            self._guest_token = self.token_client.get_guest_token()

        return self._guest_token

    def get_guest_authorization_header(self) -> str:
        token = self.get_guest_token()

        return f"Bearer {token}"
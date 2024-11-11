from fastapi import Request, Response, Depends

from settings import COOKIE_KEY


class AccessTokenRepository:
    def __init__(self, response: Response, request: Request):
        self.response = response
        self.request = request

    def create(self, token: str):
        self.response.set_cookie(COOKIE_KEY, token)

    def get(self):
        return self.request.cookies.get(COOKIE_KEY)

    def delete(self):
        return self.response.delete_cookie(COOKIE_KEY)
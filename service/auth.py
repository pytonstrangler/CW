import constants
import datetime
import calendar
import jwt

from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise Exception()

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                raise Exception()

        data = {
            'username': user.username,
            'role': user.role
        }
        access_token_lt = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        data['exp'] = calendar.timegm(access_token_lt.timetuple())
        access_token = jwt.encode(data, constants.JWT_SECRET, algorithm=constants.JWT_ALGORITHM)

        refresh_token_lt = datetime.datetime.utcnow() + datetime.timedelta(days=180)
        data['exp'] = calendar.timegm(refresh_token_lt.timetuple())
        refresh_token = jwt.encode(data, constants.JWT_SECRET, algorithm=constants.JWT_ALGORITHM)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def check_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=constants.JWT_SECRET, algorithms=[constants.JWT_ALGORITHM, ])
        username = data.get('username')

        user = self.user_service.get_by_username(username)

        if user is None:
            raise Exception()
        return self.generate_token(username, user.password, is_refresh=True)

    def valid_token(self, access_token, refresh_token):
        for t in [access_token, refresh_token]:
            try:
                jwt.decode(jwt=t, key=constants.JWT_SECRET, algorithms=[constants.JWT_ALGORITHM])
            except Exception as e:
                return True
            return False


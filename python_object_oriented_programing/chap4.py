'''
@Description: python面向对象编程-chap4-异常处理
@Version: 
@Author: liguoying
@Date: 2019-05-23 11:06:09
'''
import hashlib

# class IndividualError(Exception):
#     pass


# raise IndividualError("这是一个自定义的异常类型。")

####身份验证

class User:
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = self._encrypt_pw(passwd)
        self.is_logged_in = False
    

    def _encrypt_pw(self, passwd):
        hash_str = self.username + passwd
        hash_str = hash_str.encode('utf-8')
        return hashlib.sha256(hash_str).hexdigest()
    

    def check_passwd(self, passwd):
        encrypted = self._encrypt_pw(passwd)
        return encrypted == self.passwd


# 定义业务异常类
class AuthException(Exception):
    def __init__(self, username, user=None):
        super().__init__(username, user)
        self.username = username
        self.user = user


class UsernameAlreadyExists(AuthException):
    pass


class PasswordTooShort(AuthException):
    pass


class InvalidUsername(AuthException):
    pass


class InvalidPassword(AuthException):
    pass

class NotLoggedInError(AuthException):
    pass

class NotPermitError(AuthException):
    pass


class Authenticator:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, passwd):
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(passwd) < 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username, passwd)

    def login(self, username, passwd):
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)
        
        if not user.check_passwd(passwd):
            raise InvalidPassword(username, user)
        
        user.is_logged_in = True
        return True
    
    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in
        return False

authenticator = Authenticator()

class Authorizor:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}
    
    # 添加新权限
    def add_permission(self, perm_name):
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            self.permissions[perm_name] = set()
        else:
            raise PermissionError("Permission Exists")
    
    def permit_user(self, perm_name, username):
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.add(username)
    
    def check_permission(self, perm_name, username):
        if not self.authenticator.is_logged_in(username):
            raise NotLoggedInError(username)
        try:
            perm_set = self.permissions[username]
        except KeyError:
            raise PermissionError("Permission Does not exist")
        else:
            if username not in perm_set:
                raise NotPermitError(username)
            else:
                return True
    
authorizor = Authorizor(authenticator)
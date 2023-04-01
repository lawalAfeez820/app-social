from passlib.context import CryptContext


class Password():
    def __init__(self, algorithm:CryptContext):
        self.algorithm = algorithm
        pass

    def hash_ps(self,password: str):
        return self.algorithm.hash(password)
    
    def verify_hash(self, confirm_password:str, password: str):
        return self.algorithm.verify(confirm_password, password)
    
    def verify_plain(self, confirm_password:str, password: str):
        return confirm_password == password

    

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = Password(pwd_context)

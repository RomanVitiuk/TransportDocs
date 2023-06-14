from passlib.hash import bcrypt


class PasswordManager:
    @classmethod
    def create_password(cls, pswd: str) -> str:
        return bcrypt.hash(pswd)

    @classmethod
    def verify_password(cls, pswd: str, hashed_pswd: str) -> bool:
        return bcrypt.verify(pswd, hashed_pswd)

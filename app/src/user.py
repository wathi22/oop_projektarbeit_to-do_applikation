import hashlib

class User:
    
    def __init__ (
            self,
            id: int = None,
            firstname: str = '',
            lastname: str = '',
            email: str = '',
            password_hash: str = ''
        ):

        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hash = password_hash

    def hash_password(self, password: str):
        # Hashing des Passworts (hier nur als Beispiel, in der Praxis sollte ein sicherer Hashing-Algorithmus verwendet werden)
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.password_hash

    def check_password(self, password: str) -> bool:
        # Überprüft, ob das gehashte Passwort mit dem gespeicherten Hash übereinstimmt
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def full_name(self) -> str:
        # Gibt den vollständigen Namen des Benutzers zurück
        return f"{self.firstname} {self.lastname}"
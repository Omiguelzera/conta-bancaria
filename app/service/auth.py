from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models.account import Account
from app.database import SessionLocal, get_db

# Definindo o esquema de criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Segredo para a geração do token JWT
SECRET_KEY = "mysecretkey"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 


class AuthService:

    def get_password_hash(password: str) -> str:
        """
        Gera uma senha criptografada a partir da senha fornecida.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha fornecida é válida comparando-a com a senha criptografada.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
        """
        Gera o token JWT.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obtém o usuário atual com base no token JWT fornecido.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar o token JWT para extrair a carga útil
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        # Se o nome de usuário não estiver no token, levanta exceção
        if username is None:
            raise credentials_exception
        
        # Buscar o usuário no banco de dados
        user = db.query(Account).filter(Account.username == username).first()
        
        # Se o usuário não for encontrado, levanta exceção
        if user is None:
            raise credentials_exception
        
        return user
    
    except JWTError:
        raise credentials_exception
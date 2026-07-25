from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, Token, LoginRequest
from ..utils.security import get_password_hash, verify_password, create_access_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login-form-compatibility")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == user_id, User.deleted_at == None).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    if user_in.email:
        db_user = db.query(User).filter(User.email == user_in.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    if user_in.phone:
        db_user = db.query(User).filter(User.phone == user_in.phone).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Phone number already registered")

    # Create user
    hashed_pwd = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        phone=user_in.phone,
        role=user_in.role,
        preferred_language=user_in.preferred_language,
        status="active"
    )
    # Storing hashed password in auth_provider_id for local-only mock auth simplified integration
    user.auth_provider_id = f"local-hashed:{hashed_pwd}"
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Search by email or phone
    user = db.query(User).filter(
        (User.email == login_data.username) | (User.phone == login_data.username),
        User.deleted_at == None
    ).first()
    
    if not user or not user.auth_provider_id or not user.auth_provider_id.startswith("local-hashed:"):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    stored_val = user.auth_provider_id.replace("local-hashed:", "")
    hashed_pwd = stored_val.split(":", 1)[1] if ":" in stored_val else stored_val
    if not verify_password(login_data.password, hashed_pwd):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(subject=user.id, role=user.role)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

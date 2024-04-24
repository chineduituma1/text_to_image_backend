import database
import fastapi
import fastapi.security
import sqlalchemy
import models, schemas
import passlib.hash
from passlib.hash import bcrypt
import jwt

oauth2schema = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"

def create_database():
    return database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_email(email: str, db: sqlalchemy.orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def get_user_by_id(id: int, db: sqlalchemy.orm.Session):
    return db.query(models.User).filter(models.User.id == id)

async def create_user(user: schemas.UserCreate, db: sqlalchemy.orm.Session):

    existing_user = await get_user_by_email(user.email, db)
    if existing_user:
        raise ValueError("User already exists")
    
    user_obj = models.User(email=user.email, hashed_password=passlib.hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def delete_user(email: str, db: sqlalchemy.orm.Session):
    user = db.query(models.User).filter(models.User.email== email).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


async def authenticate_user(email: str, password: str, db: sqlalchemy.orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False
    
    if not user.verify_password(password):
        return False
    
    return user

async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)

    token = jwt.encode(user_obj.model_dump(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: sqlalchemy.orm.Session = fastapi.Depends(get_db), token: str = fastapi.Depends(oauth2schema)):
    try:
        payload =jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")
    
    return schemas.User.from_orm(user)


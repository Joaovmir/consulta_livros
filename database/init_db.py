# database/init_db.py
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.db import engine, SessionLocal
from models.user import Base, User

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db: Session = SessionLocal()

if not db.query(User).filter_by(username="admin").first():
    admin = User(
        username="admin",                              # DEFINIR EM AMBIENTE APÓS TESTES
        hashed_password=pwd_context.hash("admin123"),  # DEFINIR EM AMBIENTE APÓS TESTES
        is_admin=True
    )
    db.add(admin)
    db.commit()
    print("Admin criado com sucesso!")
else:
    print("Admin já existe.")

db.close()
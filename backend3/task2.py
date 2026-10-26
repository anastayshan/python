from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# База данных (SQLite файл)
DATABASE_URL = "sqlite:///masters.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# SQLAlchemy-модель Master и таблица masters
class Master(Base):
    __tablename__ = "masters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

# Pydantic-схема для сериализации
class MasterSchema(BaseModel):
    id: int
    name: str
    specialization: str

    class Config:
        orm_mode = True

app = FastAPI()

# Зависимость получить сессию БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Инициализация БД и начальные данные
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    # Засеивание данных, если таблица пуста
    db = SessionLocal()
    try:
        if db.query(Master).count() == 0:
            db.add_all([
                Master(id=1, name="Анна", specialization="Парикмахер"),
                Master(id=2, name="Мария", specialization="Визажист"),
            ])
            db.commit()
    finally:
        db.close()

# GET /masters — список всех мастеров (с опциональной фильтрацией)
@app.get("/masters", response_model=List[MasterSchema])
def read_masters(specialization: Optional[str] = None, db: Session = Depends(get_db)):
    if specialization:
        masters = db.query(Master).filter(Master.specialization == specialization).all()
    else:
        masters = db.query(Master).all()
    return masters

# GET /masters/{master_id} — один мастер по id
@app.get("/masters/{master_id}", response_model=MasterSchema)
def read_master(master_id: int, db: Session = Depends(get_db)):
    master = db.query(Master).filter(Master.id == master_id).first()
    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")
    return master
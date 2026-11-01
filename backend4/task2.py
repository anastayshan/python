# app.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, constr
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware

# Pydantic модель 

class ServiceCreate(BaseModel):
    categoryId: int
    title: constr(strip_whitespace=True, min_length=1, max_length=100)
    desc: constr(strip_whitespace=True, min_length=1, max_length=100)
    duration: int = Field(..., ge=30, le=180, description="Duration in minutes")
    price: float = Field(..., gt=0)

# ORM-модели

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    categoryId = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String(100), nullable=False)
    desc = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)  # в минутах
    price = Column(Float, nullable=False)

# База данных

DATABASE_URL = "sqlite:///./services.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Приложение FastAPI

app = FastAPI(title="Services API")

# Разрешаем CORS для простоты тестирования
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Стартап: создаём таблицы и предзагружаем категорию 3
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Если таблица пустая, добавим несколько категорий, включая id=3
        if db.query(Category).count() == 0:
            cats = [
                Category(id=1, name="Маникюр"),
                Category(id=2, name="Педикюр"),
                Category(id=3, name="Наращивание ресниц"),
            ]
            db.add_all(cats)
            db.commit()
    finally:
        db.close()

# POST /services
@app.post("/services", status_code=201)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    # Проверяем существование категории
    category = db.query(Category).filter(Category.id == service.categoryId).first()
    if category is None:
        raise HTTPException(status_code=400, detail="Category not found")

    new_service = Service(
        categoryId=service.categoryId,
        title=service.title,
        desc=service.desc,
        duration=service.duration,
        price=service.price
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return {
        "id": new_service.id,
        "categoryId": new_service.categoryId,
        "title": new_service.title,
        "desc": new_service.desc,
        "duration": new_service.duration,
        "price": new_service.price,
    }


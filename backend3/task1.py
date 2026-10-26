from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# 1. Настройка подключения к базе данных SQLite 
DATABASE_URL = "sqlite:///./salon.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем фабрику сессий для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Создаем базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# 3. Задание 1: Создание модели Master и таблицы masters
class Master(Base):
    __tablename__ = "masters"

    # Описываем поля таблицы согласно заданию
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=False)


# 4. Функция для инициализации базы данных и наполнения тестовыми данными
def init_db():
    # Создает таблицы в файле salon.db, если их еще нет
    Base.metadata.create_all(bind=engine)
    
    # Заполняем таблицу тестовыми данными из примера, если она пустая
    db = SessionLocal()
    try:
        if db.query(Master).count() == 0:
            master1 = Master(name="Анна", specialization="Парикмахер")
            master2 = Master(name="Мария", specialization="Визажист")
            
            db.add_all([master1, master2])
            db.commit()
            print("База данных успешно создана и заполнена тестовыми мастерами!")
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

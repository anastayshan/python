from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Схема ответа для Pydantic
class CategoryResponse(BaseModel):
    id: int
    name: str
    servicesCount: int

# Тестовые данные (имитация базы данных)
categories_db = [
    {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
    {"id": 2, "name": "Маникюр и педикюр", "servicesCount": 5},
    {"id": 3, "name": "Брови и ресницы", "servicesCount": 4},
    {"id": 4, "name": "Спа-процедуры", "servicesCount": 4}
]

# Задание 1. Список всех категорий
@app.get("/categories", response_model=list[CategoryResponse])
def get_categories():
    return categories_db

# Задание 2. Информация по конкретной категории
@app.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category_by_id(category_id: int):
    # Ищем категорию с совпадающим id
    for category in categories_db:
        if category["id"] == category_id:
            return category
            
    # Если категория не найдена, выбрасываем ошибку 404
    raise HTTPException(status_code=404, detail="Category not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("task1:app", host="127.0.0.1", port=8000, reload=True)

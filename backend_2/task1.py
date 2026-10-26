from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
# 1. Описываем схему ответа с помощью Pydantic
class CategoryResponse(BaseModel):
    id: int
    name: str
    servicesCount: int

# 2. Тестовые данные (имитация базы данных)
categories_db = [
    {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
    {"id": 2, "name": "Маникюр и педикюр", "servicesCount": 5},
    {"id": 3, "name": "Брови и ресницы", "servicesCount": 4},
    {"id": 4, "name": "Спа-процедуры", "servicesCount": 4}
]

# 3. Реализуем сам эндпоинт GET /categories
@app.get("/categories", response_model=list[CategoryResponse])
def get_categories():
    return categories_db
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("task1:app", host="127.0.0.1", port=8000, reload=True)

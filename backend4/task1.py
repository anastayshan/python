from pydantic import BaseModel, Field, ValidationError, constr

class ServiceCreate(BaseModel):
    categoryId: int
    title: constr(strip_whitespace=True, min_length=1, max_length=100)
    desc: constr(strip_whitespace=True, min_length=1, max_length=100)
    duration: int = Field(..., ge=30, le=180, description="Duration in minutes")
    price: float = Field(..., gt=0)

# Пример использования
if __name__ == "__main__":
    # корректный пример
    try:
        svc = ServiceCreate(categoryId=1, title="Маникюр", desc="Классический маникюр", duration=60, price=150.0)
        print(svc)
    except ValidationError as e:
        print("Validation error:", e)

    # пример с ошибкой (price <= 0)
    try:
        svc_bad = ServiceCreate(categoryId=1, title="Маникюр", desc="Описание", duration=60, price=0)
    except ValidationError as e:
        print("Validation error:", e)
class Master:
    def __init__(self, master_id: int, name: str):
        self.master_id = master_id
        self.name = name

class Service:
    def __init__(self, service_id: int, name: str):
        self.service_id = service_id
        self.name = name

# Примеры существующих мастеров и услуг
masters = {
    1: Master(1, "Иван"),
}
services = {
    1: Service(1, "Стрижка"),
}

def get_master(master_id: int):
    return masters.get(master_id)

def get_service(service_id: int):
    return services.get(service_id)

# ---------- запись клиента ----------
class Appoinment:
    def __init__(self, id: int, client_name: str, master_id: int, service_id: int, time: str):
        self.id = id
        self.client_name = client_name
        self.master_id = master_id
        self.service_id = service_id
        self.time = time

    def __repr__(self):
        return f"{self.client_name} {self.time}"

appointments = []

# Вспомогательная функция преобразования времени
def _parse_time(timestr: str):
    try:
        h, m = map(int, timestr.split(":"))
    except Exception:
        return None
    if not (0 <= h <= 23 and 0 <= m <= 59):
        return None
    return h * 60 + m  # минуты с полуночи

# Обновлённая функция создания записи
def create_appointment(client_name: str, master_id: int, service_id: int, time: str):
    master = get_master(master_id)
    service = get_service(service_id)

    if master is None or service is None:
        return None

    # Валидация заполненности полей
    if not client_name or not time:
        return None

    minutes = _parse_time(time)
    if minutes is None:
        return None

    # Часы работы: 08:00 (480 мин) до 20:00 (1200 мин) включительно
    if minutes < 8 * 60 or minutes > 20 * 60:
        return None

    appt = Appoinment(len(appointments) + 1, client_name, master.master_id, service.service_id, time)
    appointments.append(appt)
    return appt

# Пример использования 
first_appointment = create_appointment("Иванова А.А.", 1, 1, '10:00')
second_appointment = create_appointment("Петрова А.А.", 1, 1, '11:00')

print("Список записей:")
for appointment in appointments:
    print(appointment.client_name, appointment.time)

# Попытка создать запись с некорректным временем
no_correct_appointment = create_appointment("Сидорова А.А.", 1, 1, '00:00')
print(len(appointments))  # Ожидается 0, если запускать тест с чистого списка



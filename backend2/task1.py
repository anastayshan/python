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

appointments = []

def create_appointment(client_name: str, master_id: int, service_id: int, time: str):
    master = get_master(master_id)
    service = get_service(service_id)

    if master is None or service is None:
        return None

    # Валидация заполненности полей
    if not client_name or not time:
        return None

    appt = Appoinment(len(appointments) + 1, client_name, master.master_id, service.service_id, time)
    appointments.append(appt)
    return appt

# Пример использования
first_appointment = create_appointment("Иванова А.А.", 1, 1, '10:00')
second_appointment = create_appointment("Петрова А.А.", 1, 1, '11:00')

print("Список записей:")
for appt in appointments:
    print(appt.client_name, appt.time)

# Попытка создать неполную запись
no_correct_appointment = create_appointment("", 1, 1, '12:00')
print(len(appointments))  # должно быть 2
class Master:
    def __init__(self, master_id):
        self.master_id = master_id

class Service:
    def __init__(self, service_id):
        self.service_id = service_id

def get_master(master_id: int):
    return Master(master_id) if master_id else None

def get_service(service_id: int):
    return Service(service_id) if service_id else None

class Appointment:
    def __init__(self, appointment_id: int, client_name: str, master_id: int, service_id: int, time: str):
        self.id = appointment_id
        self.client_name = client_name
        self.master_id = master_id
        self.service_id = service_id
        self.time = time
appointments = []
def create_appointment(client_name: str, 
                       master_id: int, 
                       service_id: int, 
                       time: str,
) -> Appointment | None:
    master = get_master(master_id)
    service = get_service(service_id)
    if master is None or service is None:
        return None
    if not client_name.strip() or not time.strip():
        return None
    new_id = len(appointments) + 1
    
    appointment = Appointment(
        appointment_id=new_id,
        client_name=client_name,
        master_id=master.master_id,
        service_id=service.service_id,
        time=time
    )
    appointments.append(appointment)
    return appointment

# Проверка создание корректных записей
first_appointment = create_appointment("Иванова А.А.", 1, 1, '10:00')
second_appointment = create_appointment("Петрова А.А.", 1, 1, '11:00')

print("Список записей:")
for appointment in appointments:
    print(appointment.client_name, appointment.time)

print("-" * 30)


appointments = []

# Проверка создание записи с пустым именем клиента
no_correct_appointment = create_appointment("", 1, 1, '12:00')


print("Количество записей в списке:")
print(len(appointments))

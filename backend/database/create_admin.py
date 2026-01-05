from backend.database.database import SessionLocal
from backend.models.user import User

db = SessionLocal()

admin = User(
    username="admin",
    password="1234",
    email="admin@example.com",
    role="admin"
)

db.add(admin)
db.commit()

print("Usuário admin criado com sucesso!")

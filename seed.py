import os
import django
import bcrypt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Usuario


def seed():
    if Usuario.objects.count() > 0:
        print("Banco já populado. Pulando seed.")
        return

    senha_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode("utf-8")
    Usuario.objects.create(nome="Admin", email="admin@eventos.com", senha=senha_hash, role="admin")
    Usuario.objects.create(nome="Usuário Teste", email="user@eventos.com", senha=senha_hash, role="user")

    print("Seed concluído!")
    print("Admin: admin@eventos.com / senha: admin123")
    print("User:  user@eventos.com / senha: admin123")


if __name__ == "__main__":
    seed()
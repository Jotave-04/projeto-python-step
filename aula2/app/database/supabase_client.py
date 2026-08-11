import os
from dotenv import load_dotenv
from supabase import create_client, Client # Importe o criador de cliente

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Em vez de um dicionário {}, crie o cliente oficial
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
import os
from datetime import datetime
from crewai import Crew, Process
from agents import job_scraper, cv_analyst, career_strategist
from tasks import scrape_task, analyze_task, strategize_task

# ============================================================
# CONFIGURAÇÃO
# ============================================================
# Cole aqui a URL da vaga que quer analisar
URL_VAGA = input("Cole a URL da vaga: ").strip()

if not URL_VAGA:
    print("❌ Nenhuma URL fornecida. Usando URL de exemplo...")
    URL_VAGA = "https://exemplo.com/vaga-python"  # substitua por uma real

# ============================================================
# MONTAR A CREW
# ============================================================
crew = Crew(
    agents=[job_scraper, cv_analyst, career_strategist],
    tasks=[scrape_task, analyze_task, strategize_task],
    process=Process.sequential,
    verbose=True,
)

# ============================================================
# EXECUTAR
# ============================================================
print("\n" + "=" * 60)
print("  🚀 INICIANDO ANÁLISE DA VAGA")
print("=" * 60)
print(f"  URL: {URL_VAGA}")
print(f"  Modelo: llama-3.3-70b (Groq)")
print("=" * 60 + "\n")

resultado = crew.kickoff(inputs={"url_vaga": URL_VAGA})

# ============================================================
# SALVAR RESULTADOS
# ============================================================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Salvar resultado completo
os.makedirs("output", exist_ok=True)
with open(f"output/resultado_completo_{timestamp}.md", "w", encoding="utf-8") as f:
    f.write(f"# Análise de Vaga — {timestamp}\n\n")
    f.write(f"**URL:** {URL_VAGA}\n\n")
    f.write("---\n\n")
    f.write(str(resultado))

print("\n" + "=" * 60)
print("  ✅ ANÁLISE CONCLUÍDA!")
print(f"  Relatório salvo em: output/resultado_completo_{timestamp}.md")
print("=" * 60)
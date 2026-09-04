import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import ScrapeWebsiteTool, FileReadTool

load_dotenv()

llm = LLM(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    provider="openai",
)

# ============================================================
# FERRAMENTAS
# ============================================================
scrape_tool = ScrapeWebsiteTool()
leitor_cv = FileReadTool(file_path="meu_cv.txt")

# ============================================================
# AGENTES
# ============================================================
job_scraper = Agent(
    role="Tech Recruiter Sênior",
    goal="Extrair e estruturar todas as informações relevantes da vaga a partir da URL fornecida",
    backstory=(
        "Você é um recrutador tech com 15 anos de experiência em grandes empresas "
        "de tecnologia. Sua especialidade é analisar descrições de vagas e extrair "
        "informações de forma estruturada. Você identifica padrões em requisitos, "
        "diferencia must-have de nice-to-have, e entende profundamente stacks "
        "tecnológicas modernas. Você é detalhista e nunca deixa passar um requisito "
        "importante, por mais sutil que esteja na descrição."
    ),
    tools=[scrape_tool],
    llm=llm,
    verbose=True,
)

cv_analyst = Agent(
    role="Analista de Currículos e Match de Skills",
    goal="Comparar o currículo do candidato com os requisitos da vaga e gerar uma matriz de compatibilidade",
    backstory=(
        "Você é um analista de RH especializado em matching de currículos com vagas. "
        "Com 10 anos de experiência, você é capaz de identificar rapidamente gaps de "
        "habilidades, pontos fortes e fracos de um candidato em relação a uma vaga. "
        "Você é justo e transparente: aponta tanto alinhamentos quanto lacunas. "
        "Seu relatório é sempre estruturado em: skills que o candidato TEM, skills "
        "que o candidato TEM PARCIALMENTE, e skills que o candidato NÃO TEM."
    ),
    tools=[leitor_cv],
    llm=llm,
    verbose=True,
)

career_strategist = Agent(
    role="Coach de Carreira e Estrategista de Desenvolvimento Profissional",
    goal="Criar uma cover letter personalizada e um plano de estudos de 30 dias baseado nos gaps identificados",
    backstory=(
        "Você é um coach de carreira renomado, com centenas de profissionais "
        "recolocados em empresas como Google, Nubank, iFood e outras. Sua especialidade "
        "é criar cartas de apresentação que destacam os pontos fortes do candidato "
        "enquanto abordam gaps de forma estratégica. Você também é excelente em criar "
        "roadmaps de aprendizado realistas, priorizando o que traz mais retorno rápido. "
        "Seu tom é motivador mas realista, profissional mas pessoal."
    ),
    llm=llm,
    verbose=True,
)
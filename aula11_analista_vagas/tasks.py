from crewai import Task
from agents import job_scraper, cv_analyst, career_strategist

# ============================================================
# TAREFAS
# ============================================================
scrape_task = Task(
    description=(
        "1. Acesse a URL da vaga: {url_vaga}\n"
        "2. Extraia TODO o conteúdo relevante da descrição da vaga.\n"
        "3. Organize as informações no seguinte formato estruturado:\n"
        "   - Título da vaga e nome da empresa\n"
        "   - Stack tecnológica (linguagens, frameworks, ferramentas)\n"
        "   - Requisitos obrigatórios (must-have)\n"
        "   - Requisitos diferenciais (nice-to-have)\n"
        "   - Nível de senioridade exigido\n"
        "   - Tipo de contrato (CLT, PJ, remoto, híbrido, presencial)\n"
        "   - Benefícios oferecidos\n"
        "   - Faixa salarial (se disponível)\n"
        "4. Se a página não for uma vaga válida ou não puder ser acessada, "
        "informe claramente o problema."
    ),
    expected_output=(
        "Um relatório detalhado em markdown com todas as informações da vaga, "
        "organizado por seções conforme o formato solicitado."
    ),
    agent=job_scraper,
)

analyze_task = Task(
    description=(
        "1. Leia o arquivo 'meu_cv.txt' para conhecer o perfil do candidato.\n"
        "2. Com base na análise da vaga (output da tarefa anterior), compare "
        "sistematicamente cada requisito com o currículo do candidato.\n"
        "3. Classifique cada skill em uma das três categorias:\n"
        "   ✅ TEM — o candidato possui essa skill comprovadamente\n"
        "   ⚠️ TEM PARCIALMENTE — possui conhecimento básico ou relacionado\n"
        "   ❌ NÃO TEM — não há evidência dessa skill no currículo\n"
        "4. Calcule uma porcentagem de match geral.\n"
        "5. Destaque os 3 principais pontos fortes do candidato para esta vaga.\n"
        "6. Destaque os 3 principais gaps que precisam ser endereçados."
    ),
    expected_output=(
        "Um relatório de match em markdown contendo:\n"
        "1. Tabela de compatibilidade skill por skill\n"
        "2. Porcentagem de match geral\n"
        "3. Top 3 pontos fortes\n"
        "4. Top 3 gaps críticos"
    ),
    agent=cv_analyst,
    context=[scrape_task],   # recebe o output da tarefa anterior
)

strategize_task = Task(
    description=(
        "Com base nos outputs anteriores, produza DOIS documentos separados:\n\n"
        "DOCUMENTO 1 — COVER LETTER:\n"
        "- Carta de apresentação personalizada para esta vaga específica\n"
        "- Tom profissional mas autêntico\n"
        "- Destaque 3 experiências/habilidades do candidato alinhadas com a vaga\n"
        "- Mencione 1 gap de forma estratégica (como motivação para aprender)\n"
        "- Inclua parágrafo de abertura, 2-3 parágrafos de corpo e fechamento\n\n"
        "DOCUMENTO 2 — PLANO DE ESTUDOS DE 30 DIAS:\n"
        "- Foco nos gaps críticos identificados\n"
        "- Dividido em 4 semanas com metas realistas\n"
        "- Cada semana com tópicos específicos, recursos sugeridos e mini-projeto\n"
        "- Priorize o que tem maior impacto para esta vaga\n\n"
        "Separe os dois documentos claramente com títulos em markdown."
    ),
    expected_output=(
        "Dois documentos em markdown:\n"
        "1. Cover letter completa e pronta para enviar\n"
        "2. Plano de estudos de 30 dias estruturado por semanas"
    ),
    agent=career_strategist,
    context=[scrape_task, analyze_task],
)
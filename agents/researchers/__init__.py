from agents.researchers.news_researcher import news_researcher
from agents.researchers.research_paper_researcher import research_paper_researcher
from agents.researchers.official_docs_researcher import official_docs_researcher
from agents.researchers.github_researcher import github_researcher
from agents.researchers.blog_researcher import blog_researcher
from agents.researchers.industry_report_researcher import industry_report_researcher
from agents.researchers.government_report_researcher import government_report_researcher
from agents.researchers.memory_researcher import (
    memory_researcher,
)
RESEARCHER_MAP = {
    "news": news_researcher,
    "research_papers": research_paper_researcher,
    "official_docs": official_docs_researcher,
    "github": github_researcher,
    "blogs": blog_researcher,
    "industry_reports": industry_report_researcher,
    "government_reports": government_report_researcher,
    "memory": memory_researcher,
}

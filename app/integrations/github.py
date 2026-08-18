from app.integrations.github import Github
from app.core.config import settings

class GitHubService:
    """
    Сервіс для автоматизації роботи з GitHub API.
    """
    def __init__(self):
        # Авторизація через Personal Access Token
        self.github = Github(settings.GITHUB_TOKEN)
        self.repo = self.github.get_repo(settings.GITHUB_REPO_NAME)

    async def create_issue(self, title: str, body: str, assignee: str = None):
        """
        Автоматичне створення завдання (Issue) у репозиторії.
        """
        try:
            issue = self.repo.create_issue(
                title=title,
                body=body,
                assignee=assignee
            )
            return issue.html_url
        except Exception as e:
            # Тут логуємо помилку
            return None

    async def get_pull_request_status(self, pr_number: int):
        """
        Перевірка статусу Pull Request (чи пройшов він перевірку).
        """
        pr = self.repo.get_pull(pr_number)
        return {
            "title": pr.title,
            "status": pr.state, # open або closed
            "merged": pr.merged
        }
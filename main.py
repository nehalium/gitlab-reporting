from gitlabclient import GitlabClient
from projects import Projects


def get_client():
    return GitlabClient()


def main():
    client = get_client()

    projects = Projects(client)
    projects.load()
    projects.sort_by_last_activity_at()
    projects.print_results()


if __name__ == '__main__':
    main()

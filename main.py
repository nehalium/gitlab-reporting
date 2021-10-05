from gitlabclient import GitlabClient
from projects import Projects


def get_client():
    return GitlabClient()


def main():
    client = get_client()

    projects = Projects(client)
    print("Loading projects...")
    projects.load()

    print("Printing projects...")
    projects.sort_by_last_activity_at()
    projects.print_results()

    print("Cloning projects...")
    projects.sort_by_namespace()
    projects.clone()


if __name__ == '__main__':
    main()

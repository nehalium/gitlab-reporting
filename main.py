from gitlabclient import GitlabClient
from projects import Projects


def get_client():
    return GitlabClient()


def main():
    client = get_client()

    projects = Projects(client)
    print("Loading projects...")
    projects.load()
    projects.sort_by_namespace()

    print("Printing projects...")
    projects.print_results()

    print("Cloning projects...")
    projects.clone()


if __name__ == '__main__':
    main()

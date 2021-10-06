import configparser
import os
import git

config = configparser.ConfigParser()
config.read("config.ini")


class Projects:

    def __init__(self, client):
        self.client = client
        self.items = []
        self.whitelist = self.get_whitelist()

    def clone(self):
        index = 1
        print("Cloning {} projects...".format(str(len(self.items))))
        for item in self.items:
            project_path = self.get_project_path(item)
            if not self.directory_is_empty(project_path):
                print("{index}. Already exists! {project_path}".format(index=index, project_path=project_path))
            else:
                print("{index}. Cloning {project_path}...".format(index=index, project_path=project_path), end="")
                with git.Git().custom_environment(git_ssh_command=self.get_git_ssh_command()):
                    git.Repo.clone_from(item["ssh_url_to_repo"], project_path)
                print("done.")
            index += 1

    def get_project_path(self, item):
        return self.ensure_path(os.path.join(
            config.get("General", "cloneDir"),
            item["namespace"],
            item["name"]
        ))

    def load(self):
        page = 1
        per_page = 50
        while True:
            response = self.client.get("projects", page, per_page)
            result = response.json()

            if len(result) == 0:
                break

            if config.getboolean("General", "refreshFixtures"):
                self.write_result(result, page)
            if config.getboolean("General", "debug"):
                print("Page: {page_num}\t\t# of items: {total}".format(
                    page_num=str(page),
                    total=str(len(result))
                ))

            for item in result:
                if self.is_in_whitelist(item) and not item["archived"]:
                    self.items.append(self.build_tuple(item))

            page = page + 1

    def is_in_whitelist(self, item):
        return item["namespace"]["name"] in self.whitelist

    def sort_by_name(self):
        self.items = sorted(self.items, key=lambda projects: projects["name"], reverse=False)

    def sort_by_namespace(self):
        self.items = sorted(self.items, key=lambda projects: projects["name_with_namespace"], reverse=False)

    def sort_by_last_activity_at(self):
        self.items = sorted(self.items, key=lambda projects: projects["last_activity_at"], reverse=True)

    def sort_by_created_at(self):
        self.items = sorted(self.items, key=lambda projects: projects["created_at"], reverse=True)

    def print_results(self):
        for item in self.items:
            print(
                item["namespace"] + "\t" +
                item["name"] + "\t" +
                item["last_activity_at"] + "\t" +
                item["web_url"] + "\t" +
                item["ssh_url_to_repo"]
            )

    @staticmethod
    def get_git_ssh_command():
        return "ssh -i {}".format(config.get("General", "sshKeyPath"))

    @staticmethod
    def get_whitelist():
        return config.get("General", "whitelist").split(",")

    @staticmethod
    def build_tuple(item):
        return {
            "id": item["id"],
            "name": item["name"],
            "namespace": item["namespace"]["name"],
            "name_with_namespace": item["name_with_namespace"],
            "description": item["description"],
            "last_activity_at": item["last_activity_at"],
            "created_at": item["created_at"],
            "web_url": item["web_url"],
            "ssh_url_to_repo": item["ssh_url_to_repo"],
            "api_ref": item["_links"]["self"]
        }

    @staticmethod
    def directory_is_empty(path):
        return len(os.listdir(path)) == 0

    @staticmethod
    def ensure_path(path):
        path = path.replace(" ", "_")
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def write_result(result, page):
        path = "test/fixtures"
        if not os.path.exists(path):
            os.makedirs(path)
        result_file = open(path + "/projects-{}.json".format(str(page)), "w")
        result_file.write(str(result))
        result_file.close()

    @staticmethod
    def get_file_contents(file_name):
        requested_file = open(file_name, "r")
        return requested_file.read()

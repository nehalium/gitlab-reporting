import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")


class Projects:

    def __init__(self, client):
        self.client = client
        self.items = []

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
                print("Page: " + str(page) + "\t\t" + "# of items: " + str(len(result)))

            for item in result:
                self.items.append(self.build_tuple(item))

            page = page + 1

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
    def write_result(result, page):
        path = "test/fixtures"
        if not os.path.exists(path):
            os.makedirs(path)
        result_file = open(path + "/projects-" + str(page) + ".json", "w")
        result_file.write(str(result))
        result_file.close()

    @staticmethod
    def get_file_contents(file_name):
        requested_file = open(file_name, "r")
        return requested_file.read()

import configparser
import requests

config = configparser.ConfigParser()
config.read("config.ini")


class GitlabClient:

    def __init__(self):
        pass

    def get(self, resource, page, per_page):
        query = self.format_querystring({
            "page": page,
            "per_page": per_page
        })
        return requests.get(
            config.get("GitlabAPI", "url") + "/" + resource + "/" + query,
            headers={
                "Accept": "application/json",
                "Authorization": "Bearer " + config.get("GitlabAPI", "token")
            }
        )

    @staticmethod
    def format_querystring(params):
        if len(params) == 0:
            return ""
        query = "?"
        for key, value in params.items():
            query += "&" + key + "=" + str(value)
        return query

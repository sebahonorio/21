import requests

class AutoExecutor:
    @staticmethod
    def post_to_forum(message, forum_url="http://exemplo.com/api/post"):
        try:
            response = requests.post(forum_url, json={"message": message})
            return response.status_code == 200
        except Exception as e:
            print(f"Falha ao postar: {e}")
            return False
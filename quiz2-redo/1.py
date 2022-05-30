from typing import List
import requests


def get_emails(username: str) -> List[str]:
    user_id = requests.get(f"https://jsonplaceholder.typicode.com/users?username={username}").json()[0]['id']
    posts = requests.get(f"https://jsonplaceholder.typicode.com/posts", params={'userId': user_id}).json()
    comments = requests.get(f"https://jsonplaceholder.typicode.com/comments", params={'postId': [post['id'] for post in posts]}).json()
    return [comment['email'] for comment in comments]


def main():
    print(get_emails('Antonette'))


if __name__ == "__main__":
    main()

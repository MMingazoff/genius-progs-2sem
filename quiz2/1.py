from typing import List
import requests


def get_user_id(username: str) -> int:
    return requests.get(f"https://jsonplaceholder.typicode.com/users?username={username}").json()[0]['id']


def get_emails(username: str) -> List[str]:
    user_id = get_user_id(username)
    emails = []
    posts = requests.get(f"https://jsonplaceholder.typicode.com/posts", params={'userId': user_id}).json()
    for post in posts:
        comments = requests.get(f"https://jsonplaceholder.typicode.com/comments", params={'postId': post['id']}).json()
        for comment in comments:
            emails.append(comment['email'])
    return emails


def main():
    print(get_emails('Antonette'))


if __name__ == "__main__":
    main()

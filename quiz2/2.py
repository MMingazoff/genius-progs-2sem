topics = []  # {topic_name: name, posts: [{post_id: id, post_text: text}]}
users = []  # {user_id: id, subbed_topics: set(topic_names)}


def notify_subbed_users(topic_name: str) -> bool:
    for user in users:
        if topic_name in user['subbed_topics']:
            print()
        return False


def create_topic(topic_name: str):
    topics.append({'topic_name': topic_name, 'posts': []})


def subscribe(user_id: int, topic: str):
    for user in users:
        if user['user_id'] == user_id:
            user['subbed_topics'].add(topic)
            return


def post_feed(topic_name: str, post_id: int):
    for topic in topics:
        if topic['topic_name'] == topic_name:
            topic['posts'].append({'post_id': post_id, 'post_text': ''})
            for user in users:
                if topic_name in user['subbed_topics']:
                    print(f'Пользователь {user["user_id"]} получил новость {post_id}')


def main():
    users.append({'user_id': 1, 'subbed_topics': set()})
    users.append({'user_id': 2, 'subbed_topics': set()})
    users.append({'user_id': 3, 'subbed_topics': set()})
    create_topic('programming')
    subscribe(1, 'programming')
    subscribe(2, 'programming')
    post_feed('programming', 0)


if __name__ == '__main__':
    main()

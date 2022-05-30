class User:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def register(self):
        Event.register_user(self)

    def delete(self, admin):
        Event.delete_user(self, admin)


class Event:
    @staticmethod
    def register_user(user: User):
        print(f'Почта юзера(id={user.user_id}): вы зарегистрировались')

    @staticmethod
    def delete_user(user: User, admin: User):
        print(f'Почта у юзера(id={user.user_id}): вы удалили аккаунт')
        print(f'TG админа(id={admin.user_id}): юзер {user.user_id} удалил аккаунт')


if __name__ == '__main__':
    main_admin = User(-1)
    user1 = User(1)
    user2 = User(2)
    user1.register()
    user2.register()
    user1.delete(main_admin)


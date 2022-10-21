Investor = 'Investor'
Investor2 = 'Investor2'
NAME = 'name'
FOLLOWERS = 'Followers'
FOLLOWING = 'Following'
REQUIRED_FIELDS = [NAME, FOLLOWERS, FOLLOWING]
user_types = {Investor: {NAME: 'user1', FOLLOWERS: 0, FOLLOWING: 0},
              Investor2: {NAME: 'user2', FOLLOWERS: 0, FOLLOWING: 0}}


def user_exists(name):
    return name in user_types


def get_users():
    return list(user_types.keys())


def get_user_type_details(type):
    return user_types.get(user_types, None)


def add_user(name, details):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        # print(details.keys())
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    user_types[name] = details


def del_user(name):
    del user_types[name]


def main():
    return


if __name__ == '__main__':
    main()

Investor = 'Investor'
Investor2 = 'Investor2'
Investor3 = 'Investor3'
SampleUser = 'SampleUser'
NAME = 'name'
FOLLOWERS = 'Followers'
FOLLOWING = 'Following'
EMAIL = 'email'
PASSWORD = 'password'
REQUIRED_FIELDS = [NAME, PASSWORD, EMAIL, FOLLOWERS, FOLLOWING]
user_types = {Investor: {NAME: 'user1', PASSWORD: '****',
              EMAIL: 'user@gmail.com', FOLLOWERS: [Investor2], FOLLOWING: []},
              Investor2: {NAME: 'user2', PASSWORD: '****',
              EMAIL: 'user2@gmail.com', FOLLOWERS: [], FOLLOWING: [Investor]},
              Investor3: {NAME: 'user3', PASSWORD: '****',
              EMAIL: 'user3@gmail.com', FOLLOWERS: [], FOLLOWING: []},
              SampleUser: {NAME: 'sample', PASSWORD: '****',
              EMAIL: 'sampleuser@gmail.com', FOLLOWERS: [], FOLLOWING: []}}


def user_exists(name):
    return name in user_types


def get_users():
    return list(user_types.keys())


def get_user_type_details(type):
    return list(user_types.get(type, None))


def get_user_email(username):
    if username not in user_types:
        raise ValueError(f'User {username=} does not exist')

    return user_types[username][EMAIL]


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


def follower_exists(userName, followName):
    return ((userName in user_types[followName][FOLLOWERS])
            and (followName in user_types[userName][FOLLOWING]))


def add_follower(userName, followName):
    user_types[followName][FOLLOWERS].append(userName)
    user_types[userName][FOLLOWING].append(followName)


def remove_follower(userName, followName):
    user_types[followName][FOLLOWERS].remove(userName)
    user_types[userName][FOLLOWING].remove(followName)


def update_email(userName, newEmail):
    user_types[userName][EMAIL] = newEmail


def main():
    users = get_users()
    print(f'{users=}')
    print(f'{get_user_type_details(Investor)=}')


if __name__ == '__main__':
    main()

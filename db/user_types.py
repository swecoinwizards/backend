import db.db_connect as dbc

Investor = 'Investor'
Investor2 = 'Investor2'
Investor3 = 'Investor3'
SampleUser = 'SampleUser'
TEST_USER_NAME = "RANDOMUSER"
TEST_USER_NAME2 = "RANDOMUSER2"
NAME = 'name'
FOLLOWERS = 'Followers'
FOLLOWING = 'Following'
EMAIL = 'email'
PASSWORD = 'password'
COINS = 'coins'
USERS_COLLECT = 'users'
USER_KEY = 'name'
REQUIRED_FIELDS = [NAME, PASSWORD, EMAIL]  # FOLLOWERS, FOLLOWING, COINS]
POSTS = 'posts'

user_types = {Investor: {NAME: 'user1', PASSWORD: '****',
              EMAIL: 'user@gmail.com', FOLLOWERS: [Investor2],
              FOLLOWING: [], COINS: [], POSTS: []},
              Investor2: {NAME: 'user2', PASSWORD: '****',
              EMAIL: 'user2@gmail.com', FOLLOWERS: [],
              FOLLOWING: [Investor], COINS: [], POSTS: []},
              Investor3: {NAME: 'user3', PASSWORD: '****',
              EMAIL: 'user3@gmail.com', FOLLOWERS: [],
              FOLLOWING: [], COINS: [], POSTS: []},
              SampleUser: {NAME: 'sample', PASSWORD: '****',
              EMAIL: 'sampleuser@gmail.com', FOLLOWERS: [],
              FOLLOWING: [], COINS: [], POSTS: []}}


def user_exists(name):
    dbc.connect_db()
    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": name})
    # print("exists: ", name in user_types and temp is not None)
    # return name in user_types and temp is not None
    return temp is not None


def get_users():
    dbc.connect_db()
    return dbc.fetch_all(USERS_COLLECT)


def get_posts(userName):
    dbc.connect_db()
    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    return temp[POSTS]


def get_users_dict():
    '''
    FOR MENU
    '''
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USER_KEY, USERS_COLLECT)


def get_user(username):
    if not user_exists(username):
        raise ValueError(f'User {username=} does not exist')
    dbc.connect_db()
    print("USER DOES EXIST", dbc.fetch_one(USERS_COLLECT,
                                           {"name": username}))
    return dbc.fetch_one(USERS_COLLECT,
                         {"name": username})


def get_user_email(username):
    if not user_exists(username):
        raise ValueError(f'User {username=} does not exist')
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": username})
    return user[EMAIL]


def get_user_password(username):
    if not user_exists(username):
        raise ValueError(f'User {username=} does not exist')
    dbc.connect_db()
    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": username})
    return temp[PASSWORD]


def add_user(name, details):
    # doc = details
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    if user_exists(name):
        raise TypeError(f'User {type(details)=} exists')
    for field in REQUIRED_FIELDS:
        # print(details.keys())
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    if not isinstance(details[EMAIL], str):
        raise TypeError(f'Wrong type for email: {type(name)=}')
    if '@' not in details[EMAIL]:
        raise ValueError('Invalid Email')
    # new users will start with no coins, followers/following
    if len(details) == 3:
        details[FOLLOWERS] = []
        details[FOLLOWING] = []
        details[COINS] = []
        details[POSTS] = []
    user_types[name] = details
    dbc.connect_db()
    # doc[USER_KEY] = name
    dbc.insert_one(USERS_COLLECT, user_types[name])
    return True


def del_user(name):
    dbc.connect_db()
    # print(dbc.fetch_one(USERS_COLLECT, {"name": name}), name)
    if not user_exists(name):
        raise TypeError(f'User: {type(name)=} does not exist in db.')
    dbc.remove_one(USERS_COLLECT, {"name": name})
    del user_types[name]


def follower_exists(userName, followName):
    dbc.connect_db()
    # print(user_types[userName])
    user1 = dbc.fetch_one(USERS_COLLECT,
                          {"name": userName})
    user2 = dbc.fetch_one(USERS_COLLECT,
                          {"name": followName})
    print(user1[FOLLOWERS], user1[FOLLOWING])
    print(user2[FOLLOWERS], user2[FOLLOWING])
    isFollower = userName in user1[FOLLOWERS]
    isFollowing = followName in user2[FOLLOWING]
    return isFollowing and isFollower


def add_follower(userName, followName):
    dbc.connect_db()
    if userName == followName:
        raise ValueError("Use two different users")
    if follower_exists(userName, followName):
        raise ValueError("Follower exists")
    user1 = dbc.fetch_one(USERS_COLLECT,
                          {"name": userName})
    user2 = dbc.fetch_one(USERS_COLLECT,
                          {"name": followName})
    user1[FOLLOWERS].append(userName)
    user2[FOLLOWING].append(followName)
    # print(user1)
    print(user2)
    del_user(userName)
    add_user(userName, user1)
    del_user(followName)
    add_user(followName, user2)
    return {userName: user_types[userName], followName: user_types[followName]}


def remove_follower(userName, followName):
    if not follower_exists(userName, followName):
        raise ValueError("Follower does not exists")
    user1 = dbc.fetch_one(USERS_COLLECT,
                          {"name": userName})
    user2 = dbc.fetch_one(USERS_COLLECT,
                          {"name": followName})
    user1[FOLLOWERS].remove(userName)
    user2[FOLLOWING].remove(followName)
    del_user(userName)
    add_user(userName, user1)
    del_user(followName)
    add_user(followName, user2)
    return {userName: user_types[userName], followName: user_types[followName]}


def update_email(userName, newEmail):
    user = get_user(userName)
    del_user(userName)
    currentEmail = user[EMAIL]
    if currentEmail == newEmail:
        raise ValueError("New email must be different from the previous!")
    user[EMAIL] = newEmail
    print(user)
    add_user(user["name"], user)
    # user_types[userName][EMAIL] = newEmail
    return {userName: user_types[userName]}


def get_password(userName):
    return user_types[userName][PASSWORD]


def update_password(userName, newPassword):
    currentPassword = user_types[userName][PASSWORD]

    if currentPassword == newPassword:
        raise ValueError("New password must be different from the previous!")

    user_types[userName][PASSWORD] = newPassword
    return {userName: user_types[userName]}


def user_coin_exists(userName, coin):
    return coin in user_types[userName][COINS]


def add_coin(userName, coin):
    if not user_exists(userName):
        raise ValueError("User does not exists")
    if coin in user_types[userName][COINS]:
        raise ValueError("Already Following Coin")
    user_types[userName][COINS].append(coin)
    return {userName: user_types[userName]}


def remove_coin(userName, coin):
    if not user_exists(userName):
        raise ValueError("User does not exists")
    if coin not in user_types[userName][COINS]:
        raise ValueError("Not Following Coin")
    user_types[userName][COINS].remove(coin)
    return {userName: user_types[userName]}


def follower_count(userName, followName):
    print(user_types[userName])
    isFollowers = followName in user_types[userName][FOLLOWERS]
    return (isFollowers.count())


def following_count(userName, followName):
    print(user_types[userName])
    isFollowing = followName in user_types[userName][FOLLOWING]
    return (isFollowing.count())


def get_followers(userName):
    if user_exists(userName):
        return user_types[userName][FOLLOWERS]
    raise Exception("User does not exist")


def user_coin_valuation(userName):
    if not user_exists(userName):
        raise ValueError("User does not exist")

    value = 0
    for coin in user_types[userName][COINS]:
        print(coin)

    return value


def access_profile_posts(userName, postNumber):
    return user_types[userName][POSTS][postNumber-1]


def profile_add_post(userName, content):
    if not user_exists(userName):
        raise ValueError("User does not exists")
    if content == "":
        raise ValueError("There is no content in the post")
    user_types[userName][POSTS].append(content)
    return {userName: user_types[userName]}


def profile_delete_post(userName, postNumber):
    if not user_exists(userName):
        raise ValueError("User does not exists")
    if postNumber < 0 or postNumber >= len(user_types[userName][POSTS]):
        raise ValueError("Post not found")
    del user_types[userName][POSTS][postNumber]
    return True


def user_login(userName, password):
    if get_user_password(userName) == password:
        return get_user(userName)
    raise Exception("Wrong Password")


def main():
    users = get_users()
    print(f'{users=}')
    print(f'{get_user(Investor)=}')


if __name__ == '__main__':
    main()

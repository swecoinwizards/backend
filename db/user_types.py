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

# user_types = {Investor: {NAME: 'user1', PASSWORD: '****',
#               EMAIL: 'user@gmail.com', FOLLOWERS: [Investor2],
#               FOLLOWING: [], COINS: [], POSTS: []},
#               Investor2: {NAME: 'user2', PASSWORD: '****',
#               EMAIL: 'user2@gmail.com', FOLLOWERS: [],
#               FOLLOWING: [Investor], COINS: [], POSTS: []},
#               Investor3: {NAME: 'user3', PASSWORD: '****',
#               EMAIL: 'user3@gmail.com', FOLLOWERS: [],
#               FOLLOWING: [], COINS: [], POSTS: []},
#               SampleUser: {NAME: 'sample', PASSWORD: '****',
#               EMAIL: 'sampleuser@gmail.com', FOLLOWERS: [],
#               FOLLOWING: [], COINS: [], POSTS: []}}


def user_cleanUp(user):
    if '_id' in user:
        del user['_id']
    return user


def user_exists(name):
    dbc.connect_db()
    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": name})
    return temp is not None


def change_username(username, newUsername):
    dbc.connect_db()
    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": newUsername})
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": username})
    if temp is not None:
        raise ValueError(f'Username {newUsername=} already does exist')
    newFollowers = get_followers(username)
    newFollowings = get_followings(username)
    newCoins = get_coins(username)
    newPosts = get_posts(username)
    # newDetails = [newFollowers, newFollowings, newCoins, newPosts]
    newDetails = {NAME: newUsername, PASSWORD: user["password"],
                  EMAIL: user["email"], FOLLOWERS: newFollowers,
                  FOLLOWING: newFollowings, COINS: newCoins, POSTS: newPosts}
    del_user(username)
    add_user(newUsername, newDetails)
    return {newUsername: user_cleanUp(newDetails)}


def get_users():
    dbc.connect_db()
    return dbc.fetch_all(USERS_COLLECT)


def get_posts(userName):
    dbc.connect_db()
    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    print(temp)
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
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    if user_exists(name):
        raise ValueError(f'User {name} already exists!')
    for field in REQUIRED_FIELDS:
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
    dbc.connect_db()
    # including user_cleanUp as extra safety
    dbc.insert_one(USERS_COLLECT, user_cleanUp(details))
    return {name: user_cleanUp(details)}


def del_user(name):
    dbc.connect_db()
    if not user_exists(name):
        raise TypeError(f'User: {name} does not exist in db.')
    dbc.remove_one(USERS_COLLECT, {"name": name})
    return True
    # del user_types[name]


def follower_exists(userName, followName):
    dbc.connect_db()

    user1 = dbc.fetch_one(USERS_COLLECT,
                          {"name": userName})
    user2 = dbc.fetch_one(USERS_COLLECT,
                          {"name": followName})

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

    del_user(userName)
    add_user(userName, user1)
    del_user(followName)
    add_user(followName, user2)
    # return {userName: user_types[userName],
    # followName: user_types[followName]}
    return {userName: user_cleanUp(user1), followName: user_cleanUp(user2)}


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
    # return {userName: user_types[userName],
    # followName: user_types[followName]}
    return {userName: user_cleanUp(user1), followName: user_cleanUp(user2)}


def update_email(userName, newEmail):
    user = get_user(userName)
    del_user(userName)
    currentEmail = user[EMAIL]
    if currentEmail == newEmail:
        raise ValueError("New email must be different from the previous!")
    user[EMAIL] = newEmail

    add_user(user["name"], user)
    # return {userName: user_types[userName]}
    return {userName: user_cleanUp(user)}


def get_password(userName):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    return user[PASSWORD]


def update_password(userName, newPassword):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    currentPassword = user[PASSWORD]
    if currentPassword == newPassword:
        raise ValueError("New password must be different from the previous!")
    del_user(userName)
    # dbc.remove_one(USERS_COLLECT, PASSWORD)
    # userName.remove(userName)
    user[PASSWORD] = newPassword
    add_user(user["name"], user)
    # return {userName: user_types[userName]}
    return {userName: user_cleanUp(user)}


def user_coin_exists(userName, coin):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    return coin in user[COINS]


def add_coin(userName, coin):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if not user_exists(userName):
        raise ValueError("User does not exists")
    if coin in user[COINS]:
        raise ValueError("Already Following Coin")
    # check if coin is valid
    print("user!",user)
    user[COINS].append(coin)
    # is there a better way to modify obj in db?
    del_user(userName)
    add_user(user["name"], user)
    return {userName: user_cleanUp(user)}


def remove_coin(userName, coin):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    print("here - user:", user[COINS][0])
    if not user_exists(userName):
        raise ValueError("User does not exists")
    if coin not in user[COINS]:
        raise ValueError("Not Following Coin!")
    user[COINS].remove(coin)
    del_user(userName)
    add_user(user["name"], user)
    # return {userName: user_types[userName]}
    return {userName: user_cleanUp(user)}


def follower_count(userName, followName):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    isFollowers = followName in user[FOLLOWERS]
    return (isFollowers.count())


def following_count(userName, followName):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    isFollowing = followName in user[FOLLOWING]
    return (isFollowing.count())


def get_followers(userName):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if user_exists(userName):
        return user[FOLLOWERS]
    raise Exception("User does not exist")


def get_followings(userName):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if user_exists(userName):
        return user[FOLLOWING]
    raise Exception("User does not exist")


def get_coins(userName):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if user_exists(userName):
        return user[COINS]
    raise Exception("User does not exist")


def user_coin_valuation(userName):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if not user_exists(userName):
        raise ValueError("User does not exist")

    value = 0
    for coin in user[COINS]:
        print(coin)
    return value


def access_profile_posts(userName, postNumber):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    return user[POSTS][postNumber-1]


def profile_add_post(userName, content):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if not user_exists(userName):
        raise ValueError("User does not exists")
    if content == "":
        raise ValueError("There is no content in the post")
    user[POSTS].append(content)
    del_user(userName)
    add_user(user["name"], user)
    # return {userName: user_types[userName]}
    return {userName: user_cleanUp(user)}


def profile_delete_post(userName, postNumber):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if not user_exists(userName):
        raise ValueError("User does not exists")
    if postNumber < 0 or postNumber >= len(user[POSTS]):
        raise ValueError("Post not found")
    print("POST NUMBER", postNumber)
    user[POSTS].remove(user[POSTS][postNumber])
    del_user(userName)
    add_user(user["name"], user)
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

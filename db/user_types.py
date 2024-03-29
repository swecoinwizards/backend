import db.db_connect as dbc
import db.coins as cn
import datetime
import bcrypt
import uuid

NAME = 'name'
EMAIL = 'email'
PASSWORD = 'password'
FOLLOWERS = 'Followers'
FOLLOWING = 'Following'
COINS = 'coins'
USERS_COLLECT = 'users'
USER_KEY = 'name'
POSTS = 'posts'
REQUIRED_FIELDS = [NAME, PASSWORD, EMAIL]


# helper function for inputting user data to db
def user_cleanUp(user):
    if '_id' in user:
        del user['_id']
    return user


def user_exists(name):
    """
    Returns true if a user exists, false if not
    """
    dbc.connect_db()
    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": name})
    return temp is not None


def update_username(username, newUsername):
    """
    Updates a user's username with newUsername (must be unique)
    """
    dbc.connect_db()
    if not isinstance(newUsername, str):
        raise TypeError(f'Wrong type for username: {type(newUsername)=}')

    if ' ' in newUsername:
        raise ValueError('Usernames should not contain any spaces')

    if len(newUsername) == 0:
        raise ValueError('Invalid length of username')

    temp = dbc.fetch_one(USERS_COLLECT,
                         {'name': newUsername})

    if temp is not None:
        raise ValueError(f'Username {newUsername=} already exists')

    res = dbc.update_one(USERS_COLLECT, {'name': username},
                         {'$set': {'name': newUsername}})

    if not res:
        raise ValueError('Error updating username')

    updated_details = dbc.fetch_one(USERS_COLLECT, {'name': newUsername})

    if updated_details is None:
        raise ValueError('Error fetching new user data')

    return updated_details


def get_users():
    """
    Returns all users from the database with details
    """
    dbc.connect_db()
    return dbc.fetch_all_proj(USERS_COLLECT, {"password": 0})


def get_user_names():
    """
    Returns a list of all usernames
    """
    dbc.connect_db()
    names = []
    users = dbc.fetch_all_proj(USERS_COLLECT, {"password": 0})
    for user in users:
        names.append(user["name"])
    return names


def get_posts(userName):
    """
    Returns a list of posts by a user
    """
    dbc.connect_db()

    if not user_exists(userName):
        raise ValueError(f'User {userName} does not exist')

    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})

    return temp[POSTS]


def get_user(username):
    """
    Returns a user and their details given their username
    """
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    dbc.connect_db()
    return dbc.fetch_one_proj(USERS_COLLECT,
                              {"name": username},
                              {"password": 0})


def get_user_email(username):
    """
    Returns a user's email given their username
    """
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": username})
    return user[EMAIL]


def get_user_password(username):
    """
    Return a user's password hash given their username
    """
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    dbc.connect_db()
    temp = dbc.fetch_one(USERS_COLLECT,
                         {"name": username})
    return temp[PASSWORD]


def add_user(name, details):
    """
    Adds a new user to the database
    """
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')

    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')

    if user_exists(name):
        raise ValueError(f'User {name} already exists!')

    for field in REQUIRED_FIELDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
        if not isinstance(details[field], str):
            raise ValueError(f'Wrong type for {field=}')
        if ' ' in details[field]:
            raise ValueError(f'{field=} cannot have any blank spaces')
        if len(details[field]) == 0:
            raise ValueError(f'{field=} cannot be empty')

    if not isinstance(details[EMAIL], str):
        raise TypeError(f'Wrong type for email: {type(name)=}')

    # checking for detail requirements
    if (' ' in name):
        raise ValueError('Invalid Name')

    if ('@' not in details[EMAIL]) or ('.' not in details[EMAIL]):
        raise ValueError('Invalid Email')

    details[PASSWORD] = details[PASSWORD].encode('utf-8')
    details[PASSWORD] = bcrypt.hashpw(details[PASSWORD], bcrypt.gensalt(10))
    # new users will start with no coins, followers/following
    if len(details) == 3:
        details[FOLLOWERS] = []
        details[FOLLOWING] = []
        details[COINS] = []
        details[POSTS] = []
    dbc.connect_db()
    # including user_cleanUp as extra safety
    dbc.insert_one(USERS_COLLECT, details)
    details[PASSWORD] = str(details[PASSWORD])
    return {name: user_cleanUp(details)}


def del_user(name):
    """
    Deletes a user from the database
    """
    # Should authenticate before deletion
    dbc.connect_db()
    if not user_exists(name):
        raise ValueError(f'User {name} does not exist')
    dbc.remove_one(USERS_COLLECT, {'name': name})
    return True


def following_exists(userName, followName):
    """
    Checks if userName IS FOLLOWING followName
    """
    if not user_exists(userName):
        raise ValueError(f'User {userName} does not exist')

    if not user_exists(followName):
        raise ValueError(f'User {followName} does not exist')

    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {'name': userName})

    return followName in user[FOLLOWING]


def follower_exists(userName, followName):
    """
    Checks if userName is BEING FOLLOWED by followName
    """
    if not user_exists(userName):
        raise ValueError(f'User {userName} does not exist')

    if not user_exists(followName):
        raise ValueError(f'User {followName} does not exist')

    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {'name': userName})

    return followName in user[FOLLOWERS]


def add_following(userName, followName):
    """
    userName will now be FOLLOWING followName
    followName will now have userName as a FOLLOWER
    """
    if userName == followName:
        raise ValueError("User cannot follow themselves")

    if (not user_exists(userName)):
        raise ValueError(f'{userName} does not exist')

    if (not user_exists(followName)):
        raise ValueError(f'{followName} does not exist')

    if follower_exists(followName, userName):
        raise ValueError(f'{userName} is already following {followName}')

    dbc.connect_db()

    if not dbc.update_one(USERS_COLLECT, {'name': userName},
                          {'$push': {FOLLOWING: followName}}):
        raise ValueError(f'Error adding {followName} to {userName} following')

    if not dbc.update_one(USERS_COLLECT, {'name': followName},
                          {'$push': {FOLLOWERS: userName}}):
        raise ValueError(f'Error adding {userName} to {followName} follower')

    res = dbc.fetch_one_proj(USERS_COLLECT,
                             {"name": userName},
                             {"password": 0})

    if not res:
        raise ValueError(f'Error fetching {userName} updated data')

    return res


def remove_follow(userName, followName):
    """
    userName will unfollow followName
    followName will lose userName as a follower
    """

    if userName == followName:
        raise ValueError('Invalid unfollow with self')

    if (not user_exists(userName)):
        raise ValueError(f'{userName} does not exist')

    if (not user_exists(followName)):
        raise ValueError(f'{followName} does not exist')

    if not following_exists(userName, followName):
        raise ValueError(f'{userName} does not follow {followName}')

    dbc.connect_db()
    if not dbc.update_one(USERS_COLLECT, {'name': userName},
                          {'$pull': {FOLLOWING: followName}}):
        raise ValueError(f'Error removing {followName}-{userName} following')

    if not dbc.update_one(USERS_COLLECT, {'name': followName},
                          {'$pull': {FOLLOWERS: userName}}):
        raise ValueError(f'Error removing {userName}-{followName} follower')

    res = dbc.fetch_one_proj(USERS_COLLECT,
                             {"name": userName},
                             {"password": 0})
    return res


def update_fields(userName, new_password, new_email):
    """
    Update fields for a user, either their password or email.
    All fields optional.
    """
    if new_password is None:
        new_password = ""
    if not isinstance(new_password, str):
        raise TypeError(f'Wrong type for password: {type(new_password)}')

    if not isinstance(new_email, str):
        raise TypeError(f'Wrong type for email: {type(new_email)}')

    if len(new_email) == 0:
        raise ValueError('Email cannot be empty')

    if new_email and (('@' not in new_email) or ('.' not in new_email)):
        raise ValueError('Invalid formatting for email, expected @ and .')

    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {NAME: userName})

    current_email = user[EMAIL]
    hash_pw = user[PASSWORD]
    message = ""

    # if (new_email and new_email == current_email):
    #     raise ValueError("New email must be different from the previous")

    encoded_new_password = new_password.encode('utf-8')

    if (new_email
            and new_email != current_email) and (
                new_password and not bcrypt.checkpw(
                    encoded_new_password, hash_pw)):
        message = "Updated Email and Password"
    elif new_email and new_email != current_email:
        message = "Updated Email"
    elif new_password != "" and not bcrypt.checkpw(
                                                   encoded_new_password,
                                                   hash_pw):
        message = "Updated Password"
    elif new_password == "" and new_email == current_email:
        raise ValueError(
            "New email " +
            "must be different from the previous")
    else:
        raise ValueError(
            "New email and password " +
            "must be different from the previous")

    # if new_password and bcrypt.checkpw(encoded_new_password, hash_pw):
    #     raise ValueError("New password must be different from the previous")

    if new_email and not dbc.update_one(USERS_COLLECT, {NAME: userName},
                                        {'$set': {EMAIL: new_email}}):
        raise ValueError('Error updating email')

    hash_new_pw = bcrypt.hashpw(encoded_new_password, bcrypt.gensalt(10))

    if new_password and not dbc.update_one(USERS_COLLECT, {NAME: userName},
                                           {'$set': {PASSWORD: hash_new_pw}}):
        raise ValueError('Error updating password')

    res = dbc.fetch_one_proj(USERS_COLLECT,
                             {"name": userName},
                             {"password": 0})
    return {"data": res, "message": message}


def user_coin_exists(userName, coin):
    """
    Check if a coin exists in the database
    """
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    return coin in user[COINS]


def add_coin(userName, coin):
    """
    Adds a new coin to a user's coin tracking
    """
    if not cn.coin_exists(coin):
        raise ValueError("Coin does not exist!")

    dbc.connect_db()
    user = dbc.fetch_one_proj(USERS_COLLECT,
                              {"name": userName},
                              {"password": 0})

    if not user_exists(userName):
        raise ValueError("User does not exists")

    if coin in user[COINS]:
        raise ValueError("Already Following Coin")

    if not dbc.update_one(USERS_COLLECT, {'name': userName},
                          {'$push': {COINS: coin}}):
        raise ValueError("Error following coin")

    user = dbc.fetch_one_proj(USERS_COLLECT,
                              {"name": userName},
                              {"password": 0})
    return {userName: user_cleanUp(user)}


def remove_coin(userName, coin):
    """
    Removes a coin from a user's coin tracking
    """
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if not user_exists(userName):
        raise ValueError("User does not exist")
    if coin not in user[COINS]:
        raise ValueError("Not Following Coin!")

    if not dbc.update_one(USERS_COLLECT, {'name': userName},
                          {'$pull': {COINS: coin}}):
        raise ValueError("Error unfollowing coin")
    # user = dbc.fetch_one(USERS_COLLECT,
    #                      {"name": userName})
    # return {userName: user_cleanUp(user)}
    return True


def follower_count(userName, followName):
    """
    Returns the count of a user's followers
    """
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    isFollowers = followName in user[FOLLOWERS]
    return (isFollowers.count())


def following_count(userName, followName):
    """
    Returns the count of a user's followings
    """
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    isFollowing = followName in user[FOLLOWING]
    return (isFollowing.count())


def get_followers(userName):
    """
    Returns followers of a user
    """
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if user_exists(userName):
        return user[FOLLOWERS]
    raise Exception("User does not exist")


def get_followings(userName):
    """
    Returns followings of a user
    """
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if user_exists(userName):
        return user[FOLLOWING]
    raise Exception("User does not exist")


def get_coins(userName):
    """
    Returns a list of a user's tracked coins
    """
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    if user_exists(userName):
        return user[COINS]
    raise Exception("User does not exist")


def parse_list(term, posts, posts_with_term):
    # helper function for get_all_posts
    for post in posts:
        if term in post["title"].lower():
            # print("title:", post["title"].lower())
            posts_with_term.append(post)
        elif term in post["content"].lower():
            # print("title:", post["title"].lower())
            posts_with_term.append(post)
        else:
            tags_lower = [tag.lower() for tag in post["tags"]]
            if term in tags_lower:
                posts_with_term.append(post)
    return posts_with_term


def get_all_posts(term):
    """
    Returns all posts made by a user
    """
    dbc.connect_db()
    users = dbc.fetch_all(USERS_COLLECT)
    # print(users)
    posts_with_term = []
    term = term.lower()
    print("term", term)
    if len(users) > 0:
        for user in users:
            lst = parse_list(term, user[POSTS], posts_with_term)
        return lst
    raise Exception("No Users")


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


def get_post_by_id(username, post_id):
    """
    Returns a post by id from a user
    """
    dbc.connect_db()
    post = dbc.fetch_one_proj(USERS_COLLECT,
                              {'name': username,
                               'posts.post_id': post_id},
                              {'name': 1,
                               'posts': {
                                 '$elemMatch': {
                                     'post_id': post_id
                                 }}})
    if not post:
        raise ValueError("Post does not exist")

    return post


def profile_remove_post(username, post_id):
    """
    Removes a user's post by id
    """
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    dbc.connect_db()
    if not dbc.update_one(USERS_COLLECT, {'name': username},
                          {'$pull': {'posts': {'post_id': post_id}}}):
        raise ValueError('Post does not exist')

    return get_user(username)


def profile_add_post(userName, title, content, tags):
    """
    Adds a new post for a user given a title, content, and list of tags
    """
    if not title or not content:
        raise ValueError("Empty fields are not allowed")

    if not user_exists(userName):
        raise ValueError("User does not exist")

    dbc.connect_db()

    new_post = {
        "post_id": str(uuid.uuid4()),
        "timestamp": str(datetime.datetime.now().isoformat()),
        "title": title,
        "content": content,
        "tags": tags
    }
    if not dbc.update_one(USERS_COLLECT, {'name': userName},
                          {'$push': {POSTS: new_post}}):
        raise ValueError("Error adding post")

    return get_user(userName)


def user_login(userName, password):
    """
    User authentication
    """
    if not user_exists(userName):
        raise ValueError("Login authentication failed")

    dbc.connect_db()
    data = dbc.fetch_one(USERS_COLLECT,
                         {"name": userName})
    hash_pw = data[PASSWORD]
    if bcrypt.checkpw(password.encode('utf-8'), hash_pw):
        return True
    else:
        raise Exception("Login authentication failed")

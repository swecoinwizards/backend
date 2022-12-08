import os

import pymongo as pm

# REMOTE = "0"
LOCAL = "0"
CLOUD = "1"

USER_DB = 'userdb'
COIN_DB = 'coindb'

client = None


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        print(os.environ.get("CLOUD_MONGO", LOCAL))
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("USERS_MONGO_PW")
            if not password:
                raise ValueError("You must set your" +
                                 "password to use Mongo in the cloud")
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://dalejandro:{password}' +
                                    '@cluster0.vvtc4yu.mongodb.net/?' +
                                    'retryWrites=true&w=majority')
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def insert_one(collection, doc, db=USER_DB):
    """
    Insert a single doc into collection.
    """
    client[db][collection].insert_one(doc)


def remove_one(collection, doc, db=USER_DB):
    client[db][collection].delete_one(doc)


def fetch_one(collection, filt, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    print("filt", filt)
    for doc in client[db][collection].find(filt):
        del doc['_id']
        return doc


def fetch_all(collection, db=USER_DB):
    ret = []
    for doc in client[db][collection].find():
        del doc['_id']
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=USER_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc['_id']
        print(doc)
        ret[doc[key]] = doc
    return ret

import api.coinmarket as cm

def testCoinmarketApi (): 
    status = cm.dummyGetApiToWork(cm.coinApiLink)
    assert isinstance(status, bool)
import hashlib, json, sys


# a simple function to hash the single blocks of the chain

def hashMe(msgToHash = ""):
    if(type(msgToHash) != str):
            msgToHash = json.dumps(msgToHash, sort_keys=True)
    # must make sure dictionary is sorted to ensure the same hash every time

    if sys.version_info.major == 2:
        return str(hashlib.sha256(msgToHash).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msgToHash).encode('utf-8')).hexdigest()


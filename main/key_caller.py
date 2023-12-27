# function to call the api key
# returns a string
import string

# returns a string
def call_key(path) -> string:
    with open(path) as f:
        key = f.readline()
        return key
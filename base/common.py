import datetime
import random
import string
from uuid import uuid5, NAMESPACE_X500

UUID = lambda x: str(uuid5(NAMESPACE_X500, str(x) + str(datetime.datetime.now()) + ''.join(
    random.sample(string.ascii_letters + string.digits, 8))))

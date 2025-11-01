from Crypto.Util.number import *

big_int = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

string = long_to_bytes(big_int)
print(string.decode())
#!/usr/bin/env python3

from pwn import *

###
# decrypt
#
message_b64 = 'ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw='
message = b64d(message_b64)
key = '{"showpassword":"no","bgcolor":"#ffffff"}'
print(xor(message, key))

# output => qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jq
# key => qw8J


###
# encrypt
#
message = '{"showpassword":"yes","bgcolor":"#ffffff"}'
key = 'qw8J'
print(b64e(xor(message, key)))

# output => ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK

# flag => natas12 is EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3

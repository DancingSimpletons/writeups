# Locked Dungeon 2
> The Dungeon Keeper learned from its mistake. This next lock is protected by even stronger encryption. We're so close to the final level...there has to be a way in.
>
> Connect: nc chal1.swampctf.com 1460

https://play.swampctf.com/files/ece0eeee169fe4fd3070f1b2f146c973/enter_the_dungeon2.py

This is a two-step challenge:

First, we have to create a modified encrypted output that, when decrypted, contains "get_modflag_md5": 
```python
enc_recv_str = raw_input()
dec_recv_str = aescipher.decrypt_wrapper(enc_recv_str)
if "get_modflag_md5" in dec_recv_str:
    # success
```

Once we are through this stage, we have to extract the flag, by submitting up to 500 encrypted values, and getting the md5 hash of the decrypted value back:
```python
enc_recv_str = raw_input()
dec_recv_str = aescipher.decrypt_wrapper(enc_recv_str)
sys.stdout.write(b64encode(md5(dec_recv_str).digest()))
```

First things first: this challenge uses AES in CBC mode, with a random key and IV for each connection. However, no MAC is being used,
so there is no authenticity provided. This means that, although we cannot directly decrypt the data, we can modify the contents.

This is a good moment to read up on [Block cipher modes](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation),
and specifically, understanding the following two images:

![CBC encryption](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/601px-CBC_encryption.svg.png)
![CBC decryption](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/CBC_decryption.svg/601px-CBC_decryption.svg.png)

For the first part of the challenge, we need to insert `get_modflag_md5` into the decrypted data. To do so, we use the knowledge that
`send_modflag_enc` will be part of the decrypted data. To simplify things, we will assume the decrypted data will have the form 
`send_modflag_encflag{.....}`. The same method can be extended to situations where `send_modflag_enc` is in another block.

First, note that we are using AES, which means a 16-byte block size. `send_modflag_enc` is _exactly_ 16 bytes. Now, let's take a look
at how CBC decryption works. We know the decrypted contents of the first block is `send_modflag_enc`, we know the encrypted first block
and we know the IV. Decryption of the first block works as follows: `decrypted_block = AES_Decrypt_block(encrypted_block) ⊕ IV`, i.e.,
`'send_modflag_enc' = AES_Decrypt_block(encrypted_block) ⊕ IV`. However, we can also _modify_ the IV, which means we can directly control
the decrypted block. If we choose `newIV = oldIV ⊕ 'send_modflag_enc' ⊕ 'get_modflag_md5 '`, then we find that

```
decrypted_block = AES_Decrypt_block(encrypted_block) ⊕ newIV
                = AES_Decrypt_block(encrypted_block) ⊕ oldIV ⊕ 'send_modflag_enc' ⊕ 'get_modflag_md5 '
                = 'send_modflag_enc' ⊕ 'send_modflag_enc' ⊕ 'get_modflag_md5 '
                = 'get_modflag_md5 '
```

In Python code, using [conn.py](https://github.com/DancingSimpletons/writeups/blob/master/swampctf-2018/conn.py):
```python
import time
import numpy as np
from conn import Conn

conn = Conn(port=1460)
time.sleep(0.2)

encdata = base64.b64decode(conn.read())
conn.read()

newIV = np.frombuffer(encdata[:16], dtype=np.uint8) ^ \
        np.frombuffer(b'send_modflag_enc', dtype=np.uint8) ^ \
        np.frombuffer(b'get_modflag_md5 ', dtype=np.uint8) 

newencdata = newIV.tobytes() + encdata[16:]

result = conn.send(base64.b64encode(newencdata))

if b'Dungeon goes deeper' not in result:
    raise Exception('try again!')
```

After we get `Dungeon goes deeper..` as result, we can continue with the second part of the challenge: extracting the flag. For this,
we first take a more detailed look at the decryption method:

```python
def decrypt_wrapper(self, encoded_enc_str):
    enc_str = b64decode(encoded_enc_str)
    return self.__decrypt(enc_str[16:], enc_str[:16])

def __decrypt(self, enc_str, iv):
    cipher = AES.new(self.key, AES.MODE_CBC, iv)
    decrypted_str = cipher.decrypt(enc_str)
    decrypted_str = unpad(decrypted_str)
    return decrypted_str
    
unpad = lambda inp: inp[:-ord(inp[-1])]
```

Where the `unpad` method looks interesting: this implements a very basic form of [PKCS7 unpadding](https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7),
without any validation (e.g. validating that the result is ≤ 16 bytes, that all removed padding bytes contain the same value). Note
that this validation is generally not useful, as the data should have been MACed to begin with.

What this means is that as long as we can change the last byte to be e.g. length-1, we get the md5 hash of the first character of the
plaintext data. We can then easily enumerate the md5 hashes, get the first character, and repeat with all subsequent characters.

The easiest way to do this is to add two blocks to the ciphertext: `aaaaaaaaaaaaaaaX aaaaaaaaaaaaaaa`, where we change `X` to be every
possible byte. This means that the decrypted last byte will be `plain_last_byte = AES_Decrypt(last_block)[-1] ⊕ X`, and because
`AES_Decrypt(last_block)[-1]` is constant, `plain_last_byte` will take every value (although we will not know which value corresponds
to which value of X).

When we do this, we will get a set of values that contains
- md5('')
- md5('s')
- md5('se')
- md5('sen')
- ...etc

First step is retrieving this set from the server:

```python
allmd5hashes = []

for testbyte in range(256):
    newencdata = encdata + \ 
                 b'a' * 15 + bytes([testbyte]) + \
                 b'a' * 16

    result = conn.send(base64.b64encode(newencdata), 0.5).strip()
    allmd5hashes.append(result)
```

and we find that indeed:
```
>>> base64.b64encode(md5(b'').digest()) in allmd5hashes
True
>>> base64.b64encode(md5(b's').digest()) in allmd5hashes
True
>>> base64.b64encode(md5(b'se').digest()) in allmd5hashes
True
>>> base64.b64encode(md5(b'send_modflag_enc').digest()) in allmd5hashes
True
```
Nice!

We can then build the plaintext, one byte at a time:
```python
f = b''

# loop over positions
for i in range(100):
    # loop over character hypotheses
    for char in range(256):
        testflag = f + bytes([char])
        if (base64.b64encode(md5(testflag).digest())) in allmd5hashes:
            print(testflag)
            f = testflag
            break
```

and we get in return:
```
b's'
b'se'
b'sen'
b'send'
b'send_'
b'send_m'
b'send_mo'
b'send_mod'
b'send_modf'
b'send_modfl'
b'send_modfla'
b'send_modflag'
[...]
b'send_modflag_encflag{Ev3n_dunge0ns_are_un5af3_wIth_vu1n_padding}'
```

so the flag is `flag{Ev3n_dunge0ns_are_un5af3_wIth_vu1n_padding}`.

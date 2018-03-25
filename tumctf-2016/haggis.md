Writeup for the [Haggis](https://2016.ctf.link/internal/challenge/2) flag.

The challenge is the following:

  * A message $m$ is padded, then encrypted using AES in CBC mode, with known key $K=0$ and IV $IV=0$, to ciphertext $c$.
  * $m$ needs to _start_ with "I solemnly swear that I am up to no good.\0"
  * $c$ needs to _end_ with 16 bytes that are randomly generated as challenge.

The code given for the challenge is as follows:
``` python
#!/usr/bin/env python3
 import os, binascii, struct
from Crypto.Cipher import AES

pad = lambda m: m + bytes([16 - len(m) % 16] * (16 - len(m) % 16))
def haggis(m):
    crypt0r = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10))
    return crypt0r.encrypt(len(m).to_bytes(0x10, 'big') + pad(m))[-0x10:]

target = os.urandom(0x10)
print(binascii.hexlify(target).decode())

msg = binascii.unhexlify(input())

if msg.startswith(b'I solemnly swear that I am up to no good.\0') \
        and haggis(msg) == target:
    print(open('flag.txt', 'r').read().strip()
```

First, let's take a look at how CBC encryption works:
![Image of CBC mode](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/601px-CBC_encryption.svg.png)

For every block of 16 bytes, the plaintext is XOR'ed with the 16-byte
ciphertext of the previous block (or the IV for the first block). The result
of this XOR is then encrypted using AES to form the ciphertext block. We can add
extra data to the plaintext, and we know the ciphertext of the given text, so we
can always fully control the input to AES, and therefore, the output.

How do we now construct our message? We construct the following template for the padded
message (i.e., the input to AES):

```
00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 40  |...............@|
00000010  49 20 73 6f 6c 65 6d 6e  6c 79 20 73 77 65 61 72  |I solemnly swear|
00000020  20 74 68 61 74 20 49 20  61 6d 20 75 70 20 74 6f  | that I am up to|
00000030  20 6e 6f 20 67 6f 6f 64  2e 00 00 00 00 00 00 00  | no good........|
00000040  ?? ?? ?? ?? ?? ?? ?? ??  ?? ?? ?? ?? ?? ?? ?? ??  |????????????????|
00000050  10 10 10 10 10 10 10 10  10 10 10 10 10 10 10 10  |................|
```

Where, from top to bottom, we have the big-endian length of our message (64 bytes),
the required plaintext, padded with NUL bytes, 16 bytes we directly control, and
16 bytes of 0x10 padding.

We now start by running the first 0x40 bytes through AES. This gives us the ciphertext of block 0x30,
which is used as IV for block 0x40.

``` python
binascii.hexlify(
    AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).encrypt(
        '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40'
        'I solemnly swear that I am up to no good.'
        '\x00\x00\x00\x00\x00\x00\x00'
    )[-16:]
)

b'017697c4110fa9b0824994eb7ba4a435'
```

The final two AES steps then are:

 * $c_{0x40}$ = AES($m_{0x30}$ ^ `017697c4110fa9b0824994eb7ba4a435`),
 * $c_{0x50}$ = AES(`10101010101010101010101010101010` ^ $c_{0x40}$)

Where $c_{0x50}$ is our target string. For this example, we take
$c_{0x50}$=`00112233445566778899aabbccddeeff` as target. We now work backwards,
using AES in decryption mode, and use IV=0 so that the XOR step is explicit:

``` python
xor = lambda a,b: bytes(i ^ j for (i,j) in zip(a,b))

target = binascii.unhexlify('00112233445566778899aabbccddeeff')
dec_target = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).decrypt(target)
# dec_target = 01b01ebc304cbe5467c4d78376f9641d
c40 = xor(dec_target, binascii.unhexlify('10101010101010101010101010101010'))
# c40 = 11a00eac205cae4477d4c79366e9740d
dec_c40 = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).decrypt(c40)
# dec_c40 = d277edfe984ec000752e51f28bab3eb1
m30 = xor(dec_c40, binascii.unhexlify('017697c4110fa9b0824994eb7ba4a435'))
# m30 = d3017a3a894169b0f767c519f00f9a84
```

So the message becomes:

```
msg = b"I solemnly swear that I am up to no good." + \
      b"\x00"*7 + \
      binascii.unhexlify('d3017a3a894169b0f767c519f00f9a84')
```

and the output from `haggis`:
```
binascii.hexlify(haggis(msg))

b'00112233445566778899aabbccddeeff'
```

Success! Rewriting for a generic input gives us the following script:

``` python
#!/usr/bin/env python3
import os, binascii, struct
from Crypto.Cipher import AES

xor = lambda a,b: bytes(i ^ j for (i,j) in zip(a,b))

target = binascii.unhexlify(input())
dec_target = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).decrypt(target)
c40 = xor(dec_target, binascii.unhexlify('10101010101010101010101010101010'))
dec_c40 = AES.new(bytes(0x10), AES.MODE_CBC, bytes(0x10)).decrypt(c40)
m30 = xor(dec_c40, binascii.unhexlify('017697c4110fa9b0824994eb7ba4a435'))

msg = b"I solemnly swear that I am up to no good." + b"\x00"*7 + m30
print(binascii.hexlify(msg))
```

# JS Safe 2.0 writeup

`You stumbled upon someone's "JS Safe" on the web. It's a simple HTML file that can store secrets in the browser's localStorage. This means that you won't be able to extract any secret from it (the secrets are on the computer of the owner), but it looks like it was hand-crafted to work only with the password of the owner..`

Along with this description we get a zip containing the html/js with the safe.

Let's first take a look at the code, we've got:

1. A script block with a function x(x).
2. An open_safe() function, calling the x(x) function.

## Looking at open_safe()

The open_safe function is the starting point, so why not start there.

```javascript
function open_safe() {
  keyhole.disabled = true;
  password = /^CTF{([0-9a-zA-Z_@!?-]+)}$/.exec(keyhole.value);
  if (!password || !x(password[1])) return document.body.className = 'denied';
  document.body.className = 'granted';
  password = Array.from(password[1]).map(c => c.charCodeAt());
  encrypted = JSON.parse(localStorage.content || '');
  content.value = encrypted.map((c,i) => c ^ password[i % password.length]).map(String.fromCharCode).join('')
}
```

So, the password needs to match the regular expression, and the part between the curly brackets needs to make the x(x) function return true. Next, let's take a look at the x(x) function.

## The x(x) function

```javascript
function x(х){ord=Function.prototype.call.bind(''.charCodeAt);chr=String.fromCharCode;str=String;function h(s){for(i=0;i!=s.length;i++){a=((typeof a=='undefined'?1:a)+ord(str(s[i])))%65521;b=((typeof b=='undefined'?0:b)+a)%65521}return chr(b>>8)+chr(b&0xFF)+chr(a>>8)+chr(a&0xFF)}function c(a,b,c){for(i=0;i!=a.length;i++)c=(c||'')+chr(ord(str(a[i]))^ord(str(b[i%b.length])));return c}for(a=0;a!=1000;a++)debugger;x=h(str(x));source=/Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;source.toString=function(){return c(source,x)};try{console.log('debug',source);with(source)return eval('eval(c(source,x))')}catch(e){}}
```

Well... that's not very easy to read. Let's 'prettify' it:

```javascript
function x(х) {
    ord = Function.prototype.call.bind(''.charCodeAt);
    chr = String.fromCharCode;
    str = String;

    function h(s) {
        for (i = 0; i != s.length; i++) {
            a = ((typeof a == 'undefined' ? 1 : a) + ord(str(s[i]))) % 65521;
            b = ((typeof b == 'undefined' ? 0 : b) + a) % 65521
        }
        return chr(b >> 8) + chr(b & 0xFF) + chr(a >> 8) + chr(a & 0xFF)
    }

    function c(a, b, c) {
        for (i = 0; i != a.length; i++) c = (c || '') + chr(ord(str(a[i])) ^ ord(str(b[i % b.length])));
        return c
    }
    for (a = 0; a != 1000; a++) debugger;
    x = h(str(x));
    source = /Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;
    source.toString = function() {
        return c(source, x)
    };
    try {
        console.log('debug', source);
        with(source) return eval('eval(c(source,x))')
    } catch (e) {}
}
``` 
It seems like there is some hashing function h(s), a 'crypto' function c(a, b, c) and some other logic. The hashing function basically takes the input and produces 4 bytes of output. The crypto function takes input `a` and XORs it with with `b` byte by byte and puts the result in `c`. 

The flag seems to be encrypted in `source`, but let's look at that later. First we'll see what else we've got.

Now trying to do anything with the debugger open will just give you some nice crashing tab in the browser, due to some anti-debugging measures that are present, like:

```javascript 
for (a = 0; a != 1000; a++) debugger;
```
This is pretty straightforward, it just triggers the debugger to break at that point every loop. Luckily it is fairly easy to get around it, in the console you can assign 999 to `a` and step further without wasting our time.

and:

```javascript
source.toString = function() {
    return c(source, x)
};
```
This is a nicer one, the toString will be called a little further on, when `console.log('debug', source)` is called. It will try to XOR `source` with `x`. However, source is a regular expression and therfore the `for (i = 0; i != a.length; i++)` will just loop forever. 

## Getting around the anti-debugging

Now the first idea might be to just remove all this annoying stuff from the source and just continue unimpeded. That's what we did, however we found out the resulting hash assigned to `x` would not decrypt the value of `source`. We looked at the part where `x` was supposed to me hashed and noticed the result was the same no matter the input. Upon closer inspection we saw the `x` passed in `x = h(str(x));` is actually he reference to the function `x(x)`. So modifying anything would mess up the hash you need to decrypt the value of `source`.

We then took an unmodified file and had to do some tricks to get around the anti-debugging via other ways. The looping call to `debugger;` wasn't really in the way, so we could just work around that. The way we got around the overridden source.toString() method was by adding this:
```javascript
var console = {};
console.log = function(){};
window.console = console;
```
This will just override the `console.log()` method, so it won't call the toString method on `source` and we'll be able to step through.

While debugging, we noted the output of `x = h(str(x));` and saved it (`[130, 30, 10, 154]`) we also noted down the states of `a` and `b` in the hash function, because variables `a` and `b` keep their values. The values are:  `a` = `2714`, `b` = `33310`.

Only one mystery remains: why doesn't the `eval('eval(c(source,x))')` also end up in an infinite loop? Reading MDN on [with](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Statements/with) gives us a clue: anything in the with block that can be resolved in the `source` object _will_ be resolved there... and a JS [RegExp object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) actually has a `source` [property](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/source), which contains... the source of the regex! So `with(source) eval('eval(c(source,x))` will actually call `c` with a _string_ containing the ciphertext.

## Decrypting
We can use now output of the hashing function to decrypt the value of source as follows:

```python
key = [130, 30, 10, 154] * 100
encrypted = [ord(c) for c in u"""Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤
¢dÈ9&òªћ#³­1᧨"""]

''.join([chr(ab ^ kb) for (ab, kb) in zip(encrypted, key)])
```
which gives us:

``` javascript
"х==c('¢×&Ê´cÊ¯¬$¶³´}ÍÈ´T©Ð8Í³Í|Ô÷aÈÐÝ&¨þJ',h(х))//᧢"
```

This output will be evaled again to decrypt `'¢×&Ê´cÊ¯¬$¶³´}ÍÈ´T©Ð8Í³Í|Ô÷aÈÐÝ&¨þJ'`, and the plaintext result needs to equal the part between the curly braces of our input. The ciphertext is to be decrypted with the hash of our input (i.e., the part of the flag between the curly braces). 

Here we know the key is 4 bytes long and will repeat. We know the plain text is limited to match the regex: `([0-9a-zA-Z_@!?-]+)`. We could just try all possibilities and see which one outputs some valid string. But because we'd rather be lazy, so we try some other way.

Instead of attacking all four bytes at the same time, we tackle them independently. For example, we know the first key byte will be XORed with each fourth ciphertext byte, i.e., `['¢', 'Ê', '¯', ...]`. Each of those XORs needs to result in a value in `[0-9a-zA-Z_@!?-]`. So we simply check all 255 possible values, and verify each XOR results in a valid plaintext:

```python
ciphertext = u'¢×&Ê´cÊ¯¬$¶³´}ÍÈ´T©Ð8Í³Í|Ô÷aÈÐÝ&¨þJ'

for i in range(4):
    options = set(range(256))

    for encrypted_char in ciphertext[i::4]:
        for option in list(options):
            plaint_text_char = chr(ord(encrypted_char) ^ option)
            if plaint_text_char not in legal_chars:
                options.remove(option)
                
    print("Possible values for key byte {}: {}".format(i, options))
```

Which gives us:
```
Possible values for key byte 0: {253}
Possible values for key byte 1: {149, 153}
Possible values for key byte 2: {21}
Possible values for key byte 3: {249}
```

Now it is just a matter of trying both options of the second byte, and we get the flag: 
```
'CTF{_N3x7-v3R51ON-h45-AnTI-4NTi-ant1-D3bUg_}'
```
# The Vault

> Has it been days? Weeks? You can't remember how long you've been standing at the door to the vault.
You can't remember the last time you slept
or ate,
or had a drop of water, for that matter.
But all of that is insignificant, in the presence of the untold fortunes that must lie just beyond the threshold.
>
>But the door. It won't budge. It says it will answer only to the DUNGEON_MASTER.
Have you not shown your worth?
But more than that,
It demands to know your secrets.
>
>Nothing you've tried has worked.
You've pled, begged, cursed, but the door holds steadfast, harshly judging your failed requests.
>
>But with each failed attempt you start to notice more and more
that there's something peculiar about the way the door responds to you.
>
>Maybe the door knows more than it's letting on.
...Or perhaps it's letting on more than it knows?
>
>NOTE: DO NOT USE AUTOMATED TOOLS
Connect
http://chal1.swampctf.com:2694
>
>-=Created By: juan=-

Following the link, we arrive at a page with a Door and username and password fields. The long challenge text gave us the username `DUNGEON_MASTER`, so let's just try to log in with `aaa` as the password and see what our browsers developer tools show :).

We get an alert stating `Invalid credential` and an HTTP 500 response
```
Request URL: http://chal1.swampctf.com:2694/login/DUNGEON_MASTER.aaa
Request Method: POST
Status Code: 500 Internal Server Error
Remote Address: 18.219.151.204:2694
Referrer Policy: no-referrer-when-downgrade
```
The response also contained some html
``` html
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>test_hash [9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0] does not match real_hash[40f5d109272941b79fdf078a0e41477227a9b4047ca068fff6566104302169ce]</pre>
</body>
</html>
```
Alright, the length of the hash makes me assume this is SHA256. I try hashing my input to see if the test_hash is something from my input and it is just the SHA256 hash of 'aaa'. 

Maybe this hash is know, so let's look online. Now at the moment I did this I forgot I could use the findmyhash script, so I just went to different websites to check the hash. At crackstation.net I found the plaintext of the real_hash, which is `smaug123`

Trying to log in with the user 'DUNGEON_MASTER' and password ''smaug123' yields us an alert with `flag{somewhere_over_the_rainbow_tables}`
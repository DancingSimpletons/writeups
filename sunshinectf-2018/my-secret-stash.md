# My Secret Stash
>Do you like secrets? I like secrets! In fact, I LOVE SECRETS! But there's no way I'll ever share my secrets with you! Not in a million years! I don't share secrets with anyone! Okay, I might share one secret with you, but I've stashed it away somewhere you'll never think to find it!If you can dig up my secert stash I'll let you have it! How about that huh? Does that sound like a fun game?
>
>See if you can dig up my secret stash!hahahahahahahahahahahaha!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>
>Author: hackucf_charlos
>
> file: secret-stuff.tar.gz

The archive contains the following structure:                                   
``` terminal
$ tree -a -L 1 my-secret-stash-repo/
my-secret-stash-repo/
├── .git
└── secrets
```

Ok so it has a git repository, let's look at the log:
``` terminal
$ git log
commit 14a5c7088e7638abb2232c8cac1c7dd4687819f0
Merge: 7e29273 7b82ac0
Author: Carlos Staszeski <cstaszeski@gmail.com>
Date:   Thu Mar 15 20:31:39 2018 -0400

    WIP on master: 7e29273 vegan!

commit 7b82ac03c49c0b55a4a8b8ffb3c04c5fe565fba6
Author: Carlos Staszeski <cstaszeski@gmail.com>
Date:   Thu Mar 15 20:31:39 2018 -0400

    index on master: 7e29273 vegan!

commit 7e2927361b7e4101e07fc5a475bb244622a275e3
Author: Carlos Staszeski <cstaszeski@gmail.com>
Date:   Thu Mar 15 20:29:53 2018 -0400

    vegan!
```

So there are some commits
``` terminal
$ cat secrets
I'm so very sorry, you will not find my secrets in here. There was a time at which I wanted to share my secrets with someone, but that was long ago and I don't trust anyone anymore. I want to keep all of my secrets to myself for now on! Good luck trying to find them, there's nothing to find. hehehehehehehehe!!!!!!

$ git checkout 92fb7e7ebbc65d04ac311c3f1d4e496cd867e94d

$ cat secrets
I feel like we are becoming good friends you and I. Yes. I even considered letting you in on one of my secrets just now, but I didn't want to risk it falling into the wrong hands. So instead I stashed it away and destroyed it so that no one would ever be able to recover my secrets! muahahahahahah!!!!!!

$ git checkout 7e2927361b7e4101e07fc5a475bb244622a275e3

$ cat secrets
So, you've discovered how to travel back in time did you? Well that's not going to help you much here, you see, my stash is so well hidden you will never ever ever find it! hahahahahahahahhahahahahahahahahahahah!!!!!!!!!!!!!
```

Ok, so the flag is hidden somewhere else in the repository. After looking for branches (there were none) and some other places, I ran `git fsck`.

``` terminal
$ git fsck
Checking object directories: 100% (256/256), done.
dangling commit 14a5c7088e7638abb2232c8cac1c7dd4687819f0

$ git checkout 14a5c7088e7638abb2232c8cac1c7dd4687819f0

$ cat secrets
sun{git_gud_k1d}
```

Alright, there we have `sun{git_gud_k1d}`. The flag was hidden in a dangling commit! 
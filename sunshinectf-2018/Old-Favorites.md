# Old Favorites

>We were sent this file with the description '9/10 people could find the hidden flag, are you one of them?'.
>
>Author: hackucf_loavso
>
>OldFavorites.mp4

Okidoki, a forensics challenge with a video. Let's try to open it and see what we've got.

![screenshot](https://github.com/DancingSimpletons/writeups/blob/master/sunshinectf-2018/OldFavorites.gif)

DAMN IT, they got me.

Might as well watch the video to see if there's anything obvious. Around 2:20 into the video, there are some noticeable audio distortions.

To extract the audio from the mp4, we can run the following: `ffmpeg -i OldFavorites.mp4 OldFavorites.wav`

We need it as a *wav* file so we can open it with Sonic Visualiser and/or Audacity and check what's going on. So let's open it up and see what we can see around 2:20 in the audio. With these kind of challenges there's often something in the spectrogram, so we will first view that.
![spectrogram](https://github.com/DancingSimpletons/writeups/blob/master/sunshinectf-2018/spectrogram.PNG)

Well, there it is `sun{you_know_the_rules}`
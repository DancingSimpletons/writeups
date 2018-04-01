# Etherealboy

>A new wizard has arrived in your town and with him he brings a strange technology. He has started handing out these tiny boxes with moving pictures on them. Apparently anyone who can find his secret message will be rewarded greatly. Do you have the skills to break the code of this new device?
>
>-=Created By: matg=-

The challenge supplies us with a file named `game.gb, which seems like it will be a GameBoy rom. This challenge falls in the Forensics category, so hopefully it will be a bit light on reversing.

First, let's see what happens if we just open the rom in an emulator. I downloaded the emulator called [bgb](http://bgb.bircd.org/) to run the rom, since this also includes a debugger that might come in handy.

The game starts and shows us the below screen. Our character is in the middle and we're able to walk around and interact with the npc at the top.

![game screen](https://raw.githubusercontent.com/DancingSimpletons/writeups/master/swampctf-2018/game-screenshot.bmp)

If we interact with the npc we get some hex value in the middle of the screen and every interaction just gives a new one. An example is in the image below.

![hex value in screen](https://raw.githubusercontent.com/DancingSimpletons/writeups/master/swampctf-2018/game-screenshot2.bmp)

The characters don't really give me much information, so I decide to take a look around the different features of the debugger in the emulator. Maybe I can find some strings in memory, or maybe there is something that will help me further.

I get memory and assembly dumps through the emulator and search them for something like 'flag' or 'flag{' but i get no usable result. Time to look at some other things.

Since the challenge is forensics, I just keep looking if there's something in the resources of this rom. So let's open up the VRAM viewer of bgb. It has 4 tabs: 
* BG map
* Tiles
* OAM
* Palettes

`BG map` shows, as the name suggests, the background we see in the screenshots. Nothing much besides that. Next tab is `Tiles`.
![tiles](https://raw.githubusercontent.com/DancingSimpletons/writeups/master/swampctf-2018/bgb-debugger-tiles.jpg)

Ok, well that wasn't what I expected...
So there's our flag `flag{und3r_th3_hood}`
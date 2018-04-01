# Words of Power

> You push the wooden door. It creaks open to reveal a dust covered study. Cobwebs string across the dilapidated armchair and fine fibers stream down from the ceiling. Grey, dusty tomes line the walls. Nothing stands out...except one book which pulses, gently disturbing the dust around it. You walk over to the book and slide it from its shelf. It feels warm to the touch and tingles in your hand.
>
> You open it to find incomprehensible three word phrases written on every page. None of the words stand out on their own, yet you feel you that together they bring meaning. Decipher the book's contents and be rewarded with a new found understanding of the world around you.
> 
> Hint: the title of the book is Magni Momenti Locat

The attached file contains a series of lines with three words:

```
dunk.curing.leaned
dimly.paths.thickly
wader.tunic.pinches
sizzled.hotdogs.goals
cease.authors.crashed
prattle.bookmark.scorecard
shopper.tripped.seedless
walkway.repaint.song
bony.intestine.bubble
```

One of the many projects to make GPS coordinates more user-friendly is https://what3words.com/. Let's try to see if these locations resolve:

- https://map.what3words.com/dunk.curing.leaned
- https://map.what3words.com/dimly.paths.thickly
- https://map.what3words.com/wader.tunic.pinches

Ok, that seems to work! W3w luckily also has [an API](https://docs.what3words.com/api/v2/), which we can use in Python.
After installing [what3words-python-wrapper](https://github.com/what3words/w3w-python-wrapper), we can simply:

```python
import what3words
import requests

w3w = what3words.Geocoder(API_KEY)

words = [line.strip()
         for line in requests.get(
            "https://play.swampctf.com/files/4fdecbe9383a45cf6e1f29f9c1daac8e/book-pages.txt"
         ).text.strip().split("\n")]

coordinates = []

for word in words:
    coordinates.append(w3w.forward(addr=word)['geometry'])
```

We then plot the coordinates using matplotlib:
```python
from matplotlib import pyplot as plt

lat = [c['lat'] for c in coordinates]
lng = [c['lng'] for c in coordinates]

plt.subplot(aspect='equal')
plt.plot(lng, lat, ".")
```

and find the flag:

![flag](https://github.com/DancingSimpletons/writeups/blob/master/swampctf-2018/words-of-power.png)

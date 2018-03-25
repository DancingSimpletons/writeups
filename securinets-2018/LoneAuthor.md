# Lone Author

**Unfortunately we were only able to solve this challenge after the CTF ended. 
No tasks were available anymore, so I couldn't get the challenge text :(**

The gist of the challenge (as far as I remember): 
*Something happened and the lone_author.zip file was found/recovered or whatever.*

We'll have to find the flag in this zip file.

## The lone_author Zip file

So we have a Zip file... Let's see what happens if we look try to unzip

``` console
$ unzip lone_author.zip
Archive:  lone_author.zip
  End-of-central-directory signature not found.  Either this file is not
  a zipfile, or it constitutes one disk of a multi-part archive.  In the
  latter case the central directory and zipfile comment will be found on
  the last disk(s) of this archive.
note:  lone_author.zip may be a plain executable, not an archive
unzip:  cannot find zipfile directory in one of lone_author.zip or
        lone_author.zip.zip, and cannot find lone_author.zip.ZIP, period.
```
Ok... I don't know what I expected...

So what's up with this 'zip', let's look at the raw data.
```console
$ xxd -l 256 lone_author.zip
00000000: 504b 4603 0414 0000 0008 0059 8a75 4cef  PKF........Y.uL.
00000010: 0bc5 ad41 1f00 00d2 6202 0009 001c 0071  ...A....b......q
00000020: 725f 7073 2e74 6966 5554 0900 03e9 85b2  r_ps.tifUT......
00000030: 5aec 85b2 5a75 780b 0001 04e8 0300 0004  Z...Zux.........
00000040: e803 0000 ec3a 095c 1357 9f2f 9c8a 80a2  .....:.\.W./....
00000050: 58ad 7e6a 5494 7a84 9084 2410 3914 44c5  X.~jT.z...$.9.D.
00000060: ca21 2078 21df 6432 0929 4926 2613 4014  .! x!.d2.)I&&.@.
00000070: e2d5 5a6d d5ad a2d6 abb4 56a5 722e d60b  ..Zm......V.r...
```
Ok, so [this is what wikipedia says](https://en.wikipedia.org/wiki/Zip_(file_format)) about the ZIP format:
<table>
  <tbody>
    <tr>
      <th>Offset</th>
      <th>Bytes</th>
      <th>Description</th>
    </tr>
    <tr>
      <td>0</td>
      <td>4</td>
      <td>Local file header signature = 0x04034b50 (read as a little-endian number)</td>
    </tr>
  </tbody>
</table>

What we have `50 4b 46 03 04` vs what we expect `50 4b 03 04`. 
So we have a byte extra, that's weird. Do the other headers have an extra byte as well?
```
50 4B 46 03 04
50 4B 61 03 04
50 4B 67 03 04
50 4B 7B 03 04
50 4B 4D 07 08
50 4B 33 01 02
50 4B 33 05 06
50 4B 74 01 02
50 4B 5F 4D 01 02
50 4B 33 01 02
50 4B 5F 31 05 06
```
So apparently some had 2 extra bytes (between the 0x504B and the second half of the ID), but they are all printable ASCII characters.
All extra bytes combine to `46 61 67 7B 4D 33 33 74 5F 33 5F`, which can be represented as `Flag{M33t_M3_1` too.

Alright! However, that only seems to be half of a flag. Let's continue :)

## Lone Author zip, continued

So we know that the headers are not correct, so will the ZIP be valid if we just remove all these extra bytes from the headers?

**_Spoiler alert_**: it is :D

Unzipping gives us three files:
- some file named `0e68542470`
- a TIFF file named `qr_ps.tif`
- another ZIP file named `secret.zip`

### the 0e68542470 file
Okay, let's just hexdump this puppy
```console
$ xxd 0e68542470
00000000: 4d61 6e2c 2079 6f75 2068 6176 6520 746f  Man, you have to
00000010: 2074 6869 7320 7468 6973 2054 4946 4621   this this TIFF!
```
Okay... i have to do what to the TIFF? Let's just open the TIFF and see.

### the qr_ps.tif
Opening the TIFF file shows us this partial qr code:
![Partial qr code](https://github.com/DancingSimpletons/writeups/blob/master/securinets-2018/qr_ps-tif.png)

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

### secret.zip
Ok, secret.zip contains an image. But it also is password protected =( I guess the other files will get us the password.

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

Hmm, I think this qr code is beyond saving. So let's just look at the file, maybe there is something besides the image itself.

Things like binwalk or file don't really show things that catch my eye. So maybe just look at the raw data, maybe there is something there. A quick scan through the whole file doesn't show much of interest. So let's just go through the metadata a bit more carefully.
```console
00000000: 4949 2a00 0800 0000 1600 fe00 0400 0100  II*.............
00000010: 0000 0000 0000 0001 0300 0100 0000 af00  ................
00000020: 0000 0101 0300 0100 0000 af00 0000 0201  ................
00000030: 0300 0400 0000 1601 0000 0301 0300 0100  ................
00000040: 0000 0100 0000 0601 0300 0100 0000 0200  ................
00000050: 0000 1101 0400 0100 0000 4e84 0000 1201  ..........N.....
00000060: 0300 0100 0000 0100 0000 1501 0300 0100  ................
00000070: 0000 0400 0000 1601 0300 0100 0000 af00  ................
00000080: 0000 1701 0400 0100 0000 84de 0100 1a01  ................
00000090: 0500 0100 0000 1e01 0000 1b01 0500 0100  ................
000000a0: 0000 2601 0000 1c01 0300 0100 0000 0100  ..&.............
000000b0: 0000 2801 0300 0100 0000 0200 0000 3101  ..(...........1.
000000c0: 0200 2200 0000 2e01 0000 3201 0200 1400  ..".......2.....
000000d0: 0000 5001 0000 5201 0300 0100 0000 0100  ..P...R.........
000000e0: 0000 bc02 0100 4a1c 0000 6401 0000 4986  ......J...d...I.
000000f0: 0100 c218 0000 ae1d 0000 6987 0400 0100  ..........i.....
00000100: 0000 2484 0000 5c93 0700 b44d 0000 7036  ..$...\....M..p6
00000110: 0000 0000 0000 0800 0800 0800 0800 80fc  ................
00000120: 0a00 1027 0000 80fc 0a00 1027 0000 4164  ...'.......'..Ad
00000130: 6f62 6520 5068 6f74 6f73 686f 7020 4343  obe Photoshop CC
00000140: 2032 3031 3520 2857 696e 646f 7773 2900   2015 (Windows).
00000150: 3230 3138 3a30 333a 3231 2031 373a 3034  2018:03:21 17:04
00000160: 3a30 3400 3c3f 7870 6163 6b65 7420 6265  :04.<?xpacket be
00000170: 6769 6e3d 27ef bbbf 2720 6964 3d27 5735  gin='...' id='W5
00000180: 4d30 4d70 4365 6869 487a 7265 537a 4e54  M0MpCehiHzreSzNT
00000190: 637a 6b63 3964 273f 3e0a 3c78 3a78 6d70  czkc9d'?>.<x:xmp
000001a0: 6d65 7461 2078 6d6c 6e73 3a78 3d27 6164  meta xmlns:x='ad
000001b0: 6f62 653a 6e73 3a6d 6574 612f 2720 783a  obe:ns:meta/' x:
000001c0: 786d 7074 6b3d 2749 6d61 6765 3a3a 4578  xmptk='Image::Ex
000001d0: 6966 546f 6f6c 2031 302e 3735 273e 0a3c  ifTool 10.75'>.<
000001e0: 7264 663a 5244 4620 786d 6c6e 733a 7264  rdf:RDF xmlns:rd
000001f0: 663d 2768 7474 703a 2f2f 7777 772e 7733  f='http://www.w3
00000200: 2e6f 7267 2f31 3939 392f 3032 2f32 322d  .org/1999/02/22-
00000210: 7264 662d 7379 6e74 6178 2d6e 7323 273e  rdf-syntax-ns#'>
00000220: 0a0a 203c 7264 663a 4465 7363 7269 7074  .. <rdf:Descript
00000230: 696f 6e20 7264 663a 6162 6f75 743d 2727  ion rdf:about=''
00000240: 0a20 2078 6d6c 6e73 3a64 633d 2768 7474  .  xmlns:dc='htt
00000250: 703a 2f2f 7075 726c 2e6f 7267 2f64 632f  p://purl.org/dc/
00000260: 656c 656d 656e 7473 2f31 2e31 2f27 3e0a  elements/1.1/'>.
00000270: 2020 3c64 633a 666f 726d 6174 3e69 6d61    <dc:format>ima
00000280: 6765 2f74 6966 663c 2f64 633a 666f 726d  ge/tiff</dc:form
00000290: 6174 3e0a 203c 2f72 6466 3a44 6573 6372  at>. </rdf:Descr
000002a0: 6970 7469 6f6e 3e0a 0a20 3c72 6466 3a44  iption>.. <rdf:D
000002b0: 6573 6372 6970 7469 6f6e 2072 6466 3a61  escription rdf:a
000002c0: 626f 7574 3d27 270a 2020 786d 6c6e 733a  bout=''.  xmlns:
000002d0: 7064 663d 2768 7474 703a 2f2f 6e73 2e61  pdf='http://ns.a
000002e0: 646f 6265 2e63 6f6d 2f70 6466 2f31 2e33  dobe.com/pdf/1.3
000002f0: 2f27 3e0a 2020 3c70 6466 3a41 7574 686f  /'>.  <pdf:Autho
00000300: 723e 5061 7373 776f 7264 2074 6f20 7468  r>Password to th
00000310: 6520 7365 636f 6e64 2070 6172 7420 6973  e second part is
00000320: 2030 784e 4f58 2a2a 3c2f 7064 663a 4175   0xNOX**</pdf:Au
00000330: 7468 6f72 3e0a 203c 2f72 6466 3a44 6573  thor>. </rdf:Des
00000340: 6372 6970 7469 6f6e 3e0a 0a20 3c72 6466  cription>.. <rdf
00000350: 3a44 6573 6372 6970 7469 6f6e 2072 6466  :Description rdf
00000360: 3a61 626f 7574 3d27 270a 2020 786d 6c6e  :about=''.  xmln
00000370: 733a 7068 6f74 6f73 686f 703d 2768 7474  s:photoshop='htt
00000380: 703a 2f2f 6e73 2e61 646f 6265 2e63 6f6d  p://ns.adobe.com
00000390: 2f70 686f 746f 7368 6f70 2f31 2e30 2f27  /photoshop/1.0/'
000003a0: 3e0a 2020 3c70 686f 746f 7368 6f70 3a43  >.  <photoshop:C
000003b0: 6f6c 6f72 4d6f 6465 3e33 3c2f 7068 6f74  olorMode>3</phot
000003c0: 6f73 686f 703a 436f 6c6f 724d 6f64 653e  oshop:ColorMode>
000003d0: 0a20 3c2f 7264 663a 4465 7363 7269 7074  . </rdf:Descript
000003e0: 696f 6e3e 0a0a 203c 7264 663a 4465 7363  ion>.. <rdf:Desc
000003f0: 7269 7074 696f 6e20 7264 663a 6162 6f75  ription rdf:abou
00000400: 743d 2727 0a20 2078 6d6c 6e73 3a78 6d70  t=''.  xmlns:xmp
00000410: 3d27 6874 7470 3a2f 2f6e 732e 6164 6f62  ='http://ns.adob
00000420: 652e 636f 6d2f 7861 702f 312e 302f 273e  e.com/xap/1.0/'>
00000430: 0a20 203c 786d 703a 4372 6561 7465 4461  .  <xmp:CreateDa
00000440: 7465 3e32 3031 382d 3033 2d32 3154 3136  te>2018-03-21T16
00000450: 3a35 333a 3031 2b30 313a 3030 3c2f 786d  :53:01+01:00</xm
00000460: 703a 4372 6561 7465 4461 7465 3e0a 2020  p:CreateDate>.
```
I spy with my little eye...

```console
000002f0: 2f27 3e0a 2020 3c70 6466 3a41 7574 686f  /'>.  <pdf:Autho
00000300: 723e 5061 7373 776f 7264 2074 6f20 7468  r>Password to th
00000310: 6520 7365 636f 6e64 2070 6172 7420 6973  e second part is
00000320: 2030 784e 4f58 2a2a 3c2f 7064 663a 4175   0xNOX**</pdf:Au
00000330: 7468 6f72 3e0a 203c 2f72 6466 3a44 6573  thor>. </rdf:Des
00000340: 6372 6970 7469 6f6e 3e0a 0a20 3c72 6466  cription>.. <rdf
```

Alright, a password. Let's try it on the secret.zip we have :)

### secret.zip, revisited
Using the string `0xNOX**` as the password for secret.zip, we get another image. This displays the second half of the flag in plain text:

![second half of flag](https://github.com/DancingSimpletons/writeups/blob/master/securinets-2018/export.png)

Making the total flag `Flag{M33t_M3_1n_tHe_p4RK_T0mOrrOW}`.

**Now, we weren't able to submit the solution because the CTF closed by the time we found it**

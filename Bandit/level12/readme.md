# Level 12
## Connection
~~~~
ssh bandit12@bandit.labs.overthewire.org -p2220
password: 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
~~~~
## Goal
The password for the next level is stored in the file `data.txt`, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under `/tmp` in which you can work using `mkdir`. For example: `mkdir /tmp/myname123`. Then copy the datafile using `cp`, and rename it using `mv` (read the manpages!)

## Solution
We are provided with a dump from xxd:
~~~~
bandit12@bandit:~$ cat data.txt 
00000000: 1f8b 0808 d7d2 c55b 0203 6461 7461 322e  .......[..data2.
00000010: 6269 6e00 013c 02c3 fd42 5a68 3931 4159  bin..<...BZh91AY
00000020: 2653 591d aae5 9800 001b ffff de7f 7fff  &SY.............
00000030: bfb7 dfcf 9fff febf f5ad efbf bbdf 7fdb  ................
00000040: f2fd ffdf effa 7fff fbd7 bdff b001 398c  ..............9.
00000050: 1006 8000 0000 0d06 9900 0000 6834 000d  ............h4..
00000060: 01a1 a000 007a 8000 0d00 0006 9a00 d034  .....z.........4
00000070: 0d1a 3234 68d1 e536 a6d4 4000 341a 6200  ..24h..6..@.4.b.
00000080: 0069 a000 0000 0000 d003 d200 681a 0d00  .i..........h...
00000090: 0001 b51a 1a0c 201e a000 6d46 8068 069a  ...... ...mF.h..
000000a0: 6834 340c a7a8 3406 4000 0680 0001 ea06  h44...4.@.......
000000b0: 8190 03f5 4032 1a00 0343 4068 0000 0686  ....@2...C@h....
000000c0: 8000 0320 00d0 0d00 0610 0014 1844 0308  ... .........D..
000000d0: 04e1 c542 9ab8 2c30 f1be 0b93 763b fb13  ...B..,0....v;..
000000e0: 50c4 c101 e008 3b7a 92a7 9eba 8a73 8d21  P.....;z.....s.!
000000f0: 9219 9c17 052b fb66 a2c2 fccc 9719 b330  .....+.f.......0
00000100: 6068 8c65 e504 5ec0 ae02 fa6d 16bc 904b  `h.e..^....m...K
00000110: ba6c f692 356e c02b 0374 c394 6859 f5bb  .l..5n.+.t..hY..
00000120: 0f9f 528e 4272 22bb 103c 2848 d8aa 2409  ..R.Br"..<(H..$.
00000130: 24d0 d4c8 4b42 7388 ce25 6c1a 7ec1 5f17  $...KBs..%l.~._.
00000140: cc18 ddbf edc1 e3a4 67f1 7a4d 8277 c823  ........g.zM.w.#
00000150: 0450 2232 40e0 07f1 ca16 c6d6 ef0d ecc9  .P"2@...........
00000160: 8bc0 5e2d 4b12 8586 088e 8ca0 e67d a55c  ..^-K........}.\
00000170: 2ca0 18c7 bfb7 7d45 9346 ea5f 2172 01e4  ,.....}E.F._!r..
00000180: 5598 673f 45af 69b7 a739 7814 8706 04ed  U.g?E.i..9x.....
00000190: 5442 1240 0796 6cc8 b2f6 1ef9 8d13 421d  TB.@..l.......B.
000001a0: 461f 2e68 4d91 5343 34b5 56e7 46d0 0a0a  F..hM.SC4.V.F...
000001b0: 72b7 d873 71d9 6f09 c326 402d dbc0 7cef  r..sq.o..&@-..|.
000001c0: 53b1 df60 9ec7 f318 00df 3907 2e85 d85b  S..`......9....[
000001d0: 6a1a e105 0207 c580 e31d 82d5 8646 183c  j............F.<
000001e0: 6a04 4911 101a 5427 087c 1f94 47a2 270d  j.I...T'.|..G.'.
000001f0: ad12 fc5c 9ad2 5714 514f 34ba 701d fb69  ...\..W.QO4.p..i
00000200: 8eed 0183 e2a1 53ea 2300 26bb bd2f 13df  ......S.#.&../..
00000210: b703 08a3 2309 e43c 44bf 75d4 905e 5f96  ....#..<D.u..^_.
00000220: 481b 362e e82d 9093 7741 740c e65b c7f1  H.6..-..wAt..[..
00000230: 5550 f247 9043 5097 d626 3a16 da32 c213  UP.G.CP..&:..2..
00000240: 2acd 298a 5c8a f0c1 b99f e2ee 48a7 0a12  *.).\.......H...
00000250: 03b5 5cb3 0037 cece 773c 0200 00         ..\..7..w<...
~~~~

First let's extract the hex bytes from the hexdump.
~~~~
bandit12@bandit:~$ awk '//{print $2$3$4$5$6$7$8$9 }' data.txt | tr -d "\n" | awk '{print substr($1,1,1210)}'
1f8b0808d7d2c55b020364617461322e62696e00013c02c3fd425a68393141592653591daae59800001bffffde7f7fffbfb7dfcf9ffffebff5adefbfbbdf7fdbf2fdffdfeffa7ffffbd7bdffb001398c1006800000000d06990000006834000d01a1a000007a80000d0000069a00d0340d1a323468d1e536a6d44000341a62000069a00000000000d003d200681a0d000001b51a1a0c201ea0006d468068069a6834340ca7a83406400006800001ea06819003f540321a0003434068000006868000032000d00d00061000141844030804e1c5429ab82c30f1be0b93763bfb1350c4c101e0083b7a92a79eba8a738d2192199c17052bfb66a2c2fccc9719b33060688c65e5045ec0ae02fa6d16bc904bba6cf692356ec02b0374c3946859f5bb0f9f528e427222bb103c2848d8aa240924d0d4c84b427388ce256c1a7ec15f17cc18ddbfedc1e3a467f17a4d8277c8230450223240e007f1ca16c6d6ef0decc98bc05e2d4b128586088e8ca0e67da55c2ca018c7bfb77d459346ea5f217201e45598673f45af69b7a7397814870604ed5442124007966cc8b2f61ef98d13421d461f2e684d91534334b556e746d00a0a72b7d87371d96f09c326402ddbc07cef53b1df609ec7f31800df39072e85d85b6a1ae1050207c580e31d82d58646183c6a044911101a5427087c1f9447a2270dad12fc5c9ad25714514f34ba701dfb698eed0183e2a153ea230026bbbd2f13dfb70308a32309e43c44bf75d4905e5f96481b362ee82d90937741740ce65bc7f15550f24790435097d6263a16da32c2132acd298a5c8af0c1b99fe2ee48a70a1203b55cb30037cece773c020000
~~~~

Now, we want to convert this string to a file:
~~~~
$ mktemp -d
/tmp/tmp.rasMCilymY
$ awk '//{print $2$3$4$5$6$7$8$9 }' data.txt | tr -d "\n" | awk '{print substr($1,1,1210)}' | xxd -r -p > /tmp/tmp.rasMCilymY/file
$ file /tmp/tmp.rasMCilymY/file
/tmp/tmp.rasMCilymY/test: gzip compressed data, was "data2.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
~~~~

OK, we have to deal with a gzip compressed file, let's rename it and uncompress it
~~~~
$ cd /tmp/tmp.rasMCilymY/
$ mv file file.gz
$ gunzip file.gz
~~~~

Now we have a bzip2 compressed file, let's rename it and uncompressed it:
~~~~
$ file file 
file: bzip2 compressed data, block size = 900k
$ mv file file.bz2
$ bzip2 -d file.bz2 
~~~~

The resulting file is a gzip file, let's rename it and uncompress it.
~~~~
$ file file
file: gzip compressed data, was "data4.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix, original size modulo 2^32 20480
$ mv file file.gz
$ gunzip file.gz 
~~~~

Now, we have a tar achive. Let's rename the file, uncompress it, and remove the initial archive:
~~~~
$ file file 
file: POSIX tar archive (GNU)
$ mv file file.tar
$ tar xf file.tar 
$ rm file.tar
~~~~

Again, a tar archive:
~~~~
$ file data5.bin 
data5.bin: POSIX tar archive (GNU)
$ mv data5.bin data5.tar
$ tar xf data5.tar 
$ rm data5.tar 
~~~~

Now a bz2 archive:
~~~~
$ file data6.bin 
data6.bin: bzip2 compressed data, block size = 900k
$ mv data6.bin data6.bz2
$ bzip2 -d data6.bz2 
~~~~

Another tar archive:
~~~~
$ file data6 
data6: POSIX tar archive (GNU)
$ mv data6 data6.tar
$ tar xf data6.tar 
$ rm -f data6.tar 
~~~~

Now gzip:
~~~~
$ file data8.bin 
data8.bin: gzip compressed data, was "data9.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix, original size modulo 2^32 49
$ mv data8.bin data8.gz
$ gunzip data8.gz 
~~~~

At last, we are at the end:
~~~~
$ file data8 
data8: ASCII text
$ cat data8 
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
~~~~

# Flag
~~~~
level13:8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
~~~~
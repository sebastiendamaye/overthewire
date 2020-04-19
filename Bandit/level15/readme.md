# Level 15
## Connection
~~~~
ssh bandit15@bandit.labs.overthewire.org -p2220
password: BfMYroe26WYalil77FoDi9qh59eK5xNr
~~~~

## Goal
The password for the next level can be retrieved by submitting the password of the current level to port `30001` on `localhost` using SSL encryption.

Helpful note: Getting “HEARTBEATING” and “Read R BLOCK”? Use `-ign_eof` and read the “CONNECTED COMMANDS” section in the manpage. Next to ‘R’ and ‘Q’, the ‘B’ command also works in this version of that command…
* Commands you may need to solve this level: `ssh`, `telnet`, `nc`, `openssl`, `s_client`, `nmap`
* Helpful Reading Material
  * [Secure Socket Layer/Transport Layer Security on Wikipedia](https://en.wikipedia.org/wiki/Secure_Socket_Layer)
  * [OpenSSL Cookbook - Testing with OpenSSL](https://www.feistyduck.com/library/openssl-cookbook/online/ch-testing-with-openssl.html)

## Solution
Let's first confirm with `nmap` that a SSL service is running on port `30001`:
~~~~
$ nmap -sV -p 30001 127.0.0.1

Starting Nmap 7.40 ( https://nmap.org ) at 2020-04-19 22:53 CEST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00017s latency).
PORT      STATE SERVICE             VERSION
30001/tcp open  ssl/pago-services1?
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port30001-TCP:V=7.40%T=SSL%I=7%D=4/19%Time=5E9CBA6A%P=x86_64-pc-linux-g
SF:nu%r(GenericLines,31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20cu
SF:rrent\x20password\n")%r(GetRequest,31,"Wrong!\x20Please\x20enter\x20the
SF:\x20correct\x20current\x20password\n")%r(HTTPOptions,31,"Wrong!\x20Plea
SF:se\x20enter\x20the\x20correct\x20current\x20password\n")%r(RTSPRequest,
SF:31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\x20password\
SF:n")%r(Help,31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\x
SF:20password\n")%r(SSLSessionReq,31,"Wrong!\x20Please\x20enter\x20the\x20
SF:correct\x20current\x20password\n")%r(TLSSessionReq,31,"Wrong!\x20Please
SF:\x20enter\x20the\x20correct\x20current\x20password\n")%r(Kerberos,31,"W
SF:rong!\x20Please\x20enter\x20the\x20correct\x20current\x20password\n")%r
SF:(FourOhFourRequest,31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20c
SF:urrent\x20password\n")%r(LPDString,31,"Wrong!\x20Please\x20enter\x20the
SF:\x20correct\x20current\x20password\n")%r(LDAPSearchReq,31,"Wrong!\x20Pl
SF:ease\x20enter\x20the\x20correct\x20current\x20password\n")%r(SIPOptions
SF:,31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\x20password
SF:\n");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 88.58 seconds
~~~~

We'll use `openssl` with the `s_client` command and the `-ign_eof` option:

> **s_client**: This implements a generic SSL/TLS client which can establish a transparent connection to a remote server speaking SSL/TLS. It's intended for testing purposes only and provides only rudimentary interface functionality but internally uses mostly all functionality of the OpenSSL ssl library.

> **-ign_eof**: inhibit shutting down the connection when end of file is reached in the input.

~~~~
$ echo "BfMYroe26WYalil77FoDi9qh59eK5xNr" | openssl s_client -connect 127.0.0.1:30001 -ign_eof
CONNECTED(00000003)
depth=0 CN = localhost
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = localhost
verify return:1
---
Certificate chain
 0 s:/CN=localhost
   i:/CN=localhost
---
Server certificate
-----BEGIN CERTIFICATE-----
MIICBjCCAW+gAwIBAgIEYo1NxTANBgkqhkiG9w0BAQUFADAUMRIwEAYDVQQDDAls
b2NhbGhvc3QwHhcNMjAwMTA1MTQzNTU4WhcNMjEwMTA0MTQzNTU4WjAUMRIwEAYD
VQQDDAlsb2NhbGhvc3QwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAKF4u2eu
a8VipZPviX0hfNiCnaD2ojAffdBhKTy1bmZSNRuHPBDnU7z8rblNSknSjCITda1C
GEAI8ZktRbtLpBTbYeTgqPN/EiN5UIRMKbU6P2O93zNFPBsmyfQLrgt+DSLnsxlB
i/yYyT7WLdtNVBpgwRwkqi9K7dk9vf9waswLAgMBAAGjZTBjMBQGA1UdEQQNMAuC
CWxvY2FsaG9zdDBLBglghkgBhvhCAQ0EPhY8QXV0b21hdGljYWxseSBnZW5lcmF0
ZWQgYnkgTmNhdC4gU2VlIGh0dHBzOi8vbm1hcC5vcmcvbmNhdC8uMA0GCSqGSIb3
DQEBBQUAA4GBAJECW6IB3Ria4xG002BqD3zEbtmrDlK6nmJq+uQ4eJ6cT18o9REb
npy/lFzlv2LfcrYAnuAp6Fh89MKaYjNzJURjRQ9RkmcYgQJa1n+OBkATb7V+84/a
k9PDRkscxdNFMGBSvzFD33XZ5lbaGdrwCPyoxenoYghV/753wffN7J6H
-----END CERTIFICATE-----
subject=/CN=localhost
issuer=/CN=localhost
---
No client certificate CA names sent
Peer signing digest: SHA512
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 1019 bytes and written 269 bytes
Verification error: self signed certificate
---
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384
Server public key is 1024 bit
Secure Renegotiation IS supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : ECDHE-RSA-AES256-GCM-SHA384
    Session-ID: FE4AEFA009D14F32F188AD49A3BC2ABB9AD194F4E92807F7523325D8A8EF7A43
    Session-ID-ctx: 
    Master-Key: 97F2C89288763DAA2EA42E027C467E587285C7474C9A8A9B1C23B09BE393DE0095C8CA9BC495ED955BBCB473B131FABD
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 56 e9 4e 87 6a 28 48 d0-13 42 5f b9 61 b0 dd d0   V.N.j(H..B_.a...
    0010 - 19 56 01 d7 ee 53 4a f4-35 a1 a9 c6 23 40 a7 8b   .V...SJ.5...#@..
    0020 - 0e e4 e5 c9 3a 98 3a 86-be fb 77 8b f7 e4 7b 0f   ....:.:...w...{.
    0030 - a5 c9 81 18 b9 3b 19 bb-cc ae d5 03 14 90 ad 69   .....;.........i
    0040 - f0 d7 cd 40 15 6b 91 1c-3e e4 66 2f df 32 66 5a   ...@.k..>.f/.2fZ
    0050 - d5 29 38 a9 11 c8 f3 e3-9d 9d 54 ff ec 04 03 d3   .)8.......T.....
    0060 - 46 4c 8c e1 5a 50 33 fe-e5 f7 16 ce 57 6b fd a3   FL..ZP3.....Wk..
    0070 - e9 de 8b 0d ba 6e f1 73-cb 6a a1 16 b3 de 4f bd   .....n.s.j....O.
    0080 - 77 f0 79 3e 6a 91 63 32-3e 6d 68 54 d8 76 aa 72   w.y>j.c2>mhT.v.r
    0090 - 60 c9 70 5e ef ae 78 27-09 93 52 70 47 61 68 32   `.p^..x'..RpGah2

    Start Time: 1587329997
    Timeout   : 7200 (sec)
    Verify return code: 18 (self signed certificate)
    Extended master secret: yes
---
Correct!
cluFn7wTiGryunymYOu4RcffSxQluehd

closed
~~~~

# Flag
~~~~
level16:cluFn7wTiGryunymYOu4RcffSxQluehd
~~~~
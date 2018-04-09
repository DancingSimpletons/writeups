Search Box
----------

> This search engine doesn't look very secure.
>
> Or well coded.
>
> Or competent in any way shape or form.
>
> This should be easy.

>Note: flag is in /etc/flag.txt

>http://search-box.web1.sunshinectf.org

:information_source: _The challenge is no longer online, so this writeup was written from memory_

Let's open the URL and prod around. We find a search box, which can retrieve the source code of any page on https://www.google.com.

1. Different hostnames are all blocked. Examples are:
  * `evil.com` 
  * hostnames that include `www.google.com` such as `www.google.com.evil.com` 
  * URLs that include google.com such as `www.evil.com/http://www.google.com`

2. [php:// filter urls](https://www.idontplaydarts.com/2011/02/using-php-filter-for-local-file-inclusion/) do not work.

3. Appending a null byte to the query, i.e., `site=http%3A%2F%2Fwww.google.com%00` gives a warning: `curl_setopt(): Curl option contains invalid characters (\0)`
  * So null bytes are detected and blocked
  * We now know that the backend used is cURL
  
4. Googling for this error then leads to https://bugs.php.net/bug.php?id=68089
  * This has a nice example: `file:///etc/passwd%00http://google.com`
  * Apparently cURL also understands `file://` urls!
  * If you read carefully, you'll notice that this specific vulnerability is not addressed in PHP as it's considered a cURL issue
  
5. First focusing on the `file://` protocol: we notice that this protocol is supported, as `file://www.google.com` returns a _different_ error than before.

6. Testing locally, we find that `file://www.google.com/../etc/passwd` in fact reads `/etc/passwd`. However, search-box appends a `/`
   to the end of the url, which means the code would try to read `/etc/passwd/`, which of course doesn't exist.
   
7. Combining the two, we can send the null byte URLencoded to cURL. So the final attack URL becomes something like
   `file://www.google.com/../etc/flag.txt%00`. The final request thus becomes
   http://search-box.web1.sunshinectf.org/?submit=Submit&site=file%3A%2F%2Fwww.google.com%2F..%2Fetc%2Fflag.txt%2500
   and this finally gets us the flag.

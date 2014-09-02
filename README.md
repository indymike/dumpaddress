getum
=====

Command line tool for extracting urls from any text file, links 
from html and emails from text file.  

Uses the right method for the job:

* Emails are extracted using string processing instead of regular 
  expressions due to the complexity of RFC 5822.
* URLs are extracted using a very well designed regex.
* Links are extracted by parsing the href attribute of <a> tags.

Usage
-----
**$ getum --help**
Gets a list of commands
**$ getum links --help**
Gets help for links command

**$ getum urls somefile.txt**
returns a list of urls contained in somefile.txt.

**$ getum emails somefile.txt**
returns a list of email addresses

**$ getum emails somefile.txt >emails.txt**
saves all of the emails in somefile.txt in emails.txt

**$ getum links somefile.html**
returns a list of unique links from file

Notes
-----
* Python 3 only. This does not support Python 2. Really, let's
  move on to Python 3 already. It's really worth it. I promise.
* Regular Expressions are useful when they work, but can create 
  very subtle failures.

License
-------
This application is licensed under the BSD License.

Authors
-------
* Mike Seidle -- http://www.github.com/indymike

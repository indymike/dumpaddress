import re
import click
from unicodedata import category
from html.parser import HTMLParser


class AHrefParser(HTMLParser):
    """
    Parses links from <a> tags.

    prepend_text - text to prepend to each url (e.g. add domain to relative urls)
    """
    result = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a' :
            if self._unique:
                self.result.add(self._prepend_text+attrs[0][1])
            else:
                self.result.append(self._prepend_text+attrs[0][1])

    def __init__(self, *args, **kwargs):
        super().__init__(args)
        if 'unique' in kwargs:
            self.result = set() if kwargs['unique'] else []
            self._unique = kwargs['unique']
        else:
            self._unique = False
        if "prepend" in kwargs:
            self._prepend_text = kwargs['prepend']
        else:
            self._prepend_text = ''


def get_urls(f):
    """
    Returns a list of URLs found in string f.
    """
    # Danny Yoo's 2002 url regex. Still one of the best.
    # https://mail.python.org/pipermail/tutor/2002-September/017228.html
    urls = r'(?: %s)' % '|'.join("""http https telnet gopher file wais ftp scp ssh fish mailto""".split())
    ltrs = r'\w'
    gunk = r'/#~:.?+=&%@!\-'
    punc = r'.:?\-'
    any = "%(ltrs)s%(gunk)s%(punc)s" % { 'ltrs' : ltrs,
                                         'gunk' : gunk,
                                         'punc' : punc }

    url = r"""
        \b                            # start at word boundary
            %(urls)s    :             # need resource and a colon
            [%(any)s]  +?             # followed by one or more
                                      #  of any valid character, but
                                      #  be conservative and take only
                                      #  what you need to....
        (?=                           # look-ahead non-consumptive assertion
                [%(punc)s]*           # either 0 or more punctuation
                (?:   [^%(any)s]      #  followed by a non-url char
                    |                 #   or end of the string
                      $
                )
        )
        """ % {'urls' : urls,
               'any' : any,
               'punc' : punc }
    url_re = re.compile(url, re.VERBOSE | re.MULTILINE)
    return url_re.findall(f)




def get_hashtags(f):
    """
    returns a list of hashtags found in file like object.
    """
    pass

@click.group()
def cli():
    """
    Extracts urls or email addresses from any text file.
    """
    pass

@cli.command()
@click.argument('infile', 
                type=click.File())
def urls(infile):
    """Extract urls from file."""
    for u in get_urls(infile.read()):
        click.echo(u)

@cli.command()
@click.argument('infile', 
                type=click.File())
def emails(infile):
    """Extract emails from file."""
    
    valid_chars = "!#$%&'*+-/=?.^_`{|}~"
    valid_chars += 'abcdefghijklmnopqrstuvwxyz'
    valid_chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    valid_chars += '0123456789'
    check_list = []
    words = infile.read()
    for w in words.split(' '):
        if '@' in w:
            # clean up punctuation at end of email. easy.
            if '\n' in w:
                w = w.split('\n')[0]
            while category(w[-1]) != 'Ll':
                w = w[0:-1] if category(w[-1]) != 'Ll' else w
            # clean up the address part.
            w = w[1:] if w[0] == '"' else w
            w = w[1:] if w[0] == '.' else w
            w = w[1:] if w[0] not in valid_chars else w
            w = w[7:] if w.lower().startswith('mailto:') else w

            click.echo(w)
            
@cli.command()
@click.argument('infile',
                type=click.File())
def regex_emails(infile):
    """
    returns a list of emails found in infile
    """

    #re_emails = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
    re_emails = re.compile(r'[\w.-]+@[\w.-]+')
    #re_emails = re.compile(r'[\w\.-]+@[\w\.-]+')
    for email in re_emails.findall(infile.read()):
        click.echo(email)

@cli.command()
@click.argument('infile', 
                type=click.File())
@click.option('--prepend', 
              default='', 
              help='Text to prepend links with')
@click.option('--unique/--no-unique', 
              default=True, 
              help="Get unique or all links")
def links(infile, prepend, unique):
    """Extracts all links from html(ish) files."""
    p = AHrefParser(prepend=prepend,
                    unique=unique)
    p.feed(infile.read())
    for l in p.result:
        click.echo(l)


if __name__ == '__main__':
    cli()

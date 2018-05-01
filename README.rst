==========================================================================
squid-ext-acl-blacklist - Squid external acl blacklist helper
==========================================================================


What is this?
*************
``squid-ext-acl-blacklist`` provides an executable called ``ext_acl_blacklist``
for concurrent squid behavior.


Installation
************
*on most UNIX-like systems, you'll probably need to run the following
`install` commands as root or by using sudo*

**from source**

::

  pip install git+http://github.com/verdel/squid-ext-acl-blacklist

**or**

::

  git clone git://github.com/verdel/squid-ext-acl-blacklist.git
  cd squid-ext-acl-blacklist
  python setup.py install

as a result, the ``ext_acl_blacklist`` executable will be installed into
a system ``bin`` directory

Usage
-----
::
    ext_acl_blacklist --help
    usage: ext_acl_blacklist.py [-h] -f BLACKLIST_FILE [-l LOG_FILE]

    Squid external acl blacklist helper

    optional arguments:
      -h, --help            show this help message and exit
      -f BLACKLIST_FILE, --blacklist-file BLACKLIST_FILE
                            blacklist file
      -l LOG_FILE, --log-file LOG_FILE
                            log file path (defaults to
                            /var/log/squid/blacklist.log)

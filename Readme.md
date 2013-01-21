This stuff here will generate a nice resume for you based on your LinkedIn data. You will need to add, subtract, or shuffle some of this around to get it how you want it. Based off some stuff that Matt Joyce (http://www.github.com/openfly) wrote, but heavily modified.

Here is my scratchpad list of dependencies I had to resolve in OS X Mountain Lion to get this working. If you run the script, your error messages will usually be descriptive enough to get you to the next step.

-----

 $ ./get_lnkd_workhistory.py 
Traceback (most recent call last):
  File "./get_lnkd_workhistory.py", line 3, in <module>
    import Image
ImportError: No module named Image


 $ brew install jpeg
Warning: It appears you have MacPorts or Fink installed.
Software installed with other package managers causes known problems for
Homebrew. If a formula fails to build, uninstall MacPorts/Fink and try again.
Error: jpeg-8d already installed

-----

http://appelfreelance.com/2010/06/libjpeg-pil-snow-leopard-python2-6-_jpeg_resync_to_restart/

-----

 $ python selftest.py 
57 tests passed.

-----

 $ ./get_lnkd_workhistory.py 
Traceback (most recent call last):
  File "./get_lnkd_workhistory.py", line 7, in <module>
    import oauth2 as oauth
ImportError: No module named oauth2


 $ sudo easy_install -U setuptools


 $ easy_install oauth2

-----

 $ git clone https://github.com/defunkt/pystache.git
 $ cd pystache
 $ sudo python ./setup.py install

-----

 $ easy_install simplejson

-----

 $ export PATH=/fink-sw/lib:$PATH
 $ export PATH=/fink-sw/bin:$PATH

-----

easy_install linkedin-api-json-client

-----


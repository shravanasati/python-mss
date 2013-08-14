**WARNING**: this project is under heavy development, do not use in prod.

Python MSS
===

An attempt to create a full functionnal cross-platform multi-screen  
shot module in _pure_ python using ctypes.

Very basic, it will grab one screen shot by monitor or a screen shot  
of all monitors and save it to an optimised/progressive PNG/JPEG file.

MSS is for *Multi-Screen Shot*.

Dependancies & requirements
---

Python. And that is all :)  
MSS is writen in pure python, it uses ctypes.  
ctypes has been introduced in Python 2.5, before it will need ctypes modules to be installed separately.

Support
---

You can see the [support table](https://tiger-222.fr/tout/python-mss/support.html).  
Feel free to try MSS on a system we had not tested, and let report us by creating an [issue](https://github.com/BoboTiG/python-mss/issues).

Usage
---

It is quite easy, just call a new instance of `MSS*()` and then `save()`.  
You can pass `oneshot=True` to create one screen shot of all monitors.

    from platform import system
    from mss import *

    this_is = system()
    if this_is == 'Linux':
        MSS = MSSLinux
    elif this_is == 'Windows':
        MSS = MSSWindows
    else:
        err = 'System "{0}" not implemented.'.format(this_is)
        raise NotImplementedError(err)
    
    try:
        mss = MSS()

        # One screen shot per monitor
        for filename in mss.save():
            print('File "{0}" created.'.format(filename))

        # A shot to grab them all :)
        for filename in mss.save(oneshot=True):
            print('File "{0}" created.'.format(filename))
    except Exception as ex:
        print(ex)
        raise

Bonus
---

Just for fun ...  
Show us your screen shot with all monitors in one file, we will update the [gallery](https://tiger-222.fr/tout/python-mss/galerie/) ;)


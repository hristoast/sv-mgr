# sv-disable / sv-enable / sv-mgr

Easily enable or disable runit services.

## Installation

    sudo make install

This makes symlinks to the `sv_mgr.py` file in this repository.  Use the `DESTDIR` var to change the install location as needed.

## Why?

By its nature, [runit](http://smarden.org/runit/) is a set of very small tools; it doesn't do a lot of extra crap and I appreciate that.  Some may feel it is a bit minimalistic, but I think that's a strong point.

One thing I find myself doing over and over again, is enabling or disabling services by making or removing symlinks.  Easy enough, but it gets kind of old.

Inspired by this repetition, `sv-disable`, `sv-enable`, and `sv-mgr` were conceived to be used on a Void Linux setup but could work with any setup involving `runit`.

The idea is to have a nice-ish interface to disabling or enabling services:

    ➜ sudo sv-enable nginx
    [  OK  ]  Enabling service: 'nginx'

    ➜ sudo sv-disable nginx
    [  OK  ]  Disabling service: 'nginx'

    ➜ sudo sv-disable docker
    [ FAIL ]  'docker' is not enabled!

![in action](sv-mgr.gif)

## Goals

Not many: aside from disabling or enabling a service, listing of active services is available via `sv-mgr`.

In the future, it might be desirable to have the default directory values read from a config file.

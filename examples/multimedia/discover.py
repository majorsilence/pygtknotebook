#!/usr/bin/env python
# gst-python
# Copyright (C) 2006 Andy Wingo <wingo at pobox.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


import os
import sys

import pygtk
pygtk.require('2.0')
import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
import gst
from gst.extend import discoverer

def succeed(d):

    print('media type', d.mimetype)

    print('has video', d.is_video)
    if d.is_video:
        print('video caps', d.videocaps)
        print('video width (pixels)', d.videowidth)
        print('video height (pixels)', d.videoheight)
        print('video length (ms)', d.videolength / gst.MSECOND)
        print('framerate (fps)', '%s/%s' % (d.videorate.num, d.videorate.denom))

    print('has audio', d.is_audio)
    if d.is_audio:
        print('audio caps', d.audiocaps)
        print('audio format', d.audiofloat and 'floating-point' or 'integer')
        print('sample rate (Hz)', d.audiorate)
        print('sample width (bits)', d.audiowidth)
        print('sample depth (bits)', d.audiodepth)
        print('audio length (ms)', d.audiolength / gst.MSECOND)
        print('audio channels', d.audiochannels)
    
    sys.exit(0)

def discover(path):
    def discovered(d, is_media):
        if is_media:
            succeed(d)
        else:
            print "error: %r does not appear to be a media file" % path
            sys.exit(1)

    d = discoverer.Discoverer(path)
    d.connect('discovered', discovered)
    d.discover()
    gobject.MainLoop().run()

def usage():
    print >>sys.stderr, "usage: gst-discover PATH-TO-MEDIA-FILE"
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    path = sys.argv.pop()
    if not os.path.isfile(path):
        print >>sys.stderr, "error: file %r does not exist" % path
        usage()

    discover(path)

# This file is a personal plugin for beets.
# Copyright 2015, Len Joubert <lenjoubert gmail>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Generate tempo (bpm) for imported music. Requires
the aubio library (https://github.com/...).
"""
import time
import logging
from beets.plugins import BeetsPlugin
from beets import ui
from beets import config
from aubio import source, tempo
from numpy import median, diff
import socket


# Global logger.
log = logging.getLogger('beets')

RETRY_INTERVAL = 10  # Seconds.
RETRIES = 10


def fetch_item_tempo(lib, loglevel, item, write):
    """Fetch and store tempo for a single item. If ``write``, then the
    tempo will also be written to the file itself in the bpm field. The
    ``loglevel`` parameter controls the visibility of the function's
    status log messages.
    """
    # Skip if the item already has the tempo field.
    if item.bpm:
        log.log(loglevel, u'bpm already present: %s - %s - %s' %
                          (item.artist, item.title, item.bpm))
        return


    # Return generated tempo.
    tempo = get_file_bpm(item.path)
    if not tempo:
        log.log(loglevel, u'tempo not generated: %s - %s' %
                          (item.artist, item.title),test)
        return

    log.log(loglevel, ui.colorize('text_success', 'Generated tempo :') + u' %s - %s' %
                      (item.artist, item.title))
#    log.log(loglevel, ui.colorize('text_success', 'GENERATED:')) + log.log(loglevel, u'generated tempo: %s - %s' %
#                      (item.artist, item.title))

#    log.log(loglevel, ui.colorize('text_success', 'GENERATED:'))
#    log.log(loglevel, u'generated tempo: %s - %s' %
#                      (item.artist, item.title))
    item.bpm = int(tempo)
    if write:
        item.try_write()
    item.store()


def get_file_bpm(path, params = {}):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    try:
        win_s = params['win_s']
        samplerate = params['samplerate']
        hop_s = params['hop_s']
    except:
        """
        # super fast
        samplerate, win_s, hop_s = 4000, 128, 64 
        # fast
        samplerate, win_s, hop_s = 8000, 512, 128
        """
        # default:
        samplerate, win_s, hop_s = 44100, 1024, 512

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    # Convert to periods and to bpm 
    bpms = 60./diff(beats)
    b = median(bpms)
    return b

class MadmouseTempoPlugin(BeetsPlugin):
    def __init__(self):
        super(MadmouseTempoPlugin, self).__init__()
        self.import_stages = [self.imported]

    def commands(self):
        cmd = ui.Subcommand('tempo', help='fetch song tempo (bpm)')
        cmd.parser.add_option('-p', '--print', dest='printbpm',
                              action='store_true', default=False,
                              help='print tempo (bpm) to console')

        def func(lib, opts, args):
            # The "write to files" option corresponds to the
            # import_write config value.
            write = config['import']['write'].get(bool)

            for item in lib.items(ui.decargs(args)):
                fetch_item_tempo(lib, logging.INFO, item, write)
                if opts.printbpm and item.bpm:
                    ui.print_('{0} BPM'.format(item.bpm))
        cmd.func = func
        return [cmd]

    # Auto-fetch tempo on import.
    def imported(self, config, task):
        if self.config['auto']:
            for item in task.imported_items():
#                fetch_item_tempo(config.lib, logging.DEBUG, item, False)
                fetch_item_tempo(config.lib, logging.INFO, item, False)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: github.com/tintinweb

import os, subprocess
import sys
import time
from optparse import OptionParser
from electron_inject import ElectronRemoteDebugger, SCRIPT_HOTKEYS_F12_DEVTOOLS_F5_REFRESH
import logging

logger = logging.getLogger(__name__)

def launch_url(url):
    #https://stackoverflow.com/questions/4216985/call-to-operating-system-to-open-url
    if sys.platform == 'win32':
        os.startfile(url)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            logger.info ('Please open a browser on: ' + url)

def main():
    usage = """
    usage:
           electron_inject [options] - <electron application>

    example:
           electron_inject --enable-devtools-hotkeys - /path/to/electron/powered/application [--app-params app-args]
        """
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--enable-devtools-hotkeys",
                      action="store_true", dest="enable_devtools_hotkeys", default=False,
                      help="Enable Hotkeys F12 (Toggle Developer Tools) and F5 (Refresh) [default: %default]")
    parser.add_option("-b", "--browser",
                      action="store_true", dest="browser", default=False,
                      help="Launch Devtools in default browser. [default: %default]")
    parser.add_option("-t", "--timeout",
                      default=None,
                      help="Try hard to inject for the time specified [default: %default]")

    if "--help" in sys.argv:
        parser.print_help()
        sys.exit(1)
    if "-" not in sys.argv:
        parser.error("mandatory delimiter '-' missing. see usage or  --help")

    argidx = sys.argv.index("-")
    target = sys.argv[argidx + 1]
    if " " in target:
        target = '"%s"' % target
    target = ' '.join([target] + sys.argv[argidx + 2:]).strip()

    # parse args
    (options, args) = parser.parse_args(sys.argv[:argidx])
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)-8s - %(message)s')

    if not len(target):
        logger.error("mandatory argument <application> missing! see usage.")
        sys.exit(1)

    options.timeout = time.time() + int(options.timeout) if options.timeout else 5

    #
    erb = ElectronRemoteDebugger.execute(target)
    # launch browser?
    if options.browser:
        launch_url("http://%(host)s:%(port)s/" % erb.params)

    # erb = ElectronRemoteDebugger("localhost", 8888)
    windows_visited = set()
    while True:
        for w in (_ for _ in erb.windows() if _['id'] not in windows_visited):
            if options.enable_devtools_hotkeys:
                try:
                    logger.info("injecting hotkeys script into %s" % w['id'])
                    logger.debug(erb.eval(w, SCRIPT_HOTKEYS_F12_DEVTOOLS_F5_REFRESH))
                except Exception as e:
                    logger.exception(e)
                finally:
                    # patch windows only once
                    windows_visited.add(w['id'])

        if time.time() > options.timeout:
            break
        logger.debug("timeout not hit.")
        time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(format='[%(filename)s - %(funcName)20s() ][%(levelname)8s] %(message)s',
                        level=logging.INFO)
    logger.setLevel(logging.DEBUG)
    main()

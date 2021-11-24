#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: github.com/tintinweb

import sys
from optparse import OptionParser
from electron_inject import inject
import logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(format='[%(filename)s - %(funcName)20s() ][%(levelname)8s] %(message)s',
                        level=logging.INFO)
    logger.setLevel(logging.DEBUG)

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
    parser.add_option("-s", "--silent",
                      action="store_true", dest="silent", default=False,
                      help="Stay silent. Do not ask any questions. [default: %default]")
    parser.add_option("-t", "--timeout",
                      default=None,
                      help="Try hard to inject for the time specified [default: %default]")
    parser.add_option('-r', "--render-script",
                      action="append",
                      dest="render_scripts",
                      default=[],
                      type="string",
                      help="Add a script to be injected into each window (render thread)")

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

    if not options.silent and not options.browser and not len(options.render_scripts): # if non-silent standard execution
        # ask user if they want to open devtools in browser
        if(input("Do you want to open the Developer Console in your Browser? [y/N]").strip().lower().startswith("y")):
            options.browser = True
        
    inject(
        target,
        devtools=options.enable_devtools_hotkeys,
        browser=options.browser,
        timeout=options.timeout,
        scripts=options.render_scripts,
    )

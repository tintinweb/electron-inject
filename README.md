# 💉 electron-inject

You find yourself locked out of closed source electron applications with no easy way to enable developer tools? ↷ *electron-inject* is here to help 👲


*electron-inject* is an application wrapper that utilizes the remote debug console to inject javascript code into electron based applications. For example, this can be pretty handy to enable otherwise unavailable features like the built-in developer console.

![slack](https://cloud.githubusercontent.com/assets/2865694/24376228/70b2c2b0-133b-11e7-893c-c7a0ad262343.gif)


# install

    $ pip install electron-inject
    
or 

    $ python setup.py install
    
# usage

    $ python -m electron_inject --help
    Usage:
        usage:
               electron_inject [options] - <electron application>

        example:
               electron_inject --enable-devtools-hotkeys - /path/to/electron/powered/application [--app-params app-args]


    Options:
      -h, --help            show this help message and exit
      -d, --enable-devtools-hotkeys
                            Enable Hotkeys F12 (Toggle Developer Tools) and F5
                            (Refresh) [default: False]
      -b, --browser         Launch Devtools in default browser. [default: False]
      -t TIMEOUT, --timeout=TIMEOUT
                            Try hard to inject for the time specified [default:
                            none]
      -r RENDER_SCRIPTS, --render-script=RENDER_SCRIPTS
                            Add a script to be injected into each window (render
                            thread)

# Showcase

Inject hotkeys *F12:toggle devconsole* and *F5:reload* into closed source apps with devconsole disabled.

`--enable-devtools-hotkeys` .. enable developer hotkeys
`--timeout=xx` .. patch all known remote webContent/windows in a timeframe of `xx` seconds. set this to an arbitrary high value to make sure we're patching all future windows.

## whatsapp

`$ python -m electron_inject -d -t 60 - \\PATH\TO\Local\WhatsApp\app-0.2.2244\WhatsApp.exe`

![whatsapp gif](https://cloud.githubusercontent.com/assets/2865694/24376256/81d44e88-133b-11e7-961f-060e7b8201ed.gif)

If this gives you an error try launching it with the alternative browser method:

`$ python -m electron_inject --browser - \PATH\TO\Local\WhatsApp\app-0.2.2244\WhatsApp.exe`

## slack

`$ python -m electron_inject -d -t 60 - \\PATH\TO\Local\slack\app-2.5.2\slack.exe`

![slack](https://cloud.githubusercontent.com/assets/2865694/24376228/70b2c2b0-133b-11e7-893c-c7a0ad262343.gif)

# Render Scripts

Passing the -r file parameter allows to pass a list of scripts to be injected into the render thread. It does not follow imports, just evaluate the text

`python -m electron_inject -r ./test.js -r ~/test2.js -r /usr/bin/test3.js - /opt/electron-api-demos/Electron\ API\ Demos`

# Acknowledgments

- [NathanPB](https://github.com/NathanPB) - #7




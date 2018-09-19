#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: github.com/tintinweb

import requests
import time
import websocket
import json
import socket
import subprocess
import time

SCRIPT_HOTKEYS_F12_DEVTOOLS_F5_REFRESH = """document.addEventListener("keydown", function (e) {
    if (e.which === 123) {
        //F12
        require("electron").remote.BrowserWindow.getFocusedWindow().webContents.toggleDevTools();
    } else if (e.which === 116) {
        //F5
        location.reload();
    }
});"""


class LazyWebsocket(object):
    def __init__(self, url):
        self.url = url
        self.ws = None

    def _connect(self):
        if not self.ws:
            self.ws = websocket.create_connection(self.url)
        return self.ws

    def send(self, *args, **kwargs):
        return self._connect().send(*args, **kwargs)

    def recv(self, *args, **kwargs):
        return self.ws.recv(*args, **kwargs)

    def sendrcv(self, msg):
        self.send(msg)
        return self.recv()

    def close(self):
        self.ws.close()


class ElectronRemoteDebugger(object):
    def __init__(self, host, port):
        self.params = {'host': host, 'port': port}

    def windows(self):
        params = self.params.copy()
        params.update({'ts': int(time.time())})

        ret = []
        for w in self.requests_get("http://%(host)s:%(port)s/json/list?t=%(ts)d" % params).json():
            url = w.get("webSocketDebuggerUrl")
            if not url:
                continue
            w['ws'] = LazyWebsocket(url)
            ret.append(w)
        return ret

    def requests_get(self, url, tries=5, delay=1):
        last_exception = None
        for _ in range(tries):
            try:
                return requests.get(url)
            except requests.exceptions.ConnectionError as ce:
                # ignore it
                last_exception = ce
            time.sleep(delay)
        raise ce


    def sendrcv(self, w, msg):
        return w['ws'].sendrcv(msg)

    def eval(self, w, expression):

        data = {'id': 1,
                'method': "Runtime.evaluate",
                'params': {'contextId': 1,
                           'doNotPauseOnExceptionsAndMuteConsole': False,
                           'expression': expression,
                           'gneratePreview': False,
                           'includeCommandLineAPI': True,
                           'objectGroup': 'console',
                           'returnByValue': False,
                           'userGesture': True}}

        ret = json.loads(w['ws'].sendrcv(json.dumps(data)))
        if "result" not in ret:
            return ret
        if ret['result']['wasThrown']:
            raise Exception(ret['result']['result'])
        return ret['result']

    @classmethod
    def execute(cls, path):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()

        cmd = "%s %s" % (path, "--remote-debugging-port=%d" % port)
        print (cmd)
        p = subprocess.Popen(cmd, shell=True)
        time.sleep(0.5)
        if p.poll() is not None:
            raise Exception("Could not execute cmd: %r"%cmd)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for _ in range(30):
            result = sock.connect_ex(('localhost', port))
            if result > 0:
                break
            time.sleep(1)
        return cls("localhost", port=port)


if __name__ == "__main__":
    erb = ElectronRemoteDebugger("localhost", 8888)
    for w in erb.windows():
        print (erb.eval(w, SCRIPT_HOTKEYS_F12_DEVTOOLS_F5_REFRESH))

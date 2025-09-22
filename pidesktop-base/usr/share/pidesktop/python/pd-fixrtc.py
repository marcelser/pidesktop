#!/usr/bin/env python3

import os

def runCommand(command):
    print(command)
    with os.popen(command) as r:
        for line in r:
            print(line.strip())

def updategpio6():
    filename = '/boot/firmware/config.txt'
    key = 'gpio'
    value = '6=op,pn,dl'
    update = 0
    newValue = ''

    with open(filename, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()

    for line in lines:
        if key in line:
            if not line.strip().startswith('#'):
                sps = line.strip().split('=', 1)
                if len(sps) == 2 and sps[1] == value:
                    update = 1
                elif update == 0:
                    newValue += f'{key}={value}\n'
                    update = 2
        else:
            newValue += line

    if update != 1:
        if update == 0:
            newValue += f'\n{key}={value}\n'
        with open(filename, 'w', encoding='utf-8') as fw:
            fw.write(newValue)

def updategpio13():
    filename = '/boot/firmware/config.txt'
    key = 'gpio'
    value = '13=ip'
    update = 0
    newValue = ''

    with open(filename, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()

    for line in lines:
        if key in line:
            if not line.strip().startswith('#'):
                sps = line.strip().split('=', 1)
                if len(sps) == 2 and sps[1] == value:
                    update = 1
                elif update == 0:
                    newValue += f'{key}={value}\n'
                    update = 2
        else:
            newValue += line

    if update != 1:
        if update == 0:
            newValue += f'\n{key}={value}\n'
        with open(filename, 'w', encoding='utf-8') as fw:
            fw.write(newValue)

def updateConfig():
    filename = '/boot/firmware/config.txt'
    key = 'dtoverlay'
    value = 'i2c-rtc,pcf8563'
    update = 0
    newValue = ''

    with open(filename, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()

    for line in lines:
        if key in line:
            if not line.strip().startswith('#'):
                sps = line.strip().split('=', 1)
                if len(sps) == 2 and sps[1] == value:
                    update = 1
                elif update == 0:
                    newValue += f'{key}={value}\n'
                    update = 2
        else:
            newValue += line

    if update != 1:
        if update == 0:
            newValue += f'\n{key}={value}\n'
        with open(filename, 'w', encoding='utf-8') as fw:
            fw.write(newValue)

def removeFakeHwclock():
    command = 'sudo systemctl status fake-hwclock.service'
    with os.popen(command) as r:
        for line in r:
            if line.strip().startswith('Loaded:'):
                if 'enabled' in line:
                    runCommand('sudo systemctl disable fake-hwclock.service')

def updateHwclockSet():
    filename = '/lib/udev/hwclock-set'
    key = '-e /run/systemd/system'
    update = False
    doUpdate = False
    newValue = ''

    with open(filename, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()

    for line in lines:
        if line.strip().startswith('if') and key in line:
            update = True
            doUpdate = True
        if update:
            newValue += '#'
        if line.strip() == 'fi':
            update = False
        newValue += line

    if doUpdate:
        with open(filename, 'w', encoding='utf-8') as fw:
            fw.write(newValue)

if __name__ == "__main__":
    updateConfig()
    updategpio6()
    # updategpio13()
    updateHwclockSet()
    removeFakeHwclock()

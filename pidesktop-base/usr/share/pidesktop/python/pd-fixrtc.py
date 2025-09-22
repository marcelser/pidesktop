#!/usr/bin/env python3

import os

def runCommand(command):
    print(command)
    with os.popen(command) as r:
        for line in r:
            print(line.strip())

def updateConfig():
    filename = '/boot/firmware/config.txt'
    key = 'dtoverlay'
    value = 'i2c-rtc,pcf8563'
    target_line = f'{key}={value}'

    with open(filename, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()

    found = False
    has_sections = False
    has_all_section = False
    new_lines = []
    all_section_start = None
    next_section_start = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith('[') and stripped.endswith(']'):
            has_sections = True
            section_name = stripped[1:-1].strip().lower()
            if section_name == 'all':
                has_all_section = True
                all_section_start = i
            elif has_all_section and next_section_start is None:
                next_section_start = i

        if stripped.startswith(key + '=') and value in stripped:
            found = True

    if found:
        return

    new_lines = lines.copy()

    if has_all_section:
        insert_index = next_section_start if next_section_start is not None else len(new_lines)
        new_lines.insert(insert_index, f'{target_line}\n')

    elif has_sections:
        new_lines.append('\n[all]\n')
        new_lines.append(f'{target_line}\n')

    else:
        new_lines.append(f'\n{target_line}\n')

    with open(filename, 'w', encoding='utf-8') as fw:
        fw.writelines(new_lines)

def appendIfMissing(filename, key, value):
    target_line = f'{key}={value}'
    with open(filename, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()

    for line in lines:
        if line.strip().startswith(key + '=') and value in line:
            return

    with open(filename, 'a', encoding='utf-8') as fw:
        fw.write(f'\n{target_line}\n')

def updategpio6():
    appendIfMissing('/boot/firmware/config.txt', 'gpio', '6=op,pn,dl')

def updategpio13():
    appendIfMissing('/boot/firmware/config.txt', 'gpio', '13=ip')

def removeFakeHwclock():
    command = 'sudo systemctl status fake-hwclock.service'
    with os.popen(command) as r:
        for line in r:
            if line.strip().startswith('Loaded:') and 'enabled' in line:
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

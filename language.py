#!/bin/env python3
import subprocess

lang = subprocess.check_output(['setxkbmap', '-query']).split()
if 'us' in str(lang[-1]): subprocess.call(['setxkbmap', 'ru'])
else: subprocess.call(['setxkbmap', 'us'])

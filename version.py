#!/usb/bin/env python

import subprocess
import os

def exec_git(args):
  cmd = ['git']
  cmd.extend(args.split(' '))
  return subprocess.check_output(cmd, cwd="..", stderr=subprocess.STDOUT).strip().decode()

commit = exec_git('rev-parse --short HEAD') or 'unknown'

try:
  exec_git('diff --quiet')
except subprocess.CalledProcessError as e:
  if e.returncode == 1:
    commit += '-dirty'

branch = exec_git('rev-parse --abbrev-ref HEAD') or 'unknown'
branch_num = exec_git('rev-list --count HEAD') or 'n/a'

try:
  version = exec_git('describe --tags --abbrev=0 --exact-match')
except subprocess.CalledProcessError:
  version = 'unknown'

defines = [
  '-DGIT_COMMIT=\\"%s\\"' % commit,
  '-DGIT_BRANCH=\\"%s\\"' % branch,
  '-DGIT_BRANCH_NUM=\\"%s\\"' % branch_num,
  '-DVERSION=\\"%s\\"' % version
]


new_defines = ' '.join(defines)

with open('version.inc', 'r') as file:
  current_defines = file.read()

if current_defines != new_defines:
  with open('version.inc', 'w') as file:
    file.write(new_defines)
  os.utime('../lib/toolbox/version.c', None)
  print("Version information updated")
else:
  print("Version information hasn't changed")
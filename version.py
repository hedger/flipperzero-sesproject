#!/usb/bin/env python

import subprocess
import os
from datetime import date

def exec_git(args):
  cmd = ['git']
  cmd.extend(args.split(' '))
  return subprocess.check_output(cmd, cwd="..", stderr=subprocess.STDOUT).strip().decode()

commit = exec_git('rev-parse --short HEAD') or 'unknown'

dirty = False
try:
  exec_git('diff --quiet')
except subprocess.CalledProcessError as e:
  if e.returncode == 1:
    dirty = True
    commit += '-dirty'

branch = exec_git('rev-parse --abbrev-ref HEAD') or 'unknown'
branch_num = exec_git('rev-list --count HEAD') or 'n/a'
build_date = date.today().isoformat()

try:
  version = exec_git('describe --tags --abbrev=0 --exact-match')
except subprocess.CalledProcessError:
  version = 'unknown'

defines = [
  '-DGIT_COMMIT=\\"%s\\"' % commit,
  '-DGIT_BRANCH=\\"%s\\"' % branch,
  '-DGIT_BRANCH_NUM=\\"%s\\"' % branch_num,
  '-DVERSION=\\"%s\\"' % version,
  '-DBUILD_DATE=\\"%s\\"' % build_date,
  '-DBUILD_DIRTY=%s' % (dirty and 1 or 0)
]


new_defines = ' '.join(defines)
current_defines = None

try:
  with open('version.inc', 'r') as file:
    current_defines = file.read()
except FileNotFoundError:
  pass

if current_defines != new_defines:
  with open('version.inc', 'w') as file:
    file.write(new_defines)
  os.utime('../lib/toolbox/version.c', None)
  print("Version information updated")
else:
  print("Version information hasn't changed")
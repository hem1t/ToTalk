#! /bin/bash

pyinstaller -F -w ToTalk.py && (mv ./dist/ToTalk ./Executables/ToTalk && rm -r *.spec build dist)
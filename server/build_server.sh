#! /bin/bash

pyinstaller -F -w server.py && (mv ./dist/server ./Executables/server && rm -r *.spec build dist)
#!/bin/bash

VERSION=1.0.3

wget -O go$VERSION.src.tar.gz http://go.googlecode.com/files/go$VERSION.src.tar.gz
git clone https://github.com/davecheney/golang-crosscompile
tar -zcvf golang-crosscompile.tar.gz --exclude .git golang-crosscompile

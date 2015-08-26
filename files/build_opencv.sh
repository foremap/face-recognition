#!/bin/bash
unzip opencv-3.0.0.zip
mkdir -p opencv-3.0.0/release
cd opencv-3.0.0/release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON -D WITH_XINE=ON -D WITH_TBB=ON -D WITH_IPP=OFF ..
make && make install
cd ../../
rm -rf opencv-3.0.0
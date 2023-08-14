# Linux下安装ffmpeg的详细教程:
## CentOS

```commandline
yum install yasm

wget http://www.ffmpeg.org/releases/ffmpeg-3.1.tar.gz
tar -zxvf ffmpeg-3.1.tar.gz 

cd ffmpeg-3.1
./configure --prefix=/usr/local/ffmpeg
make && make install


vi /etc/profile

export PATH=$PATH:/usr/local/ffmpeg/bin

source /ect/profile

# verify if works.
ffmpeg -version

# install relative lib.
yum install libX11 libXext
ldconfig
find / -name "libX11.so.6"
export LD_LIBRARY_PATH="{YOUR-LIB-PATH}/libX11.so.6:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="{YOUR-LIB-PATH}/libXext.so.6:$LD_LIBRARY_PATH"
```

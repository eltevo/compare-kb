keras with theano on ubuntu

Make sure numpy and scipy are bleeding edge

pip3 install nose
pip3 install numpy scipy --upgrade

If complains about blas or lapack, install necessary packages.

# apt-get install libblas-dev liblapack-dev
# apt-get install libopenblas-dev
# apt-get install gfortran

Then run tests

1.NumPy (~30s): python3 -c "import numpy; numpy.test()"
2.SciPy (~1m): python3 -c "import scipy; scipy.test()"

Install cnmem for DL frameworks to manage cuda memory

% git clone https://github.com/NVIDIA/cnmem.git cnmem
% cd cnmem
% mkdir build
% cd build
% cmake ..
% make all
% make install

Install Theano from source

git clone git://github.com/Theano/Theano.git
cd Theano
python setup.py develop
cd ..

Create .theanorc in ~

[cuda]
root = /usr/local/cuda-6.5/bin

[global]
#device = gpu1
device = cpu
floatX = float32

[blas]
ldflags = -lopenblas

[lib]
cnmem = 1

----

Run tests:

3.Theano (~30m): python -c "import theano; theano.test()"

If libcublas is not found, add it to ldconf

# echo "/usr/local/cuda-6.5/lib64" > /etc/ld.so.conf.d/cuda.conf
# ldconfig


Manual Openblas 

# remove openblas if you installed it
sudo apt-get remove libopenblas-base
# Download the development version of OpenBLAS
git clone git://github.com/xianyi/OpenBLAS
cd OpenBLAS
make FC=gfortran
sudo make PREFIX=/usr/local/ install
# Tell Theano to use OpenBLAS.
# This works only for the current user.
# Each Theano user on that computer should run that line.
echo -e "\n[blas]\nldflags = -lopenblas\n" >> ~/.theanorc


Install cuDNN

download from https://developer.nvidia.com/cudnn

Clone Keras from github:

git clone https://github.com/fchollet/keras.git
cd keras
python3 setup.py install

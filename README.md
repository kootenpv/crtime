## crtime

[![Build Status](https://travis-ci.org/kootenpv/crtime.svg?branch=master)](https://travis-ci.org/kootenpv/crtime)
[![PyPI](https://img.shields.io/pypi/v/crtime.svg?style=flat-square)](https://pypi.python.org/pypi/crtime/)
[![PyPI](https://img.shields.io/pypi/pyversions/crtime.svg?style=flat-square)](https://pypi.python.org/pypi/crtime/)

Get creation time of files for any platform and no external dependencies.

### Caveat

Linux requires sudo! There is no way to avoid this, as creation time is not exposed by the kernel.

It uses debugfs to mount the filesystem, as the information is actually contained on most linux platforms.

Speed: because it does one query for a whole directory, it is roughly 1000x faster than any other method (such as the `xstat` utility that can be found online).

### Installation

    pip install crtime

### Usage

In a shell:

```bash
crtime .
# 1552938709\tfile_a.py
```

In Python

```python
from crtime import get_ctimes_in_dir

for fname, date in get_ctimes_in_dir(".", raise_on_error=True, as_epoch=False):
    print(fname, date)
# file_a.py Mon Mar 18 20:51:18 CET 2019
```

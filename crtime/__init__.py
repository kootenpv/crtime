""" Main file for crtime """

__project__ = "crtime"
__version__ = "0.0.2"
__repo__ = "https://github.com/kootenpv/crtime"

import time
import os
import sys
import subprocess
import tempfile
import platform

system = platform.system()
if system == "Linux" and not os.environ.get("SUDO_USER"):
    raise ValueError("Should be run as sudo user on linux")


def get_device(fname):
    df = subprocess.Popen(["df", fname], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, _, _, _, _, _ = output.decode("utf8").split("\n")[1].split()
    return device


def parse_output(output, as_epoch):
    fname = None
    results = {}
    for line in output.split("\n"):
        if line.startswith("debugfs: stat"):
            fname = line[14:]
        elif line.startswith("crtime:"):
            crtime = line.split("-- ")[1]
            if as_epoch:
                crtime = int(time.mktime(time.strptime(crtime)))
            results[fname.strip('"')] = crtime
    return results


def get_crtimes(fnames, raise_on_error=True, as_epoch=False):
    if system != "Linux":
        return [(fname, os.stat(fname).st_birthtime) for fname in fnames]

    with tempfile.NamedTemporaryFile() as f:
        f.write(("\n".join('stat "' + x + '"' for x in fnames) + "\n").encode())
        f.flush()
        cmd = ["debugfs", "-f", f.name, get_device(fnames[0])]
        with open(os.devnull, 'w') as devnull:
            output = subprocess.check_output(cmd, stderr=devnull)
        results = parse_output(output.decode("utf8"), as_epoch)
    if raise_on_error:
        for fname in fnames:
            if fname in results:
                continue
            raise ValueError('filename "{}" does not have a crtime'.format(fname))
    return [(fname, results.get(fname)) for fname in fnames]


def get_crtimes_in_dir(directory, raise_on_error=True, as_epoch=False):
    if not directory.endswith("/"):
        directory = directory + "/"
    return get_crtimes([directory + x for x in os.listdir(directory)], raise_on_error, as_epoch)


def format_results(results):
    return "\n".join(sorted("{}\t{}".format(v, k) for k, v in results))


def main():
    base = os.path.abspath(sys.argv[-1])
    print(format_results(get_crtimes_in_dir(base, as_epoch=True, raise_on_error=False)))


if __name__ == "__main__":
    main()

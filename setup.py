"""Setup file for netbox-tunnels plugin.

(c) 2020 Justin Drew
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import codecs
import os.path

from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

def get_min_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="netbox-tunnels2",
    version=get_min_version('netbox_tunnels2/version.py'),
    description="A plugin for NetBox to support documentation of network tunneling protocols, ie IPsec, GRE, L2TP, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robertlynch3/netbox-tunnels2",
    author="Robert Lynch",
    license="Apache v2.0",
    package_data={"": ["LICENSE"],},
    install_requires=[],
    min_version=get_min_version('netbox_tunnels2/version.py'),
    packages=find_packages(),
    include_package_data=True,
)

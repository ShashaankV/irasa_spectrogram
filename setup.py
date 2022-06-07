#! /usr/bin/env python


DESCRIPTION = "IRASA spectrogram"
LONG_DESCRIPTION = """
IRASA spectrogram
"""

DISTNAME = 'irasa_spectrogram'
MAINTAINER = 'Shashaank Vattikuti'
MAINTAINER_EMAIL = 'svattikuti@cittatech.org'
URL = 'https://github.com/ShashaankV/irasa_spectrogram/'
DOWNLOAD_URL = 'https://github.com/ShashaankV/irasa_spectrogram/'
VERSION = '0.1.0'

INSTALL_REQUIRES = [
'intervaltree==3.1.0',
'matplotlib==3.3.4',
'mne==0.22.0',
'numpy',
'pandas==1.2.1',
'scipy==1.6.0',
'tqdm==4.56.0']

PACKAGES = [
    'irasa',
]


try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=INSTALL_REQUIRES,
          include_package_data=True,
          packages=PACKAGES,
          package_dir = {'': 'code'}
        )
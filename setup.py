#! /usr/bin/env python


DESCRIPTION = "IRASA spectrogram"
LONG_DESCRIPTION = """
IRASA spectrogram
"""

DISTNAME = 'irasa_spectrogram'
MAINTAINER = 'Shashaank Vattikuti'
MAINTAINER_EMAIL = 'svattikuti@cittatech.org'
URL = 'https://github.com/ShashaankV/irasa_spectrogram/'
# LICENSE = ('LICENSE.txt',)
DOWNLOAD_URL = 'https://github.com/ShashaankV/irasa_spectrogram/'
VERSION = '0.1.0'
# PACKAGE_DATA = {'yasa.data.icons': ['*.svg']}

INSTALL_REQUIRES = ['intervaltree==3.1.0',
'matplotlib==3.3.4',
'mne==0.22.0',
'numpy',
'pandas==1.2.1',
'plotly==4.9.0',
'scipy==1.6.0',
'seaborn==0.11.1',
'statsmodels==0.12.2',
'tqdm==4.56.0']

PACKAGES = [
    'irasa',
]

# CLASSIFIERS = [
#     'Intended Audience :: Science/Research',
#     'Programming Language :: Python :: 3.7',
#     'Programming Language :: Python :: 3.8',
#     'Programming Language :: Python :: 3.9',
#     'License :: OSI Approved :: BSD License',
#     'Operating System :: POSIX',
#     'Operating System :: Unix',
#     'Operating System :: MacOS'
# ]

# from setuptools.command.egg_info import egg_info


# class egg_info_ex(egg_info):
#     """Includes license file into `.egg-info` folder."""

#     def run(self):
#         # don't duplicate license into `.egg-info` when building a distribution
#         if not self.distribution.have_run.get('install', True):
#             # `install` command is in progress, copy license
#             self.mkpath(self.egg_info)
#             self.copy_file('LICENSE.txt', self.egg_info)

#         egg_info.run(self)



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
        #   license = LICENSE,
        #   cmdclass = {'egg_info': egg_info_ex},
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=INSTALL_REQUIRES,
          include_package_data=True,
          packages=PACKAGES,
          package_dir = {'': 'code'}
        #   package_data=PACKAGE_DATA,
        #   classifiers=CLASSIFIERS,
          )
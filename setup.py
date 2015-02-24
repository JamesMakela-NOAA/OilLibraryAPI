""" Setup file.
"""
import os
import shutil
import fnmatch

from setuptools import setup, find_packages
from distutils.command.clean import clean

# could run setup from anywhere
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

requires = ['cornice',
            'waitress',
            'WebTest',
            'webhelpers2>=2.0b5',
            'pyramid_debugtoolbar',
            'pyramid_tm',
            'PasteScript']


class cleandev(clean):
    description = 'cleans files generated by develop mode'

    def run(self):
        # call base class clean
        clean.run(self)

        # clean auto-generated files
        paths = [os.path.join(here, 'oil_library_api'),
                 ]
        file_patterns = ['*.pyc']

        for path in paths:
            for pattern in file_patterns:
                file_list = [os.path.join(dirpath, f)
                             for dirpath, dirnames, files in os.walk(path)
                             for f in fnmatch.filter(files, pattern)]

                for f in file_list:
                    try:
                        os.remove(f)
                        print "Deleted auto-generated file: {0}".format(f)
                    except OSError as err:
                        print ("Failed to remove {0}. Error: {1}"
                               .format(f, err))

        rm_dir = ['oil_library_api.egg-info']
        for dir_ in rm_dir:
            try:
                shutil.rmtree(dir_)
                print "Deleted auto-generated directory: {0}".format(dir_)
            except OSError as err:
                if err.errno != 2:
                    # we report everything except file not found.
                    print ("Failed to remove {0}. Error: {1}"
                           .format(dir_, err))


setup(name='oil_library_api',
      version=0.1,
      description='OilLibraryAPI',
      long_description=README,
      classifiers=["Programming Language :: Python",
                   "Framework :: Pylons",
                   "Topic :: Internet :: WWW/HTTP",
                   "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
                   ],
      keywords="adios gnome oilspill weathering trajectory modeling",
      author='ADIOS/GNOME team at NOAA ORR',
      author_email='orr.gnome@noaa.gov',
      url='',
      cmdclass={'cleandev': cleandev,
                },
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points=('[paste.app_factory]\n'
                    '  main = oil_library_api:main\n'
                    '[console_scripts]\n'
                    '  export_oil_library = oil_library_api.scripts.reports:export\n'
                    '  audit_oil_library = oil_library_api.scripts.reports:audit\n'
                    '  audit_oil_cuts = oil_library_api.scripts.reports:audit_cuts\n'
                    '  score_oils = oil_library_api.scripts.reports:score_oils\n'
                    '  plot_oil_viscosity = oil_library_api.scripts.plot_oil_viscosity:main\n'
                    ),
      paster_plugins=['pyramid'],
      )

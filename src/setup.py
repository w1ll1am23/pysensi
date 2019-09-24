from setuptools import setup, find_packages

setup(name='pysensi',
      version='0.0.1',
      description='Interface api.nilu.no',
      url='http://github.com/w1ll1am23/pysensi',
      author='William Scanlon',
      license='MIT',
      install_requires=['requests>=2.0'],
      tests_require=['mock'],
      test_suite='tests',
      packages=find_packages(exclude=["dist", "*.test", "*.test.*", "test.*", "test"]),
      zip_safe=True)

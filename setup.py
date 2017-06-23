try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    
def readme():
    with open('README.rst') as file:
        return file.read()
        
setup(name='Frequency-meter-APP',
      version='0.1.0-alpha',
      description='UVigo Frequency-meter software application',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering'
      ],
      url='',
      author='Javier Lopez Randulfe',
      author_email='javier.randulfe@uvigo.es',
      data_files = [("", ["LICENSE"])],
      packages=find_packages(exclude=['docs', 'tests*']),
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False
      )

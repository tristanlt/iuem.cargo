from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='iuem.cargo',
      version=version,
      description="Configuration specific pour Cargo",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Tristan Le Toullec',
      author_email='tristan.letoullec@univ-brest.fr',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['iuem'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.dexterity',
          'collective.autopermission',
          'collective.geo.bundle',
          'collective.wtf',
          'collective.geo.behaviour',
          'collective.dexteritytextindexer'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )

from setuptools import setup
setup(
name='CloudByte',
version='1.0',
py_modules=['cb'],
install_requires=[
	'Click',
],
entry_points='''
	[console_scripts]
	cb=cb:display
''',
)


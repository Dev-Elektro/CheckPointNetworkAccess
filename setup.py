from setuptools import setup

setup(
    name='CheckPointNetworkAccess',
    version='0.1',
    packages=['CheckPointNetworkAccess'],
    url='https://github.com/Dev-Elektro/CheckPointNetworkAccess',
    license='MIT license',
    author='Dev-Elektro',
    author_email='elektro.linux@gmail.com',
    description='Dev-Elektro',

    install_requires=[
        'setuptools~=60.2.0',
        'pyppeteer~=1.0.2',
        'loguru~=0.6.0',
        'cryptography~=38.0.1'
    ],

    entry_points={
        'console_scripts':
            ['check_point_network_access = CheckPointNetworkAccess.main:main']
    },
    python_requires=">=3.5",
)

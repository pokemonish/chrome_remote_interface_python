import chrome_remote_interface
from distutils.core import setup


setup(
    name='chrome_remote_interface',
    version='0.1',
    description='Client for talking to the Google Chrome remote shell port',
    author='wasiher',
    author_email='watashiwaher@gmail.com',
    url='https://github.com/wasiher/chrome_remote_interface_python',
    packages=['chrome_remote_interface'],
    install_requires=['websockets', 'websocket-client', 'requests'],
)
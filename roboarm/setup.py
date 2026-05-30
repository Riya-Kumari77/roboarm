from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'roboarm'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*')),
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@email.com',
    description='3-DOF Robot Arm',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'arm_controller = roboarm.arm_controller:main',
            'arm_teleop     = roboarm.arm_teleop:main',
        ],
    },
)
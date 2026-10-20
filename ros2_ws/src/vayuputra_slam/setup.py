from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'vayuputra_slam'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Vayuputra Team',
    maintainer_email='maintainers@vayuputra.invalid',
    description='RTAB-Map SLAM and localization integration for the Vayuputra search-and-rescue UAV.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'slam_interface_node = vayuputra_slam.slam_interface_node:main',
        ],
    },
)

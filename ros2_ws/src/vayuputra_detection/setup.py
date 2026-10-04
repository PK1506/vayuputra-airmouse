from setuptools import find_packages, setup

package_name = 'vayuputra_detection'

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
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Vayuputra Team',
    maintainer_email='maintainers@vayuputra.invalid',
    description='Survivor detection ROS 2 integration for the Vayuputra search-and-rescue UAV.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
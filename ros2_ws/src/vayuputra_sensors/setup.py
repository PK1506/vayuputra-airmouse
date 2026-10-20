from setuptools import find_packages, setup

package_name = 'vayuputra_sensors'

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
            'share/' + package_name + '/config',
            ['config/sensor_topics.yaml']
        ),
        (
        'share/' + package_name + '/launch',
        ['launch/sensor_config.launch.py']
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Vayuputra Team',
    maintainer_email='maintainers@vayuputra.invalid',
    description='Sensor ROS 2 integration for LiDAR, IMU, camera and other Vayuputra UAV sensors.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                    'sensor_config_node = vayuputra_sensors.sensor_config_node:main',

        ],
    },
)
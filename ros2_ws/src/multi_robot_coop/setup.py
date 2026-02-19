from setuptools import setup
from setuptools import find_packages
from glob import glob
import os

package_name = 'multi_robot_coop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # ament / package index
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),

        # package.xml
        ('share/' + package_name, ['package.xml']),

        # launch files
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.launch.py')),

        # config files (اگر داری)
        (os.path.join('share', package_name, 'config'),
         glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kishu',
    maintainer_email='mkhodashenas78@gmail.com',
    description='Multi robot cooperation project (TB3 + iiwa)',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tb3_coordinator = multi_robot_coop.tb3_coordinator:main',
            'arm_coordinator = multi_robot_coop.arm_coordinator:main',
            'arm_real_controller = multi_robot_coop.arm_real_controller:main',
            'arm_controller = multi_robot_coop.arm_controller:main',
            'tb3_controller = multi_robot_coop.tb3_controller:main',
            'scenario_coordinator = multi_robot_coop.scenario_coordinator:main',
        ],
    },
)


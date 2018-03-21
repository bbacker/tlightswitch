from setuptools import setup

setup(name='taglightswitch',
        version='0.1',
        description='schedule EC2 instances on/off based on tags',
        long_description="""power EC2 instances on and off on a schedule based
        on AWS tags applied to the instances. see
        https://github.com/bbacker/taglightswitch for more information""",
        url='http://github.com/bbacker/taglightswitch',
        author='Bryan Backer',
        author_email='bryan.backer@gmail.com',
        license='MIT',
        packages=['taglightswitch'],
        scripts=['taglightswitch/check_lightswitches'],
        zip_safe=False)


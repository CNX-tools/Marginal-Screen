from setuptools import setup

APP = ['main.py']  # Replace 'your_main_script.py' with the name of your main Python script
DATA_FILES = []  # Add any additional data files or resources here
OPTIONS = {
    'argv_emulation': True,
    'packages': [],  # Add any additional packages your application depends on
    'iconfile': '/Users/khacanh/Documents/GitHub/Marginal-Screen/assets/quan.ico',  # Replace 'path/to/your/icon.icns' with the path to your application icon
    'plist': {
        'CFBundleShortVersionString': '0.1.0',  # Replace with your application version
        'CFBundleName': 'Marginal Screen'  # Replace with your application name
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
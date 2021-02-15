from setuptools import setup
APP = ['recharge.py']
DATA_FILES = ['renew.png', 'stop-renew.png', 'set_max_charge.sh', 'smcutil']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'renew.icns',
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}
setup(
    app=APP,
    name='ReCharge',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps']
)

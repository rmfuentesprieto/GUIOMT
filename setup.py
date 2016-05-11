from distutils.core import setup

setup(
        name='OMTGUI',
        version='1',
        packages=['omt', 'omt.gui', 'omt.gui.sourcepanel', 'omt.gui.sourcepanel.bla',
                  'omt.gui.sourcepanel.alternatives', 'omt.gui.extract_data_panel',
                  'omt.gui.extract_data_panel.alternatives', 'omt.gui.data_processing_panel',
                  'omt.gui.data_processing_panel.alternatives'],
        url='',
        license='',
        author='Roberto Fuentes',
        author_email='',
        description='', requires=['kivy']
)

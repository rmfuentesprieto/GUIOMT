from distutils.core import setup

setup(
    name='OMTGUI',
    version='1.0',
    packages=['omt', 'omt.gui', 'omt.gui.util', 'omt.gui.sourcepanel', 'omt.gui.sourcepanel.alternatives',
              'omt.gui.extract_data_panel', 'omt.gui.extract_data_panel.alternatives', 'omt.gui.data_processing_panel',
              'omt.gui.data_processing_panel.alternatives', 'omt.gui.data_processing_panel.alternatives.functions_gui',
              'omt.util', 'omt.controller', 'omt.controller.data', 'omt.controller.source',
              'omt.controller.source.beam_scanner', 'omt.controller.procesing',
              'omt.controller.procesing.dynamic_modules'],
    url='',
    license='',
    author='Roberto Fuentes',
    author_email='amermelao@gmail.com',
    description='', requires=['corr']
)

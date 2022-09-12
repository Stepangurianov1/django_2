#!"c:\users\user\desktop\django 2часть\952_1294_1186\geekshop\venv\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'bookmarks2markdown==1.0.2','console_scripts','bookmarks2markdown'
__requires__ = 'bookmarks2markdown==1.0.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('bookmarks2markdown==1.0.2', 'console_scripts', 'bookmarks2markdown')()
    )

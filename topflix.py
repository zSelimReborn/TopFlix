#from gevent.monkey import patch_all

#patch_all()
#print('Patching all!')

from app import create_app

app = create_app()

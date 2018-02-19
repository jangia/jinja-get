import os

print 'Path to file folder: %s' % os.path.dirname(__file__)
print __file__

print os.path.join(os.path.dirname(__file__), "templates", 'test', 'muha')

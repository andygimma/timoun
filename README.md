Timoun
======

## Open Source Resource Map for Children's Services in Haiti

### Set up your environment
1. Download Google App Engine for Python. https://cloud.google.com/appengine/downloads

2. Clone this repository

    $ cd google_appengine && git clone https://github.com/andygimma/timoun.git
    
3. Test the application

    $ lettuce /tests/features

4. Run the application

    $ python dev_appserver.py timoun
    
    

### Testing
Timoun employs behavioral testing, and uses [lettuce_webdriver](https://pypi.python.org/pypi/lettuce_webdriver). Docs for terrain.py setup can be found [here](http://lettuce.it/reference/terrain.html).

To test the application

    $ lettuce /tests/features
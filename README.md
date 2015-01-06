Timoun
======

## Open Source Resource Map for Children's Services in Haiti

A partnership between Catholic Relief Services, Institut du Bien-Être Social et de Recherches, the Government University Department of Social Work and VisionLink to map projects and services, with a focus on mental health for vulnerable children and their families in Haiti.

### Set up your environment
1. Download Google App Engine for Python. https://cloud.google.com/appengine/downloads

2. Clone this repository

    $ cd google_appengine && git clone https://github.com/andygimma/timoun.git
    
3. Set up virtualenv

    $ pip install virtualenv

    $ virtualenv timoun

    $ source timoun/bin/activate
    
    To deactivate virtualenv
    
    $ deactivate
    
4. Install dependencies from requirements.txt

    $ pip install -r requirements.txt
    
5. Test the application

    $ lettuce /tests/features

6. Run the application

    $ python dev_appserver.py timoun
    
    

### Testing
Timoun employs behavioral testing, and uses [lettuce_webdriver](https://pypi.python.org/pypi/lettuce_webdriver). Docs for terrain.py setup can be found [here](http://lettuce.it/reference/terrain.html).

To test the application

    $ lettuce /tests/features
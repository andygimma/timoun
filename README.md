Timoun
======

## Open Source Resource Map for Children's Services in Haiti

A partnership between Catholic Relief Services (CRS), Institut du Bien-Être Social et de Recherches (IBESR), the Government University Department of Social Work, VisionLink and CrisisCleanup.org to map projects and services, with a focus on mental health for vulnerable children and their families in Haiti. "Timoun" is Haitian Creole for "children."

### Set up your environment
1. Download Google App Engine for Python. https://cloud.google.com/appengine/downloads

    We will be using Python 2.7.

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
    
## Contribute

### Developers

Check out our issues list. If you see something you think you can solve, create a branch in the format Issue-<issue-#>/<description>. When you feel the code is well-written and well-tested, send a pull request.

### Testing

Are you good at making Lettuce tests and want to add more coverage? Create a branch in the format tests/<description>. When you feel the code is well-written, send a pull request.

### Style Guidelines

Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.

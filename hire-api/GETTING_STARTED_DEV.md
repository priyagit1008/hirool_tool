## HIRE-API

### Overview


Strictly adhere to the following versions of the stack:

- Python 3.6
- Postgres 9.6
- Django 2.0.1

---


### Setup your development environment

Below instructions are tailored for the MacOs. Update the **Homebrew** before setting up your environment.


#### Python 3.6

- If you have a different version of python running, unhook it:

    `brew unlink python`

- Install Python 3.6 using the following brew formula:

    `
    brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
    `

- Switch to the installed version:

    `brew switch python 3.6.5_1`

- Install pip:

    `sudo easy_install pip`



### python 3.7.2

wget https://www.python.org/ftp/python/3.7.2/python-3.7.2-macosx10.6.pkg

>>>>>>>>>>install pkg
brew switch python 3.7.2_2
brew link --overwrite python





#### Postgres 9.6

- If you don't have postgres installed or having a different version than specified, remove them by running:

    ```
    brew uninstall --force postgresql
    rm -rf /usr/local/var/postgres
    ```

- install postgres 9.6 using Homebrew:

    ```
    brew install postgresql@9.6
    brew link postgresql@9.6 --force
    ```

- Start the postgres as a service:

    `brew services start postgresql@9.6`


    #### Setting up the db for the project:

    - log on to **psql** console:

        `psql -U <mac_username> -d postgres`

    - Create user 'hire_user' with password 'hire@123'

        `CREATE USER hire_user WITH PASSWORD 'hire@123'`

    - Create the database named 'hire_db'

        `CREATE DATABASE hire_db with owner hire_user`

    #### Caveats

    - Make sure that the psql app & server versions are the same:

        ```
        psql (9.6.10)
        Type "help" for help.
        ```

    - Restart the machine if there's a mismatch between them.


#### Django 2.0.1

- Install *virtualenv* using pip3:

    `pip3 install virtualenv`

- Install *virtualenvwrapper* using pip3:

    `pip3 install virtualenvwrapper`

- Create directory *~/.virtualenvs*

- Configure *virtualenvwrapper* by adding the following code to *~/.bash_profile*:

    ```
    export WORKON_HOME=$HOME/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=($which python3)
    export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
    export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'

    source /usr/local/bin/virtualenvwrapper.sh
    ```

- Source *~/.bash_profile*

- Test if the setup works:

    ```
    mkvirtualenv test
    deactivate
    ```

- Create a virtualenv using the following cmd:

    `mkvirtualenv --python=($which python3) env_name`

- Activate the virtualenv:

    `workon env_name`

    #### Setting up the project

    - After cloning the project, move into the project dir:

        `cd hire-api`

    - Install the specified *django* version and other packages through the requirements.txt:

        `pip install -r requirements/requirements.txt`

    - Use *sudo* incase you bump into the permission issue during *pip install*.

    - Before running the migration, copy api/settings.py.sample > api/settings.py and configure it according to your development setup.

        `cd api && cp api/settings.py.sample api/settings.py`

    - Create the following directory with appropriate permissions:

        `mkdir /var/log/hire_api && sudo chown -R <mac_username>:staff /var/log/hire_api`

    - Run the migration:

        `python manage.py migrate`

    - Start the development server using

        `python manage.py runserver`

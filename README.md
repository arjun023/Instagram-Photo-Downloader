## Instagram Photo Downloader

- It is for downloading your friend's photos and videos with your account.
- Your username and your password won't be stored.
- Whether or not you have two factor authentication in your Instagram account or not, this will still work.
- It uses `Selenium` and two different browsers which are `Chrome` and `PhantomJS`
    - The driver is being asked at the beginning of the program.
    - If you want to see what happens -> use `Chrome`
    - If you want to view the process in the background -> use `PhantomJs`

## Requirements

- Python 3
- Selenium
- PhantomJS
- Chrome Driver for Selenium

## How to install and run

1. Download and install `Python 3.6` into your computer.
	- [Python Download Page](https://www.python.org/downloads/ "Python Download Page")
2. Install `Pip`
	- [Pip Installation Page](https://pip.pypa.io/en/stable/installing/ "Pip Installation Page")
3. Download the source from Github
    - `git clone https://github.com/serhatsnmz/Instagram-Photo-Downloader.git`
    - `cd Instagram-Photo-Downloader`
4. Install requirements
	- `pip install -r requirements.txt`
5. Download and install `PhantomJs` 
    - For Linux
        - Do not use apt-get for downloading PhantomJs!
        - Wget the latest phantomjs (as per [PhatomJs Download Page](http://phantomjs.org/download.html "PhatomJs Download Page"))
            - `wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2`
        - Untar it
            - `tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2`
        - Moved the phantomjs executable to /usr/bin/ (may need sudo)
            - `cp /path/to/phantom/untar/bin/phantomjs /usr/bin/`
    - For Windows
        - Download the `PhantomJS` with link below :
            - [PhatomJs Download Page](http://phantomjs.org/download.html "PhatomJs Download Page")
        - Copy `path\phantomjs-2.1.1-windows\bin\phantomjs.exe` file to `C:\Program Files (x86)\Python36-32\Scripts`
6. Run python file with Python 3
	- `python Instagram_Photo_Donwloader.py`
    
## Config.Json File

This file can be used for saving login data and path for photos. Nothing is saved automatically to here even if you change the file.
- *username* : User's username
- *password* : User's pass
- *path* : The path for saving photos. Default value is `photos`
    - Exp : `path/photos` or `../path/photos`

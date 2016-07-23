# Collector

New upgrade from subdomain scan.This script having new features like find people in linkedin,
find twitter user,resolve host to find any host's ip,etc.My script will be useful for collecting information that's why it being called Collector.

# Note:

Because my script use google search engine so sometime google may ban your ip when you sending request to google it will
response a page which you need enter character to continue that will make script not work.But you don't worry it will work again when your ip not be blocked

## Usage:

    USAGE: ./collector -d [domain] [OPTIONS]                                                                    
                                                                                                            
       _|_|_|            _|  _|                        _|                                                   
     _|          _|_|    _|  _|    _|_|      _|_|_|  _|_|_|_|    _|_|    _|  _|_|  
     _|        _|    _|  _|  _|  _|_|_|_|  _|          _|      _|    _|  _|_|      
     _|        _|    _|  _|  _|  _|        _|          _|      _|    _|  _|        
      |_|_|_|    _|_|    _|  _|    _|_|_|    _|_|_|      _|_|    _|_|    _|

    Author: ___T7hM1___
    Github: http://github.com/t7hm1
    Version:2.0
    Collector python scipt which useful to collector information.It made for information gathering

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit

    options:

    -d <domain>           Specify target domain,it look like google.com
    -f <file>, --file <file>
                        Optional to choose default wordlist or custom wordlist
    --subscan             Enable subdomain scan
    --resolver            Resolve host name
    --lookup              Lookup Domain
    --whois               Whois your target
    --gemail              Enable emails searcher
    --gtwitter            Enable twitter searcher
    --linkedin            Enable search people in linkedin
    --getheader           Get a few information with headers

    Example:
      ./collector -d example.com --getheader
      ./collector -d google.com --subscan
      ./collector -d apple.com --gemail
      

# Collector

* version 2.7 :

       add stealth scan,xmas scan,fin scan,ack scan and udp scan
       Upgrade some new feature

New upgrade from subdomain scan.This script having new features like find people in linkedin,
find twitter user,resolve host to find any host's ip,etc.My script will be useful for collecting information that's why it being called Collector.


# Note:

Because my script use google search engine so sometime google may ban your ip when you sending request to google it will
response a page which you need enter character to continue that will make script not work.But you don't worry it will work again when your ip not be blocked

## Usage:
        ******            **  **                   **
       **////**          /** /**                  /**
      **    //   ******  /** /**  *****   *****  ******  ******  ******
     /**        **////** /** /** **///** **///**///**/  **////**//**//*
     /**       /**   /** /** /**/*******/**  //   /**  /**   /** /** /
     //**    **/**   /** /** /**/**//// /**   **  /**  /**   /** /**
      //****** //******  *** ***//******//*****   //** //****** /***
       //////   //////  /// ///  //////  /////     //   //////  ///

                           @teachyourselfhacking

       Author: ___T7hM1___
       Github: http://github.com/t7hm1
       Version:3.0

                Scanning -=- Gathering -=- Collecting


       usage: ./collector.py -d [domain] [OPTIONS]

       REQUIRES:
              -d , --domain      Specify target domain,it look like google.com.
              -i , --ip          Argument for ip pinger.

       OPTIONAL:
              -p , --port        Optional to choose port to traceroute or sS sU scan.
              -f , --file        Optional to choose default wordlist or custom wordlist.
              -s , --srange      Specify start range for ping module (default:0).
              -e , --erange      Specify end range for ping module (default:256).
              -t , --timeout     Set timeout for connectivity (default=0.5).
              -m , --method      Specify method to test.Default is GET method.
              -w , --writefile   Write output to text file.
              -q, --quite        quite.

       WEB CRAWLER:
              --method-test      Test method status of website.
              --scraping-links   Enable web scraping.

       PORT SCAN TECHNIQUES:
              -sC                Use socket connect() to scan ports.
              -sS                TCP SYN.
              -sF                FIN scan.
              -sA                ACK scan.
              -sX                XMAS scan.
              -sN                Null scan.
              -sU                UDP Scan.

       WHOIS/LOOKUP DOMAIN:
              -lookup            Lookup Domain.
              -whois             Whois your target.
              -subscan           Enable subdomain scan.
              --zone             Check DNS zone transfer.

       SNSE:
              -EH                Start email hunter.
              -snse              Search user on social network such like 
                     linkedin,twitter,googleplus(gplus).

       NETWORK GATHERING:
              -ping              Enable ping check alive ip.
              -getheader         Get a few information with headers.
              -traceroute        Traceroute your target.

       HELP SCREEN:
              -h, --help         Print help screen and exit.
              -v, --version      Print program's version and exit.

       Example:
              ./collector.py -i 192.168.1 -s 10 -e 100
              ./collector.py -d example.com -getheader
              ./collector.py -d google.com -subscan -f /path/to/worldlist
              ./collector.py -d apple.com -gemail -linkedin
              ./collector.py -d google.com -p 1-500 -sS


# Collector

* version 3.0 :

      [+] Add pass same host in Subscan.
      
      [+] Add feature links extractor.
      
      [+] Upgrade pyWhois
      
            * add subdomain handler.
            
            * add 4 network whois server.
            
            * also use correct domain whois server.
      
      
# Required Modules

* When you run this tool it will detect required modules and install it.

# Note

* My Scanner (except TCP Connect Scan) won't work in Arch,Debain and may Fedora.

* Also Email Hunter may not work in some linux platform.

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


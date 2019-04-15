<div align="center">
    <a href="https://php.net">
        <img src="https://www.seasiainfotech.com/blog/wp-content/uploads/2016/09/php7.jpg" width="800">
    </a>
</div>

# System Information
    $ uname -a
    Linux ovz-junhua-zhang 2.6.32-042stab120.19 #1 SMP Mon Feb 20 20:05:53 MSK 2017 x86_64 x86_64 x86_64 GNU/Linux
    $ cat /etc/centos-release
    CentOS release 6.8 (Final)
     
    $ ldd --version
    ldd (GNU libc) 2.12
    Copyright (C) 2010 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Written by Roland McGrath and Ulrich Drepper.

# Yum Information
    $ rpm -vh 'http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm'

    $ yum repolist -v
    Loading "fastestmirror" plugin
    Config time: 0.017
    Yum Version: 3.2.29
    Loading mirror speeds from cached hostfile
     * base: mirrors.aliyun.com
     * epel: mirrors.aliyun.com
     * extras: mirrors.aliyun.com
     * updates: mirrors.aliyun.com
    Setting up Package Sacks
    pkgsack time: 0.027
    Repo-id      : base
    Repo-name    : CentOS-6 - Base - mirrors.aliyun.com
    Repo-revision: 1530286202
    Repo-updated : Fri Jun 29 23:37:23 2018
    Repo-pkgs    : 6,713
    Repo-size    : 5.5 G
    Repo-baseurl : http://mirrors.aliyun.com/centos/6/os/x86_64/, http://mirrors.aliyuncs.com/centos/6/os/x86_64/, http://mirrors.cloud.aliyuncs.com/centos/6/os/x86_64/
    Repo-expire  : 21,600 second(s) (last: Thu Apr 11 18:20:25 2019)
    
    Repo-id      : epel
    Repo-name    : Extra Packages for Enterprise Linux 6 - x86_64
    Repo-revision: 1554880898
    Repo-updated : Wed Apr 10 15:41:46 2019
    Repo-pkgs    : 12,522
    Repo-size    : 11 G
    Repo-metalink: https://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=x86_64
      Updated    : Wed Apr 10 15:41:46 2019
    Repo-baseurl : http://mirrors.aliyun.com/epel/6/x86_64/ (21 more)
    Repo-expire  : 21,600 second(s) (last: Thu Apr 11 18:20:27 2019)
    
    Repo-id      : extras
    Repo-name    : CentOS-6 - Extras - mirrors.aliyun.com
    Repo-revision: 1554122385
    Repo-updated : Mon Apr  1 20:39:45 2019
    Repo-pkgs    : 46
    Repo-size    : 13 M
    Repo-baseurl : http://mirrors.aliyun.com/centos/6/extras/x86_64/, http://mirrors.aliyuncs.com/centos/6/extras/x86_64/, http://mirrors.cloud.aliyuncs.com/centos/6/extras/x86_64/
    Repo-expire  : 21,600 second(s) (last: Thu Apr 11 18:20:33 2019)
    
    Repo-id      : updates
    Repo-name    : CentOS-6 - Updates - mirrors.aliyun.com
    Repo-revision: 1554840057
    Repo-updated : Wed Apr 10 04:06:00 2019
    Repo-pkgs    : 421
    Repo-size    : 5.4 G
    Repo-baseurl : http://mirrors.aliyun.com/centos/6/updates/x86_64/, http://mirrors.aliyuncs.com/centos/6/updates/x86_64/, http://mirrors.cloud.aliyuncs.com/centos/6/updates/x86_64/
    Repo-expire  : 21,600 second(s) (last: Thu Apr 11 18:20:33 2019)

# Fetch php-7.3.3 source
    $ git clone -b PHP-7.3.3 https://github.com/php/php-src.git php-7.3.3
    ...
    fatal: Out of memory, malloc failed (tried to allocate 31476624 bytes)
## resolved: 
    增加CTID(OpenVZ)内存: 
    $ vzctl set 114 --ram 2048M --swap 16M --save

# ./buildconf --force
    Forcing buildconf
    Removing configure caches
    buildconf: checking installation...
    buildconf: autoconf not found.
           You need autoconf version 2.68 or newer installed
           to build PHP from Git.
    make: *** [buildmk.stamp] Error 1
## resolved
    $ sudo yum install autoconf automake
    ./buildconf --force
    Forcing buildconf
    Removing configure caches

    OR:
    $ wget http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz
    $ tar xvf autoconf-2.69.tar.gz
    $ cd autoconf-2.69
    $ ./configure --prefix=/usr
    $ make && sudo make install

    $ wget http://ftp.gnu.org/gnu/automake/automake-1.14.tar.gz
    $ tar xvf automake-1.14.tar.gz
    $ cd automake-1.14
    $ ./configure --prefix=/usr
    $ make && sudo make install

# ./configure
    $ './configure' '--prefix=/usr/local/php7.3' \
    '--disable-ipv6' \
    '--enable-calendar' \
    '--enable-ctype' \
    '--enable-dom' \
    '--enable-exif' \
    '--enable-fileinfo' \
    '--enable-filter' \
    '--enable-gd-native-ttf' \
    '--enable-hash' \
    '--enable-json' \
    '--enable-libxml' \
    '--enable-mbstring' \
    '--enable-opcache' \
    '--enable-pcntl' \
    '--enable-pdo' \
    '--enable-posix' \
    '--enable-session' \
    '--enable-simplexml' \
    '--enable-soap' \
    '--enable-tokenizer' \
    '--enable-xml' \
    '--enable-xmlreader' \
    '--enable-xmlwriter' \
    '--enable-zip' \
    '--with-apxs2=/usr/local/apache2/bin/apxs' \
    '--with-bz2' \
    '--with-curl' \
    '--with-freetype-dir' \
    '--with-gd' \
    '--with-iconv' \
    '--with-jpeg-dir' \
    '--with-webp-dir=/etc/libwebp' \
    '--with-mcrypt' \
    '--with-mysql=mysqlnd' \
    '--with-openssl' \
    '--with-pdo-mysql=mysqlnd' \
    '--with-pdo-odbc=unixODBC,/usr/local/unixODBC' \
    '--with-png-dir' \
    '--with-readline' \
    '--with-zlib' \
    '--disable-all'
# Compile failure: bison invalid
    ...
    checking for bison version... invalid
    configure: WARNING: This bison version is not supported for regeneration of the Zend/PHP parsers (found: none, min: 204, excluded: ).
    checking for re2c... no
    configure: WARNING: You will need re2c 0.13.4 or later if you want to regenerate PHP parsers.
    configure: error: bison is required to build PHP/Zend when building a GIT checkout!
## resloved: install bison from source
    $ wget http://ftp.gnu.org/gnu/bison/bison-2.5.1.tar.gz
    $ tar xvf bison-2.5.1.tar.gz
    $ cd bison-2.5.1
    $ ./configure --prefix=/usr
    $ make && sudo make install
# Compile failed: libxml2
    configure: error: libxml2 not found. Please check your libxml2 installation.
## resolved: 
    $ yum list installed|grep libxml2-devel
    $ sudo yum install libxml2-devel
# Compile failed: openssl
    ...
    checking whether to use system default cipher list instead of hardcoded value... no
    checking for RAND_egd... no
    checking for pkg-config... /usr/bin/pkg-config
    configure: error: Cannot find OpenSSL's <evp.h>
## resolved:
    $ yum list installed|grep openssl
    $ sudo yum install openssl-devel
# Compile failed: bzip2
    ...
    checking for BZip2 in default path... not found
    configure: error: Please reinstall the BZip2 distribution
## resolved:
    $ sudo yum install bzip2-devel
# Compile failed: curl
    ...
    checking for cURL 7.15.5 or greater... configure: error: cURL version 7.15.5 or later is required to compile php with cURL support
## resolved:
    $ yum list installed|grep curl
    curl.x86_64                     7.19.7-52.el6                    @base          
    libcurl.x86_64                  7.19.7-52.el6                    @base          
    python-pycurl.x86_64            7.19.0-9.el6                     @base          

    curl已经安装过了，需安装curl-devel包
    $ sudo yum install curl-devel
# Compile failed: webp
    ...
    checking for WebPGetInfo in -lwebp... yes
    checking for jpeg_read_header in -ljpeg... yes
    configure: error: png.h not found.
    ...
    configure: error: webp/decode.h not found.
    ...
    configure: error: jpeglib.h not found.
    ...
    configure: error: png.h not found.
    ...
    configure: error: freetype-config not found.
## resolved:
    $ sudo yum install -y libpng libpng-devel

    检查webp/decode.h头文件的提供者
    $ yum provides '*/webp/decode.h'
    ...
    libwebp-devel-0.4.3-3.el6.x86_64 : Development files for libwebp, a library for the WebP format
    Repo        : epel
    Matched from:
    Filename    : /usr/include/webp/decode.h

    进而安装 libwebp-devel
    $ sudo yum install libwebp-devel

    $ sudo yum install libjpeg-turbo-devel

    $ sudo yum install libpng-devel

    $ yum list installed|grep freetype
    freetype.x86_64                 2.3.11-17.el6                    @base

    $ sudo yum install freetype-devel
# Compile failure
    checking for PSPELL support... no
    checking for libedit readline replacement... no
    checking for readline support... yes
    configure: error: Please reinstall readline - I cannot find readline.h
## resolved
    $ sudo yum install libedit-devel readline-devel
# Compile failure
    checking libzip... yes
    checking for the location of zlib... /usr
    checking for pkg-config... (cached) /usr/bin/pkg-config
    checking for libzip... not found
    configure: error: Please reinstall the libzip distribution
## resolved
    $ sudo yum install libzip-devel
# Compile failure
    checking libzip... yes
    checking for the location of zlib... /usr
    checking for pkg-config... (cached) /usr/bin/pkg-config
    checking for libzip... configure: error: system libzip must be upgraded to version >= 0.11
## resolve
    $ wget http://rpms.remirepo.net/enterprise/6/remi/x86_64//libzip-last-1.1.3-1.el6.remi.x86_64.rpm
    $ rpm -Uvh libzip-last-1.1.3-1.el6.remi.x86_64.rpm

    $ wget http://rpms.remirepo.net/enterprise/6/remi/x86_64//libzip-last-devel-1.1.3-1.el6.remi.x86_64.rpm
    $ sudo rpm -Uvh libzip-last-devel-1.1.3-1.el6.remi.x86_64.rpm
### error
    libzip-devel < 1.1.3 conflicts with libzip-last-devel-1.1.3-1.el6.remi.x86_6
### resolve
    $ sudo yum remove libzip -y
    $ sudo rpm -Uvh libzip-last-devel-1.1.3-1.el6.remi.x86_64.rpm

# Compile successed with a WARNING
    configure: WARNING: unrecognized options: --enable-gd-native-ttf, --with-mcrypt, --with-mysql

# make
## make failure
    /etc/libwebp/lib/libwebp.a: could not read symbols: Bad value
    collect2: ld returned 1 exit status
    make: *** [libphp7.la] Error 1
    make: *** Waiting for unfinished jobs....
## resolved
    remove '--with-webp-dir=/etc/libwebp'

# make test
    =====================================================================
    FAILED TEST SUMMARY
    ---------------------------------------------------------------------
    Bug #64267 (CURLOPT_INFILE doesn't allow reset) [ext/curl/tests/bug64267.phpt]
    Bug #71523 (Copied handle with new option CURLOPT_HTTPHEADER crashes while curl_multi_exec) [ext/curl/tests/bug71523.phpt]
    PDO ODBC varying character with max/no length [ext/pdo_odbc/tests/max_columns.phpt]
    Bug #76348 (WSDL_CACHE_MEMORY causes Segmentation fault) [ext/soap/tests/bugs/bug76348.phpt]
    Bug #74090 stream_get_contents maxlength>-1 returns empty string on windows [ext/standard/tests/streams/bug74090.phpt]
    int stream_socket_sendto ( resource $socket , string $data [, int $flags = 0 [, string $address ]] ); [ext/standard/tests/streams/stream_socket_sendto.phpt]

# make install
    Installing PHP SAPI module:       apache2handler
    /usr/local/apache2//build/instdso.sh SH_LIBTOOL='/usr/local/apache2//build/libtool' libphp7.la /usr/local/apache2//modules
    /usr/local/apache2//build/libtool --mode=install cp libphp7.la /usr/local/apache2//modules/
    cp .libs/libphp7.so /usr/local/apache2//modules/libphp7.so
    cp .libs/libphp7.lai /usr/local/apache2//modules/libphp7.la
    libtool: install: warning: remember to run `libtool --finish /opt/php-7.3.3/libs'
    chmod 755 /usr/local/apache2//modules/libphp7.so
    [activating module `php7' in /usr/local/apache2//conf/httpd.conf]
    Installing shared extensions:     /usr/local/php7.3/lib/php/extensions/no-debug-non-zts-20180731/
    Installing PHP CLI binary:        /usr/local/php7.3/bin/
    Installing PHP CLI man page:      /usr/local/php7.3/php/man/man1/
    Installing phpdbg binary:         /usr/local/php7.3/bin/
    Installing phpdbg man page:       /usr/local/php7.3/php/man/man1/
    Installing PHP CGI binary:        /usr/local/php7.3/bin/
    Installing PHP CGI man page:      /usr/local/php7.3/php/man/man1/
    Installing build environment:     /usr/local/php7.3/lib/php/build/
    Installing header files:          /usr/local/php7.3/include/php/
    Installing helper programs:       /usr/local/php7.3/bin/
      program: phpize
      program: php-config
    Installing man pages:             /usr/local/php7.3/php/man/man1/
      page: phpize.1
      page: php-config.1

# test php7
    $ /usr/local/php7.3/bin/php -v
    PHP 7.3.3 (cli) (built: Apr  4 2019 17:38:55) ( NTS )
    Copyright (c) 1997-2018 The PHP Group
    Zend Engine v3.3.3, Copyright (c) 1998-2018 Zend Technologies

# config php.init & apache2handler
    $ sudo cp /opt/php-7.3.3/php.ini-* /usr/local/php7.3/lib
    $ sudo mv php.ini-development php.ini

    Listen 80
    LoadModule php7_module        modules/libphp7.so
    #LoadModule php5_module        modules/libphp5.so

    $ /usr/local/apache2//bin/httpd -k restart

# test apache2handler
    $ vi info.php
    <?php
        phpinfo();

# environment 
    $ vi /usr/bin/php7
    #! /bin/bash
    export PATH="/usr/local/php7.3/bin:$PATH"
    php "$@"
    $ chmod +x /usr/bin/php7 


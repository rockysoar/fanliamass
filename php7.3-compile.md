# ./buildconf
    ./buildconf --force
    Forcing buildconf
    Removing configure caches

# ./configure
    './configure' '--prefix=/ usr/local/php7.3' \
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
# Compile failure
    checking for WebPGetInfo in -lwebp... yes
    checking for jpeg_read_header in -ljpeg... yes
    configure: error: png.h not found.
## resolved
    sudo yum install -y libpng libpng-devel
# Compile failure
    checking for PSPELL support... no
    checking for libedit readline replacement... no
    checking for readline support... yes
    configure: error: Please reinstall readline - I cannot find readline.h
## resolved
    sudo yum install libedit-devel readline-devel
# Compile failure
    checking libzip... yes
    checking for the location of zlib... /usr
    checking for pkg-config... (cached) /usr/bin/pkg-config
    checking for libzip... not found
    configure: error: Please reinstall the libzip distribution
## resolved
    sudo yum install libzip-devel
# Compile failure
    checking libzip... yes
    checking for the location of zlib... /usr
    checking for pkg-config... (cached) /usr/bin/pkg-config
    checking for libzip... configure: error: system libzip must be upgraded to version >= 0.11
## resolve
    wget http://rpms.remirepo.net/enterprise/6/remi/x86_64//libzip-last-1.1.3-1.el6.remi.x86_64.rpm
    rpm -Uvh libzip-last-1.1.3-1.el6.remi.x86_64.rpm
    
    wget http://rpms.remirepo.net/enterprise/6/remi/x86_64//libzip-last-devel-1.1.3-1.el6.remi.x86_64.rpm
    sudo rpm -Uvh libzip-last-devel-1.1.3-1.el6.remi.x86_64.rpm
### error
    libzip-devel < 1.1.3 conflicts with libzip-last-devel-1.1.3-1.el6.remi.x86_6
### resolve
    sudo yum remove libzip -y
    sudo rpm -Uvh libzip-last-devel-1.1.3-1.el6.remi.x86_64.rpm

# Compile Warning
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
    /usr/local/php7.3/bin/php -v
    PHP 7.3.3 (cli) (built: Apr  4 2019 17:38:55) ( NTS )
    Copyright (c) 1997-2018 The PHP Group
    Zend Engine v3.3.3, Copyright (c) 1998-2018 Zend Technologies

# copy php.ini
    sudo cp /opt/php-7.3.3/php.ini-* /usr/local/php7.3/lib
    sudo mv php.ini-development php.ini

# config apache2handler
    Listen 80
    LoadModule php7_module        modules/libphp7.so
    #LoadModule php5_module        modules/libphp5.so

    /usr/local/apache2//bin/httpd -k restart

# test apache2handler
    info.php
    <?php
        phpinfo();

# environment 
    vi /etc/profile
    PATH="$PATH:/usr/local/php7.3/bin/:"
    . /etc/profile

# other
     ln -s /usr/local/php7.3/bin/php /usr/bin/php7


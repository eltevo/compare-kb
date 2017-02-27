# Access MSSQL Server running on Windows from linux

## Install prerequisites

    # apt-get install autoconf
    # apt-get install libkrb5-dev
    # apt-get install unixodbc-dev tdsodbc unixodbc libodbc1 odbcinst1debian2
    # apt-get install libiodbc2 libiodbc2-dev iodbc
    # apt-get install libgnutls-dev
    # git clone https://github.com/openssl/openssl

## Build iodbc from source

## Build unixodbc from source

http://www.unixodbc.org/doc/FreeTDS.html

Use -l switch to add system DSN (kerberos will be used to authenticate individual users)

    # odbcinst -i -s -l -f tds.datasource.template

Test with 
    # isql -v future1

## Build freetds from source

    # git clone https://github.com/FreeTDS/freetds.git
    # cd freetds

See INSTALL.GIT

    # libtoolize
    # aclocal
    # acheader
    # autoconf
    # ./autogen.sh
    # ./configure --enable-krb5 --enable-mars --enable-sspi --enable-odbc --enable-msdblib --with-openssl --with-tdsver=7.4 --with-iodbc=../libiodbc-3.52.10
    # ./configure --enable-krb5 --enable-mars --enable-sspi --enable-odbc --enable-msdblib --with-openssl --with-tdsver=7.4 --with-unixodbc=/usr/local
    # make all -j 4
    # make install

Test setup with

    # tsql -C

It should return something like this:

```
Compile-time settings (established with the "configure" script)
                            Version: freetds v1.0rc5
             freetds.conf directory: /usr/local/etc
     MS db-lib source compatibility: yes
        Sybase binary compatibility: no
                      Thread safety: yes
                      iconv library: yes
                        TDS version: 7.4
                              iODBC: no
                           unixodbc: yes
              SSPI "trusted" logins: no
                           Kerberos: yes
                            OpenSSL: yes
                             GnuTLS: no
                               MARS: yes
```

Edit config /usr/local/etc/freetds.conf:

```
[global]
        tds version = 7.4
        connect timeout = 10
[future1]
        host = future1.vo.elte.hu
        port = 1433
        realm = VO.ELTE.HU
        SPN = MSSQLSvc/future1.vo.elte.hu:1433
        tds version = 7.4
```

## Configure SQL Server SPNs in active directory

    PS> setspn -A MSSQLSvc/future1.vo.elte.hu:1433 VO\sqlserver

Do it for each server, then verify with

    PS> setspn -L VO\sqlserver

## Test connection

    # tsql -S future1

## Configuring ODBC data sources


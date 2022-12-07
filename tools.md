keygen.py
=========

Keys generation for user (.JSON and <WORM>)
-------------------------------------------

params
------

### default
  - show help


### help -h
  - show help


### Create Key
  - user <username> <Keypair count> "coma,separated,tags" [entropy 10]
  - node <Node URL> <tariff> master-user-name "coma,separated,tags"  [entropy 10]


### Change Key
  - change <User Key File> <new keypair index>
    - change current keypair in users key file

node.py
=======

List nodes and information about specific node
----------------------------------------------

params
------

### default
  - list my nodes


### -h help

### <node URL>
  - Select current node from my nodes


### add <node URL>
  - Join remote node and add to My nodes list


### info <node URL>
  - Show info about node

user.py
=======

Different actions with user (userinfo, balance, etc)
----------------------------------------------------

params
------

### default
  - userinfo for current node


### -h help

### out <to address> <coins> <hours>
  - take out funds

master.py
=========

Node management
---------------

params
------

### default
  - show help


### -h help

### info <node URL>
  - Show info about node


### out <node URL> <to address> <coins> <hours>

prng.py
=======

PRNG client
-----------

params
------

### default

### -h help

### -s --seed

### -n --numbers

### -i256

### -h256

pd-dir.py
=========

directory listing
-----------------

params
------

### default
  - show root directory listing


### -h --help

### <dirname>
  - show "dirname" directory listing

pd-upload.py
============

upload file
-----------

params
------

### default
  - show help


### -h --help

### <filename> [remote filepath]

pd-download.py
==============

download file
-------------

params
------

### default
  - show help


### -h --help

### <remote filepath>

pd-move.py
==========

move file to another directory
------------------------------

params
------

### default
  - show help


### -h --help

### <from filepath> <to filepath>

pd-remove.py
============

delete remote file
------------------

params
------

### default
  - show help


### -h --help

### <remote filepath>

pd-info.py
==========

info about file
---------------

params
------

### default
  - show help


### -h --help

### <remote filepath>

pd-sync.py
==========

syncronise selected directory
-----------------------------

params
------

### default
  - show help


### -h --help

### <local dirname>

+++
===
***
===
key.py
======

Actions with keys
-----------------

params
------

### List Keys
  - list {dirpath]
    - List all keys in selected directory or current directory


### Show Key
  - show <keyfile>
    - Show all contents of keyfile

  - nvs <keyfile>
    - show nvs name (for blockchain)

  - worm <keyfile>
    - Show <worm> for blockchain (if there are any)

  - list <keyfile>
    - Show all encrypted keys (if there are any)


### Pack keyfiles into encrypted keyfile
  - pack <keyfile1,keyfile2, ...> <encrypted keyfile>


### Unpack keyfiles from encrypted keyfile
  - unpack <encrypted keyfile>


### Save local keyfiles into encrypted keyfile
  - save <encrypted keyfile>


### Restore local keyfiles from encrypted keyfile
  - restore <encrypted keyfile>


Tasks
-----


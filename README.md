# PrivatenessTools
Privateness console tools
## Key generation
### keygen.py
```
*** PrivateNess KEY GENERATOR
### DESCRIPTION:
  Generates ciphers for NESS service nodes and NESS service node clients
  Works on ed25519 for keypairs
  Adjustable entropy when generating private keys
### USAGE:
#### Generate user
  user <username> <Keypair count> "coma,separated,tags" <Entropy level>
  Example: $ python keygen.py user user1 10 "Hello,World" 5
#### Generate node
  node <Node URL> <Tariff> master-user-name "coma,separated,tags"  <Entropy level>
  Example: $ python keygen.py node http://my-node.net 111 master "Hello,World" 5
#### Change user's keypair
  change <User Key File> <new keypair index>
  Example: $ python keygen.py change user.key.json 2
#### Generate seed
  seed <length> <Entropy level>
  Example: $ python keygen.py seed 32 5
#### Show version
  $ python codegen.py version
  $ python codegen.py -v
#### Show this manual
  $ python codegen.py help
  $ python codegen.py -h
```
## Key management
### key.py
```
*** PrivateNess KEY UTILITY
### DESCRIPTION:
  Privateness keys infrastructure management
### USAGE:
### List Keys
#### Show all contents of keyfile
  list {dirpath]
### Show Key
#### Show all contents of keyfile
 show <keyfile>
#### show nvs name (for blockchain)
 nvs <keyfile>
#### Show <worm> for blockchain (if there are any)
 worm <keyfile>
#### Show all encrypted keys (if there are any)
 list <keyfile>
### Pack keyfiles into encrypted keyfile
 pack <keyfile1,keyfile2, ...> <encrypted keyfile>
### Unpack keyfiles from encrypted keyfile
 unpack <encrypted keyfile>
### Save local keyfiles into encrypted keyfile
 save <encrypted keyfile>
### Restore local keyfiles from encrypted keyfile
 restore <encrypted keyfile>
```
## Node management
### nodes-update.py
```
*** Remote nodes update UTILITY
### DESCRIPTION:
  Service node list update from blockchain or remote node
### USAGE:
#### Update from blockchain (if RPC connection settings olready exist)
 python nodes-update.py blockchain
 python nodes-update.py blk
#### Update from blockchain (connect to Emercoin RPC and save connection settings)
 python nodes-update.py blk rpc-host rpc-port rpc-user rpc-password
#### Update from remote node
 python nodes-update.py node <remote-node-url>
#### Update from remote node (random node fron existing nodes list)
 python nodes-update.py node
#### Auto update (try to update from random node, on error try to update from blockchain
 python nodes-update.py
```
### node.py
```
*** Node manipulation
### USAGE:
#### List all nodes (previously fetched from blockchain or remote node):
 python node.py list
#### Set current node (node name usualy equals node url):
 python node.py set <node-name>
```

## Files management (Privateness DISK)
### TODO ...


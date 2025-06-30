# DICMA (The dictionary maker)

### Dicma creates massive wordlists based on specific words for password cracking.

It includes extracted patterns from rockyou.txt dictionary to "passworize" any specific word or concept. 
Commontly users use a specific word or concept to create their passwords. They modify the concept with simbols, and also they attach numbers and simbols to acomplish the password requirements.
Unfortunatly this behavior coult be predicteble because some of this patterns are used more than others. Dicma extract this patterns from masive dictionaryes and you can even use your specific dicitonary to extract the patterns. All possible combinations are returned for password cracking purpose, using hashcat, john the ripper, or any other software.

```
usage: dicma.py [-h] (-u USERS | -p PASSWORD) [-l] [-f] [-nv] [-d file_name] [-o file_name]

Welcome to DICMA. The Dictionary Maker:

optional arguments:
  -h, --help            show this help message and exit
  -u USERS, --users USERS
                        File with usernames, or usernames list: "jony random,fahim jordan,..."
  -p PASSWORD, --password PASSWORD
                        file with words to "passworize", or list like: "ibis,megacorp,..."
  -l, --light           Light mode, for small list (passwd mode).
  -f, --full            Full mode. Warning, the output could be very heavy (passwd mode).
  -nv, --no-verbose     Remove any output except the dictionary itself (Errors will be shown anyway).
  -d file_name, --dictionary file_name
                        Extract patterns from your specific dictionary
  -o file_name, --output file_name
                        Dictionary will be stored in this file.
```

### USERS mode:

This mode allows you to introduce a list of specific names and surnames from users that you expect to find in an Active directory enviroment and creates a list of all possible combinations based on the most used metods from IT departments.
The input can be a file, containing names and surnames (one per line) or an string like "john kenedy, albert random, patrick harper, ...". The output cand be printed on termianl or stored in a file with `-o` flag.

Example: The user "John Kenedy" will be processed like:

`python3 dicma.py -u "john kenedy"`

`python3 dicma.py -u usernames.txt -o possible_users.txt`
```
johnkenedy
john.kenedy
j_kenedy
john-k
...
```


### PASSWORD mode:

This is the main mode of this tool, and can generate a massive list of possible password based on specific words or concetps. You can introduce this words from a text file (one per line) or a list like "hotel, ibis, corporate, ...". Output can be printed throug terminal or (more recomended) stored in a file with `-o` flag.

Example: word "hotel" will be processed like:

`python3 dicma.py -p "hotel"`

`python3 dicma.py -p words.txt -o dictionary.txt`
```
hotel
Hotel
HOTEL
hotel1
...
!H0TEL2024
h0tel123!
...
```

`--dictionary` flag allows you to specify specific dicionary from wich you want to extract the patterns. By default, will use internaly stored patterns extracted from a famous dictionary (rockyou.txt)

`python3 dicma.py -p words.txt -o dictionary.txt -d rockyou.txt`

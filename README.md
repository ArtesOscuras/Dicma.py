# DICMA (The dictionary maker)

### Dicma creates massive wordlists based on specific words for password cracking.

It includes extracted patterns from the rockyou.txt dictionary to "passworize" any specific word or concept.
Users often create passwords based on specific words or concepts. They modify these with symbols, numbers, and capitalization to meet password requirements.

Unfortunately, this behavior can be predictable, as some patterns are more commonly used than others. Dicma extracts these patterns from massive dictionaries, and you can even use your own custom dictionary to extract patterns. All possible combinations are returned for password cracking purposes using tools like Hashcat, John the Ripper, or others.

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

This mode allows you to input a list of usernames and surnames (e.g., from an Active Directory environment) and generates a list of possible combinations based on commonly used naming patterns in IT departments.

Input can be a file (one name per line) or a string like "john kenedy, albert random, patrick harper, ...".
The output can be printed to the terminal or saved to a file using the `-o` flag.

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

This is the main mode of the tool and can generate a massive list of possible passwords based on specific words or concepts. You can provide these words via a text file (one per line) or a list like "hotel, ibis, corporate, ...".
The output can be shown in the terminal or (recommended) saved to a file with the `-o` flag.

Example: The word "hotel" will be processed like:

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

<br>

Use the `--dictionary` flag to specify a custom dictionary to extract patterns from.
By default, Dicma uses internal patterns extracted from the famous rockyou.txt dictionary.

`python3 dicma.py -p words.txt -o dictionary.txt -d rockyou.txt`

<br>

The `-l` flag enables LIGHT mode, which produces a shorter dictionary output (5,000–10,000 lines x word). 

`python3 dicma.py -p words.txt -o dictionary.txt -l`

<br>

The `-f` flag enables FULL mode, which generates a massive dictionary output (~5,000,000 lines x word).

`python3 dicma.py -p words.txt -o dictionary.txt -l`

<br>

The `-nv` flag disables verbose output and only prints the dictionary. Errors will still be displayed.

`python3 dicma.py -p words.txt -vn > dictionary.txt`

<br>

Massive mode: this is triggered automatically when Dicma detects a large input. It will display progress information and estimated output size.
In massive mode, an output file is required. If you don’t specify one with the -o flag, Dicma will default to saving it in `./output.txt`.

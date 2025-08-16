# DICMA (The dictionary maker)

### Dicma creates massive wordlists based on specific words for password cracking.

It includes extracted patterns from the rockyou.txt dictionary to "passworize" any specific word or concept.
Users often create passwords based on specific words or concepts. They modify these with symbols, numbers, and capitalization to meet password requirements.

Unfortunately, this behavior can be predictable, as some patterns are more commonly used than others. Dicma extracts these patterns from massive dictionaries, and you can even use your own custom dictionary to extract patterns. All possible combinations are returned for password cracking purposes using tools like Hashcat, John the Ripper, or others.

```
usage: dicma.py [-h] (-u USERS | -p PASSWORD) [-l] [-f] [-nv] [-d file_name] [-o file_name] [-ml file_name]
                [-n integer]

Welcome to DICMA. The Dictionary Maker:

options:
  -h, --help            show this help message and exit
  -u, --users USERS     File with usernames, or usernames list: "jony random,fahim jordan,..."
  -p, --password PASSWORD
                        file with words to "passworize", or list like: "ibis,megacorp,..."
  -l, --light           Light mode, for small list (passwd mode).
  -f, --full            Full mode. Warning, the output could be very heavy (passwd mode).
  -nv, --no-verbose     Remove any output except the dictionary itself (Errors will be shown anyway).
  -d, --dictionary file_name
                        Extract patterns from your an specific dictionary.
  -o, --output file_name
                        Dictionary will be stored in this file.
  -ml, --machine-learning-model file_name
                        Use a trained machine learning model to include neighbors of your original words.
  -n, --neighbours-number integer
                        Ammount of neighbors for each word (20 by Default).
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

<br>

### MACHINE LEARNING mode:

  <mark>WARNING!! 11GB ram required for this option.</mark>

Only available for password mode. This mode will allow you to use a machine learning model to find the nearest possible words to the actual input words. For example, if you use "queen" as input, the nearest neighbors will be "queens", "princess", "women", etc... This will help you to find other words to passworize, but will increase your final dictionary a lot (Light mode recommended). As more details you know from the user, more keywords you will find when trying to map their mind. With this methode you can create realistic wordlists to crack the password of an specific user.

<br>

The `-ml` flag will allow you to set the machine learning model. You can download this trained models from -> https://fasttext.cc/docs/en/crawl-vectors.html

(You need to download the .bin file for the lenguage you want.)

<br>

The `-n` flag will allow you to specify how many neighbors you want for any input word (20 by default).

`python3 dicma.py -p words.txt -o dictionary.txt -l -ml cc.es.300.bin -n 100`

<br>

LINUX / MACOS USERS: For Linux and MacOS dicma will use "fasttext" python library. This can be installed like this:

```
git clone https://github.com/facebookresearch/fastText.git
cd fastText
sudo pip install .
```
More details can be found here -> https://fasttext.cc/docs/en/support.html

<br>

WINDOWS USERS: For Windows users "fasttext" python library have problems to be compiled so dicma will use the windows compiled binary "fasttext.exe". If the binary is not located in the same folder will prompt you to download fasttext.exe. This binary can be found at -> https://github.com/sigmeta/fastText-Windows

To make sure dicma can find fasttext.exe make sure that is in your current working directory.

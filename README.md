# DICMA — The Dictionary Maker

Dicma creates massive wordlists based on specific words for password cracking.

It includes extracted patterns from the rockyou.txt dictionary to "passworize" any word or concept. Users often create passwords based on specific words and modify them with symbols, numbers, and capitalization — Dicma generates all those combinations.

---

## Setup

```bash
pip install openai
```

On first run, Dicma creates `config.txt` with LLM provider examples. The default is **Ollama** (local, no API key required):

```bash
python3 dicma.py
# → config.txt is created automatically
```

### Ollama (default, local, free)

```bash
# Install and start Ollama
brew install ollama       # macOS
# or: curl -fsSL https://ollama.com/install.sh | sh   # Linux
ollama serve

# Pull the default model
ollama pull llama3.2:3b

# Done — config.txt is already set for Ollama
```

### DeepSeek (recommended for best results)

1. Sign up at https://platform.deepseek.com
2. Copy your API key
3. Edit `config.txt` and uncomment the DeepSeek section:

```ini
API_KEY = "sk-your_key"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"
```

### Other providers

```ini
# === OpenAI ===
API_KEY = "sk-your_key"
BASE_URL = "https://api.openai.com/v1"
MODEL = "gpt-4o-mini"
```

---

## Modes

### USERS mode (`-u`)

Generates username combinations from names and surnames using common IT department patterns.

```
# Two words (name + surname)
python3 dicma.py -u "jony random"
# → jony.random, jrandom, jony_random, random.jony, j.r, jr, jony, ...

# Three words (name + two surnames)
python3 dicma.py -u "jony random smith"
# → jony.random.smith, jrs, j.r.s, jony.randoms, j_random_smith, ...

# Light mode: only the most common IT patterns (~10 patterns)
python3 dicma.py -u "jony random" -l
# → jony.random, jrandom, jony_random, j.random, jony.r, ...

# From file
python3 dicma.py -u users.txt -o usernames.txt
```

---

### PASSWORD mode (`-p`)

Generates password variations with suffixes, prefixes, leet speak, numbers and symbols.

```
# Basic (no LLM): password-patterns only
python3 dicma.py -p "dragon"
# → dragon, Dragon, DRAGON, dr@gon, dragon1, dragon123, ...

# Save to file
python3 dicma.py -p "dragon" -o dic.txt

# Light mode (~7K lines per word)
python3 dicma.py -p "dragon" -l -o dic.txt

# Full mode (~5M lines per word)
python3 dicma.py -p "dragon" -f -o dic.txt

# From file with a custom dictionary for pattern extraction
python3 dicma.py -p words.txt -d rockyou.txt -o dic.txt
```

**With LLM expansion** (`-n1`). Finds semantically related words first, then passworizes them:

```
# Expand "dragon" with 20 semantic neighbours, then passworize all
python3 dicma.py -p "dragon" -n1 20 -o dic.txt

# Multi-level expansion
python3 dicma.py -p "starwars" -n1 20 -n2 10 -n3 5 -o dic.txt
```

`-n1` triggers LLM mode. `-n2` and `-n3` add indirect neighbours (second and third degree). Each level multiplies the number of base words before password patterns are applied, resulting in larger dictionaries.

---

### JUST-NEIGHBOURS mode (`-jn`)

Find semantically related words using an LLM. No password patterns applied — just plain words.

```
# Basic: 20 related words for "starwars"
python3 dicma.py -jn "starwars" -n1 20
# → jedi, skywalker, lightsaber, darthvader, sith, ...

# Two levels: 20 direct + 10 indirect per direct result
python3 dicma.py -jn "starwars" -n1 20 -n2 10

# Three levels
python3 dicma.py -jn "dragon" -n1 20 -n2 10 -n3 5

# Save to file
python3 dicma.py -jn "starwars" -n1 20 -o neighbours.txt

# Multiple input words
python3 dicma.py -jn "starwars,finalfantasy" -n1 20
```

---

## Full help

```
usage: dicma.py [-h] (-u USERS | -p PASSWORD | -jn JUST_NEIGHBOURS)
                [-l] [-f] [-nv] [-d file_name] [-o file_name]
                [-n1 N1] [-n2 N2] [-n3 N3]
                [--api-key API_KEY] [--base-url BASE_URL]
                [--model MODEL] [--config CONFIG]
```

| Flag | Description |
|---|---|
| `-u` | Users mode: generate username combinations |
| `-p` | Password mode: generate password variations |
| `-jn` | Just neighbours: find related words (LLM) |
| `-l` | Light mode (users: IT patterns only, passwords: ~7K lines/word) |
| `-f` | Full mode (passwords: ~5M lines/word) |
| `-nv` | No verbose: only output the dictionary |
| `-d` | Custom dictionary for pattern extraction |
| `-o` | Output file (otherwise prints to stdout) |
| `-n1` | Level-1 neighbours per input word (triggers LLM) |
| `-n2` | Level-2 neighbours per level-1 result (LLM) |
| `-n3` | Level-3 neighbours per level-2 result (LLM) |
| `--api-key` | LLM API key (or env var LLM_API_KEY) |
| `--base-url` | LLM API base URL (default from config.txt) |
| `--model` | LLM model name (default from config.txt) |
| `--config` | Config file path (default: config.txt) |

Config precedence: CLI args > env vars > config.txt > defaults.

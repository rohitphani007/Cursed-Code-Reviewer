# Cursed Code Reviewer

The ghost of a dead programming language haunts your code. Point it at a file, pick a ghost, and it gives you a spooky greeting, three numbered review comments, and a farewell. It runs entirely on your own computer with a small open-weight model through Ollama, so your code never leaves your machine.

Built for the Hacktoberfest Open-Source AI Challenge, Week 4: Ghost in the Machine.

## Setup

1. Install [Ollama](https://ollama.com) and make sure it is running.
2. Download the model:

   ```
   ollama pull llama3.2:3b
   ```

3. Install the Python package:

   ```
   pip install ollama
   ```

## Usage

```
python haunt.py <code_file> [ghost]
```

For example:

```
python haunt.py haunt.py cobol
```

Ghosts: `cobol`, `fortran`, `perl`, `lisp`, `basic`. The default is `cobol`.

To try another model, change the `MODEL` line at the top of `haunt.py` and pull that model with `ollama pull`.

## How it works

The script numbers the lines of your file and sends it to a local model with a short prompt. The model writes three numbered review points. The ghost's greeting and farewell are written in plain Python, not by the model, because the small model was unreliable at producing them.

## Limitations

This uses a 3B model on a CPU, so the feedback is entertaining but not always right. In my tests it sometimes misread code or made a false claim, so treat it as a fun second opinion and not a real code review. Very long files are cut off at 6000 characters.
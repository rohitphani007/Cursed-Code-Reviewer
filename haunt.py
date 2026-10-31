"""
Cursed Code Reviewer
The ghost of a dead programming language haunts your code.
Runs fully locally through Ollama. No internet needed after the model is downloaded.

Usage:
    python haunt.py <code_file> [ghost]

Ghosts: cobol, fortran, perl, lisp, basic
"""

import sys
from pathlib import Path

import ollama

MODEL = "llama3.2:3b"   # change this one line to try another model, e.g. "qwen2.5-coder:3b"
MAX_CHARS = 6000             # long files are cut so a small model can cope

# Short description of each ghost's voice (kept short on purpose, small models echo long ones)
GHOSTS = {
    "cobol": "the ghost of COBOL, dramatic and bureaucratic, mourning divisions and paragraphs",
    "fortran": "the ghost of FORTRAN, proud and ancient, obsessed with arrays and punch cards",
    "perl": "the ghost of Perl, mischievous and cryptic, muttering about line noise",
    "lisp": "the ghost of Lisp, calm and eerie, whispering about parentheses",
    "basic": "the ghost of BASIC, nostalgic, remembering line numbers and GOTO",
}

# The greeting and farewell are written here, in plain code, so the model does not have to
# produce them. Its only job is the three numbered points.
GREETINGS = {
    "cobol": "AH... MORTAL. I AM THE GHOST OF COBOL. I HAVE READ YOUR CODE AND MY DIVISIONS WEEP.",
    "fortran": "Mortal... I am FORTRAN, born in 1957. I have counted your array indices in the dark.",
    "perl": "Heh heh... mortal. I am Perl. There is more than one way to haunt you.",
    "lisp": "(whisper (mortal) (i-am-lisp)) ... I have read your code, and counted its parentheses.",
    "basic": "10 PRINT 'BOO'. 20 GOTO 10. Mortal... I am BASIC. I have read your code.",
}
FAREWELLS = {
    "cobol": "STOP RUN. I RETURN WHEN THE NEXT BUILD FAILS.",
    "fortran": "END. Until the next compile, mortal.",
    "perl": "1; # I will be back. Perl always returns true.",
    "lisp": "(return 'to-the-void) ... until we meet again.",
    "basic": "END. Type RUN if you dare to summon me again.",
}

SYSTEM = """You are {persona}.
You are haunting a programmer by reviewing their code, in your spooky ghostly voice.
Write exactly 3 short numbered points. Each point must name something REAL from the code (a function name, a variable name or a line number) and say one thing about it or one thing to improve.
Do not describe what the program does in general. Do not invent names or problems. Do not use your own language's keywords.
Do not write a greeting, a farewell, headings or markdown. Start directly with "1." and keep it under 100 words."""

USER = "File: {filename} (judge ONLY what is written below)\n{code}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    path = Path(sys.argv[1])
    ghost = sys.argv[2].lower() if len(sys.argv) > 2 else "cobol"

    if not path.is_file():
        print(f"Cannot find the file: {path}")
        sys.exit(1)
    if ghost not in GHOSTS:
        print(f"Unknown ghost '{ghost}'. Choose from: {', '.join(GHOSTS)}")
        sys.exit(1)

    code = path.read_text(encoding="utf-8", errors="replace")
    if len(code) > MAX_CHARS:
        code = code[:MAX_CHARS] + "\n... (the rest has faded into the mist)"

    # Number the lines so the model can point at real places
    code = "\n".join(f"{n}: {line}" for n, line in enumerate(code.splitlines(), 1))

    system_msg = SYSTEM.format(persona=GHOSTS[ghost])
    user_msg = USER.format(filename=path.name, code=code)

    print(f"\nSummoning the ghost of {ghost.upper()}... (this can take a little while)\n")
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            options={"temperature": 0.4},
        )
    except Exception as err:
        print(f"The spirits would not answer: {err}")
        print("Make sure Ollama is running and that you ran:  ollama pull " + MODEL)
        sys.exit(1)

    print(GREETINGS[ghost])
    print()
    print(response["message"]["content"].strip())
    print()
    print(FAREWELLS[ghost])
    print()


if __name__ == "__main__":
    main()
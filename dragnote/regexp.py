import re


NOTE_DURATION_RE = re.compile(r"^(?P<name>[AC-Hac-h])(?P<sign>[#b]*)(?P<octave>\d)(\((?P<duration>\S+)\))?$")

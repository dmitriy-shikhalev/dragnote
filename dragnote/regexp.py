import re


NOTE_DURATION_RE = re.compile(
    r"^(?P<name_first>[AC-Hac-h])(?P<sign_first>[#b]*)(?P<octave_first>\d)"
    r"(:(?P<name_additial>[AC-Hac-h])(?P<sign_additional>[#b]*)(?P<octave_additional>\d))*"
    r"(\((?P<duration>\S+)\))?$"
)

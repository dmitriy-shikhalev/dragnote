import re

NOTE_INPUT = re.compile(r"^(?P<note>[ac-hAC-H])(?P<sign>bb|b|#|##)?(?P<octave>-?\d)$")

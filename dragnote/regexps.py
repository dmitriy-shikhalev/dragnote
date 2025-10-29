import re

NOTE_INPUT = re.compile(r"^(?P<name>[ac-hAC-H])(?P<sign>bb|b|#|##)?(?P<octave>-?\d)$")
DURATION_INPUT = re.compile(r"^\((?P<beats>\d+)/(?P<duration>\d+)\)")

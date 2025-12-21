"""
Зона ответственности модуля - одно уражнение.
"""

class Exercise:
    def __init__(
        self,
        num: int,
        composition: Composition,
        sequencer: Sequencer,
        max_error_count: int,
        volume: int,
        tempo: int,
    ):
        self.num = num
        self.composition = list(composition)
        self.sequencer = sequencer
        self.max_error_count = max_error_count
        self.volume = volume
        self.tempo = tempo
        self.input_queue = InputQueue()  # Нужно более говорящее название,а не input_queue
        self.queue: LifoQueue[Harmony] = LifoQueue()
        self._init_queue()

        self.error_count = 0
        self._notes = []

    def _play_composition(self):
        logger.debug("Play composition")
        self.sequencer.play_composition(self.composition)

    def _init_queue(self):
        for harmony in self.composition[::-1]:
            self.queue.put(harmony)

    def _ok(self, harmony: Harmony):
        logger.debug("Ok")
        self.sequencer.play_harmony(harmony)
        play_ok()
        self.error_count = 0
        self._notes.append(harmony.notes)

    def _mistake(self, harmony: Harmony, notes: list[Note]):
        logger.debug("Mistake")
        self.queue.put(harmony)
        self.sequencer.play_harmony(Harmony(notes=tuple(notes), duration=harmony.duration))
        play_mistake()
        self.sequencer.play_harmony(harmony)
        self.error_count += 1
        if self.error_count > self.max_error_count:
            raise GameOver

    def _get_notes(self, first_note: Harmony, notes_list: list[list[Note]]) -> set[Note]:
        return self.input_queue.get(first_note=first_note, notes_list=notes_list)

    @staticmethod
    def _is_harmony_eq_notes(harmony: Harmony, notes: list[Note]):
        return set(notes) == set(harmony.notes)

    def _one_iterate_play(self):
        logger.debug("One iteration play")
        try:
            notes = list(self._get_notes(first_note=self.composition[0], notes_list=self._notes))
        except EmptyInput:
            self._play_composition()
            return

        harmony = self.queue.get()
        if self._is_harmony_eq_notes(harmony, notes):
            self._ok(harmony)
        else:
            self._mistake(harmony, notes)

    def play(self):
        logger.debug("Play")
        print(f"New composition: {self.num}")
        self._play_composition()

        while True:
            if not self.queue.qsize():
                play_over()
                break

            self._one_iterate_play()

# dragnote

## В debian linux запустить fluidsynth:
- Установить ALSA в ОС.
- Установить в ОС ```fluidsynth``` и ```fluid-soundfont-gm```.
- Открыть терминал и запустить ```fluidsynth```.
- Узнать номер синтезатора ```aconnect -l``` (номер - это порядковый номер из приведенных, начиная с 0)
```
$ aconnect -l
client 0: 'System' [type=ядро]
    0 'Timer           '
        Подключение к: 144:0
    1 'Announce        '
        Подключение к: 144:0
client 14: 'Midi Through' [type=ядро]
    0 'Midi Through Port-0'
client 128: 'FLUID Synth (3539874)' [type=пользователь,pid=3539874]
    0 'Synth input port (3539874:0)'
client 144: 'PipeWire-System' [type=пользователь,pid=270936]
    0 'input           '
        Подключено от: 0:1, 0:0
client 145: 'PipeWire-RT-Event' [type=пользователь,pid=270936]
    0 'input           '
``` - номер Fluid Synth равен 2
- Вписать номер синтезатора в ```settings.yaml```

## Запуск:
- ```python dragnote```

## Добавить кучу гамм: https://samesound.ru/write/78409-piano-scales-for-dummies

## Цели:
- покрыть тестами Game
- покрыть тестами Exercise
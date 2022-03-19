#!/usr/bin/env python

from typing import TextIO
from unicodedata import category as unicodedata_category


def get_text_data(fd: TextIO):
    """ """

    # Set up positional markers and slots

    pos = 0

    nword = 0
    word = ""
    word_pos = 0

    nsent = 1
    sent_pos = 0
    sent = ""

    nline = 0
    line = ""
    line_pos = 0

    nblok = 1
    blok_pos = 0
    blok = ""

    while c := fd.read(1):

        category = unicodedata_category(c)
        if len(category) > 2:
            raise Exception(f"Weird character! {c}")

        ordinal = ord(c)

        if category[0] == "L":

            # New word
            if not word:
                word_pos = pos

            word += c
            line += c

            if not sent:
                sent_pos = pos
            sent += c

            if not blok:
                blok_pos = pos
            blok += c

        # Separator
        elif category[0] in "MNPSZC":

            # Connectors ... ignore
            if (word and category == "Cf") or (word and category == "Pc"):
                pass

            # Sentence Breaker
            elif category == "Po":
                sent += c
                line += c

                if c in ".?!¿¡" and sent.strip():
                    nsent += 1
                    yield "SENT", sent_pos, nsent, sent
                    sent = ""

                if not blok:
                    blok_pos = pos
                blok += c

            # Control character
            elif ordinal in [0x0D, 0x0A]:

                if line.strip():
                    nline += 1
                    yield "LINE", line_pos, nline, line.rstrip()
                    line = ""

                    if not blok:
                        blok_pos = pos
                    blok += c

                else:
                    nblok += 1
                    yield "BLOK", blok_pos, nblok, blok.rstrip()
                    blok = ""

                line_pos = pos + 1

                if sent:
                    sent += " "

            else:
                line += c

                if sent:
                    sent += c

                if not blok:
                    blok_pos = pos
                blok += c

            # Handle word and sent
            if word:
                nword += 1
                yield "WORD", word_pos, nword, word
                word = ""

        pos += 1

    if sent.strip():
        yield "SENT", sent_pos, nsent, sent
    if word:
        yield "WORD", word_pos, nword, word
    if line.strip():
        yield "LINE", line_pos, nline, line.rstrip()
    if blok:
        yield "BLOK", blok_pos, nblok, blok.rstrip()


def foo():

    for k, pos, n, v in list(get_text_data(stream)):
        if v != data[pos : pos + len(v)].rstrip():

            if k == "SENT":
                new_data = data[pos : pos + len(v)].replace("\n", " ")
                if v == new_data:
                    continue
                else:
                    print(k, n)
                    print(f">>{v}<<")
                    print(f">>{new_data}<<")
            else:
                print(k, n)
                print(f">>{v}<<")
                print(f">>{data[pos:pos+len(v)]}<<")

        else:
            print(k, n, "OK")
            print(f"{v}")

    print()


if __name__ == "__main__":

    from io import StringIO
    from sys import stdin

    stream = StringIO(stdin.read())
    data = stream.getvalue()
    stream.seek(0)

    for k, pos, n, v in list(get_text_data(stream)):
        print(k, pos, n, v)

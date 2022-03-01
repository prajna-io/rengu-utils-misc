#!/usr/bin/env python

from unicodedata import category as unicodedata_category
from typing import TextIO




def get_text_data(fd: TextIO):
    """
    """

    # Set up positional markers and slots

    pos = 0

    nword = 0
    word = ""
    word_pos = 0

    nsent = 0
    sent_pos = 0
    sent = ""

    nline = 0
    line = ""
    line_pos = 0

    nblok = 0
    blok_pos = 0
    blok = ""


    while c := fd.read(1):
       
        category = unicodedata_category(c)
        if len(category) > 2:
            raise Exception(f"Weird character! {c}")

        ordinal = ord(c)
     
        match category[0]:

            # Letter
            case "L": 

                # New word
                if not word:
                    word_pos = pos

                word += c
                line += c

                if not sent:
                    sent_pos = pos
                sent += c

            # Separator
            case "M" | "N" | "P" | "S" | "Z" |"C":

                # Connectors ... ignore
                if ( word and category == "Cf" ) or ( word and category == "Pc" ):
                    pass

                # Sentence Breaker
                elif category == "Po":
                    sent += c
                    line += c
                    
                    if  c in '.?!¿¡'  and sent.strip():
                        nsent += 1
                        yield "SENT", sent_pos, nsent, sent
                        sent = ""

                # Control character
                elif ordinal in [ 0x0d, 0x0a ]:
                    
                    if line.strip():
                        nline += 1
                        yield "LINE", line_pos, nline, line
                        line = ""

                    else:
                        nblok += 1
                        yield "BLOK", blok_pos, nblok, blok
                        blok = ""
                        blok_pos = pos + 1
     
                    line_pos = pos + 1

                    if sent:
                        sent += " "

                else:
                    line += c

                    if sent:
                        sent += c

                # Handle word and sent
                if word:
                    nword += 1
                    yield "WORD", word_pos, nword, word
                    word = ""


        pos += 1
        blok += c

    if sent.strip():
        yield "SENT", sent_pos, nsent, sent
    if word:
        yield "WORD", word_pos, nword, word
    if line.strip():
        yield "LINE", line_pos, nline, line
    if blok:
        yield "BLOK", blok_pos, nblok, blok


if __name__ == "__main__":
    
    from sys import stdin

    for d in get_text_data(stdin):
        print(d)

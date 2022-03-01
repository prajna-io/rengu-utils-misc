#!/usr/bin/env python


from sys import stdin

import unicodedata

from slugify import slugify

pos = 0

nword = 0
word = ""
word_pos = 0

nline = 0
line = ""
line_pos = 0

nblok = 0
blok_pos = 0
blok = ""

nsent = 0
sent_pos = 0
sent = ""


while c := stdin.read(1):
   
    category = unicodedata.category(c)
    if len(category) > 2:
        print(c, category)
        raise Exception("Weird character!")

    ordinal = ord(c)
 
    match category[0]:

        # Letter
        case "L": 

            # New word
            if not word:
                word_pos = pos

            word += c
            line += c
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
                
                if sent.strip():
                    nsent += 1
                    print("SENT :", sent_pos, nsent, sent)
                    sent = ""

            # Control character
            elif ordinal in [ 0x0d, 0x0a ]:
                
                if line.strip():
                    nline += 1
                    print("LINE :", line_pos, nline, line)
                    line = ""

                else:
                    print("BLOCK")
                    blok = ""
                
                sent += " "
                line_pos = pos + 1

            else:
                if word:
                    nword += 1
                    print("WORD :", word_pos, nword, word)
                    word = ""

                if line:
                    line += c

                if sent:
                    sent += c

    pos += 1

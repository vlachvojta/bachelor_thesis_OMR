# Prevod symbolu na kratsi format

## Semantic encoding types:
* barline -> b
* clef
* gracenote
* keySignature
* multirest -> m\d{1,4}
* note
* rest
* tie
* timeSignature

### Note
- vzdy note_vyska... ?

## Agnostic encoding types
* accidental
* barline -> B
* clef -> r'C[CFG]\d'
* digit
* dot
* fermata -> F
* gracenote
* metersign -> r'M[CD]'
* multirest -> M
* note
* rest -> r'R[EHQSTW46]\d'
* slur -> 'S(S|E)(L|S).?\d':

## slur 
JE rozdíl mezi slur.end-L-2 a slur.end-L2!!
**Slur back?**

## rest
rest.eighth-L3 -> RE3
rest.half-L3 -> RH3
**rest.quadruple_whole-L3** -> RQ3
**rest.quarter-L3** -> R43
**rest.sixteenth-L3** -> R63
**rest.sixty_fourth-L3** -> RS3
rest.thirty_second-L3 -> RT3 
rest.whole-L4 -> RW4

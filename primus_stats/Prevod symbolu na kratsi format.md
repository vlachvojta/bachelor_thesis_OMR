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
* accidental -> r'r'A[FNS][LS]_?\d''
* barline -> B
* clef -> r'C[CFG]\d'
* digit -> r'D\d{2}[HLS]'
* dot -> OK
* fermata -> F
* gracenote
* metersign -> r'M[CD]'
* multirest -> M
* note
* rest -> r'R[EHQSTW46]\d'
* slur -> 'S(S|E)(L|S).?\d':

### rest
rest.eighth-L3 -> RE3
rest.half-L3 -> RH3
**rest.quadruple_whole-L3** -> RQ3
**rest.quarter-L3** -> R43
**rest.sixteenth-L3** -> R63
**rest.sixty_fourth-L3** -> RS3
rest.thirty_second-L3 -> RT3 
rest.whole-L4 -> RW4

### digit
r'digit\.\d{1,2}-(S5|L[2-4])'
L4 -> H (higher time signature symbol)
L2 -> L (lower time signature symbol)
S5 -> S (digits above note staff)



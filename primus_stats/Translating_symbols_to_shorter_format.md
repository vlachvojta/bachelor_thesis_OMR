# Translating symbols to shorter format

## Semantic encoding types:
* barline -> b
* clef -> OK
* gracenote -> OK
* keySignature -> r'k[a-g][#b]?m'
* multirest -> m\d{1,4}
* note -> OK
* rest -> OK
* tie -> OK
* timeSignature

## Agnostic encoding types
* accidental -> r'r'A[FNS][LS]_?\d''
* barline -> B
* clef -> r'C[CFG]\d'
* digit -> r'D\d{2}[HLS]'
* dot -> OK
* fermata -> F
* gracenote -> r'G(B\d|R\d|[DEHQST46])[SL]_?\d'
* metersign -> r'M[CD]'
* multirest -> M
* note -> r'N(B\d|R\d|L\d|[DEHQST46])[SL]_?\d'
* rest -> r'R[EHQSTW46]\d'
* slur -> 'S(S|E)(L|S).?\d'

### agnostic length:
eighth -> E
half -> H
**quadruple_whole -> Q**
**quarter -> 4**
**sixteenth -> 6**
**sixty_fourth -> S**
thirty_second -> T 
whole -> W

### digit
* L4 -> H (higher time signature symbol)
* L2 -> L (lower time signature symbol)
* S5 -> S (digits above note staff)

### gracenote
* beamedBoth\d -> B\d
* beamedRight\d -> R\d

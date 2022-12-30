# %%
import json
import pyperclip
from common import Common


class Sym_conv:

    data = []
    data_before = []
    data_out = []
    repeated = []

    len_before = 0

    def __init__(self, data: list = []):
        data = set(data)
        self.len_before = len(data)
        self.data = data
        self.data_before = data
        self.repeated = []

    def _replace(self, pattern: str, with_what: str):
        self.data = [v.replace(pattern, with_what) for v in self.data]

    def _replace_dict(self, dictos: dict = {}):
        for k, v in dictos.items():
            self._replace(k, v)

    def finalize(self):
        identical_list = Sym_conv.get_identical_list(self.data,
                                                     self.data_before)

        self.out = Sym_conv.two_lists_to_dict(self.data_before, self.data)

        assert self.len_before == len(self.out)

        new_out = {k: self.out[k] for k in sorted(self.out.keys())}

        pyperclip.copy(json.dumps(new_out))
        Sym_conv.print_dict(self.out)

        print(f'{len(identical_list)} symbols stil to convert ' +
              f'from total {len(self.data)}')
        print(f'TODO for example: {sorted(identical_list)[:100]}')

        if not self.len_before == len(set(self.data)):
            sorted_data = sorted(self.data)
            self.repeated += [v for i, v in enumerate(sorted_data)
                              if v == sorted_data[i-1]]
        if len(self.repeated) > 0:
            print(f'Repeated symbols are: {self.repeated}')

    @staticmethod
    def print_dict(data: dict = {}) -> None:
        keys = sorted(data.keys())
        for k in keys:
            print(f'"{k}": "{data[k]}",')

    @staticmethod
    def get_identical_list(list1: list = [], list2: list = []) -> int:
        identical_list = []
        for v1, v2 in zip(list1, list2):
            if v1 == v2:
                identical_list.append(v1)
        return identical_list

    @staticmethod
    def two_lists_to_dict(l1: list = [], l2: list = []):
        return {v1: v2 for v1, v2 in zip(l1, l2)}

# %%


def main():
    # %%
    data = ['accidental.flat-L-1', 'accidental.flat-L0', 'accidental.flat-L1', 'accidental.flat-L2', 'accidental.flat-L3', 'accidental.flat-L4', 'accidental.flat-L5', 'accidental.flat-L6', 'accidental.flat-L7', 'accidental.flat-L8', 'accidental.flat-S-1', 'accidental.flat-S-2', 'accidental.flat-S0', 'accidental.flat-S1', 'accidental.flat-S2', 'accidental.flat-S3', 'accidental.flat-S4', 'accidental.flat-S5', 'accidental.flat-S6', 'accidental.flat-S7', 'accidental.natural-L-1', 'accidental.natural-L-2', 'accidental.natural-L0', 'accidental.natural-L1', 'accidental.natural-L2', 'accidental.natural-L3', 'accidental.natural-L4', 'accidental.natural-L5', 'accidental.natural-L6', 'accidental.natural-L7', 'accidental.natural-L8', 'accidental.natural-S-1', 'accidental.natural-S-2', 'accidental.natural-S-3', 'accidental.natural-S0', 'accidental.natural-S1', 'accidental.natural-S2', 'accidental.natural-S3', 'accidental.natural-S4', 'accidental.natural-S5', 'accidental.natural-S6', 'accidental.natural-S7', 'accidental.sharp-L-1', 'accidental.sharp-L-2', 'accidental.sharp-L0', 'accidental.sharp-L1', 'accidental.sharp-L2', 'accidental.sharp-L3', 'accidental.sharp-L4', 'accidental.sharp-L5', 'accidental.sharp-L6', 'accidental.sharp-L7', 'accidental.sharp-L8', 'accidental.sharp-S-1', 'accidental.sharp-S-2', 'accidental.sharp-S0', 'accidental.sharp-S1', 'accidental.sharp-S2', 'accidental.sharp-S3', 'accidental.sharp-S4', 'accidental.sharp-S5', 'accidental.sharp-S6', 'accidental.sharp-S7', 'accidental.sharp-S8', 'barline-L1', 'clef.C-L1', 'clef.C-L2', 'clef.C-L3', 'clef.C-L4', 'clef.C-L5', 'clef.F-L3', 'clef.F-L4', 'clef.F-L5', 'clef.G-L1', 'clef.G-L2', 'digit.0-S5', 'digit.1-L2', 'digit.1-L4', 'digit.1-S5', 'digit.11-L4', 'digit.12-L2', 'digit.12-L4', 'digit.16-L2', 'digit.2-L2', 'digit.2-L4', 'digit.2-S5', 'digit.24-L4', 'digit.3-L2', 'digit.3-L4', 'digit.3-S5', 'digit.4-L2', 'digit.4-L4', 'digit.4-S5', 'digit.48-L2', 'digit.5-L4', 'digit.5-S5', 'digit.6-L2', 'digit.6-L4', 'digit.6-S5', 'digit.7-L4', 'digit.7-S5', 'digit.8-L2', 'digit.8-L4', 'digit.8-S5', 'digit.9-L4', 'digit.9-S5', 'dot-S-1', 'dot-S-2', 'dot-S-3', 'dot-S0', 'dot-S1', 'dot-S2', 'dot-S3', 'dot-S4', 'dot-S5', 'dot-S6', 'dot-S7', 'dot-S8', 'fermata.above-S6', 'gracenote.beamedBoth1-L1', 'gracenote.beamedBoth1-L2', 'gracenote.beamedBoth1-L3', 'gracenote.beamedBoth1-L4', 'gracenote.beamedBoth1-L5', 'gracenote.beamedBoth1-L6', 'gracenote.beamedBoth1-S0', 'gracenote.beamedBoth1-S1', 'gracenote.beamedBoth1-S2', 'gracenote.beamedBoth1-S3', 'gracenote.beamedBoth1-S4', 'gracenote.beamedBoth1-S5', 'gracenote.beamedBoth2-L-1', 'gracenote.beamedBoth2-L0', 'gracenote.beamedBoth2-L1', 'gracenote.beamedBoth2-L2', 'gracenote.beamedBoth2-L3', 'gracenote.beamedBoth2-L4', 'gracenote.beamedBoth2-L5', 'gracenote.beamedBoth2-L6', 'gracenote.beamedBoth2-S-1', 'gracenote.beamedBoth2-S0', 'gracenote.beamedBoth2-S1', 'gracenote.beamedBoth2-S2', 'gracenote.beamedBoth2-S3', 'gracenote.beamedBoth2-S4', 'gracenote.beamedBoth2-S5', 'gracenote.beamedBoth3-L1', 'gracenote.beamedBoth3-L2', 'gracenote.beamedBoth3-L3', 'gracenote.beamedBoth3-L4', 'gracenote.beamedBoth3-L5', 'gracenote.beamedBoth3-L6', 'gracenote.beamedBoth3-S1', 'gracenote.beamedBoth3-S2', 'gracenote.beamedBoth3-S3', 'gracenote.beamedBoth3-S4', 'gracenote.beamedBoth3-S5', 'gracenote.beamedRight0-S2', 'gracenote.beamedRight1-L5', 'gracenote.double_whole-L5', 'gracenote.eighth-L-1', 'gracenote.eighth-L0', 'gracenote.eighth-L1', 'gracenote.eighth-L2', 'gracenote.eighth-L3', 'gracenote.eighth-L4', 'gracenote.eighth-L5', 'gracenote.eighth-L6', 'gracenote.eighth-S-1', 'gracenote.eighth-S0', 'gracenote.eighth-S1', 'gracenote.eighth-S2', 'gracenote.eighth-S3', 'gracenote.eighth-S4', 'gracenote.eighth-S5', 'gracenote.half-L2', 'gracenote.half-L3', 'gracenote.half-L4', 'gracenote.half-L5', 'gracenote.half-L6', 'gracenote.half-S2', 'gracenote.half-S3', 'gracenote.half-S4', 'gracenote.half-S5', 'gracenote.quarter-L0', 'gracenote.quarter-L1', 'gracenote.quarter-L2', 'gracenote.quarter-L3', 'gracenote.quarter-L4', 'gracenote.quarter-L5', 'gracenote.quarter-L6', 'gracenote.quarter-S0', 'gracenote.quarter-S1', 'gracenote.quarter-S2', 'gracenote.quarter-S3', 'gracenote.quarter-S4', 'gracenote.quarter-S5', 'gracenote.sixteenth-L-1', 'gracenote.sixteenth-L-2', 'gracenote.sixteenth-L0', 'gracenote.sixteenth-L1', 'gracenote.sixteenth-L2', 'gracenote.sixteenth-L3', 'gracenote.sixteenth-L4', 'gracenote.sixteenth-L5', 'gracenote.sixteenth-L6', 'gracenote.sixteenth-S-1', 'gracenote.sixteenth-S-2', 'gracenote.sixteenth-S0', 'gracenote.sixteenth-S1', 'gracenote.sixteenth-S2', 'gracenote.sixteenth-S3', 'gracenote.sixteenth-S4', 'gracenote.sixteenth-S5', 'gracenote.thirty_second-L-1', 'gracenote.thirty_second-L0', 'gracenote.thirty_second-L1', 'gracenote.thirty_second-L2', 'gracenote.thirty_second-L3', 'gracenote.thirty_second-L4', 'gracenote.thirty_second-L5', 'gracenote.thirty_second-L6', 'gracenote.thirty_second-S-1', 'gracenote.thirty_second-S-2', 'gracenote.thirty_second-S0', 'gracenote.thirty_second-S1', 'gracenote.thirty_second-S2', 'gracenote.thirty_second-S3', 'gracenote.thirty_second-S4', 'gracenote.thirty_second-S5', 'metersign.C-L3', 'metersign.C/-L3', 'multirest-L3', 'note.beamedBoth0-L0', 'note.beamedBoth0-L1', 'note.beamedBoth0-L2', 'note.beamedBoth0-L3', 'note.beamedBoth0-L4', 'note.beamedBoth0-L5', 'note.beamedBoth0-L6', 'note.beamedBoth0-L7', 'note.beamedBoth0-S-1', 'note.beamedBoth0-S-3', 'note.beamedBoth0-S0', 'note.beamedBoth0-S1', 'note.beamedBoth0-S2', 'note.beamedBoth0-S3', 'note.beamedBoth0-S4', 'note.beamedBoth0-S5', 'note.beamedBoth0-S6', 'note.beamedBoth1-L-1', 'note.beamedBoth1-L-2', 'note.beamedBoth1-L-3', 'note.beamedBoth1-L0', 'note.beamedBoth1-L1', 'note.beamedBoth1-L2', 'note.beamedBoth1-L3', 'note.beamedBoth1-L4', 'note.beamedBoth1-L5', 'note.beamedBoth1-L6', 'note.beamedBoth1-L7', 'note.beamedBoth1-L8', 'note.beamedBoth1-S-1', 'note.beamedBoth1-S-2', 'note.beamedBoth1-S-3', 'note.beamedBoth1-S0', 'note.beamedBoth1-S1', 'note.beamedBoth1-S2', 'note.beamedBoth1-S3', 'note.beamedBoth1-S4', 'note.beamedBoth1-S5', 'note.beamedBoth1-S6', 'note.beamedBoth1-S7', 'note.beamedBoth1-S8', 'note.beamedBoth2-L-1', 'note.beamedBoth2-L-2', 'note.beamedBoth2-L-3', 'note.beamedBoth2-L0', 'note.beamedBoth2-L1', 'note.beamedBoth2-L2', 'note.beamedBoth2-L3', 'note.beamedBoth2-L4', 'note.beamedBoth2-L5', 'note.beamedBoth2-L6', 'note.beamedBoth2-L7', 'note.beamedBoth2-L8', 'note.beamedBoth2-S-1', 'note.beamedBoth2-S-2', 'note.beamedBoth2-S-3', 'note.beamedBoth2-S0', 'note.beamedBoth2-S1', 'note.beamedBoth2-S2', 'note.beamedBoth2-S3', 'note.beamedBoth2-S4', 'note.beamedBoth2-S5', 'note.beamedBoth2-S6', 'note.beamedBoth2-S7', 'note.beamedBoth2-S8', 'note.beamedBoth3-L-1', 'note.beamedBoth3-L-2', 'note.beamedBoth3-L0', 'note.beamedBoth3-L1', 'note.beamedBoth3-L2', 'note.beamedBoth3-L3', 'note.beamedBoth3-L4', 'note.beamedBoth3-L5', 'note.beamedBoth3-L6', 'note.beamedBoth3-L7', 'note.beamedBoth3-L8', 'note.beamedBoth3-S-1', 'note.beamedBoth3-S-2', 'note.beamedBoth3-S0', 'note.beamedBoth3-S1', 'note.beamedBoth3-S2', 'note.beamedBoth3-S3', 'note.beamedBoth3-S4', 'note.beamedBoth3-S5', 'note.beamedBoth3-S6', 'note.beamedBoth3-S7', 'note.beamedBoth3-S8', 'note.beamedBoth4-L-1', 'note.beamedBoth4-L0', 'note.beamedBoth4-L1', 'note.beamedBoth4-L2', 'note.beamedBoth4-L3', 'note.beamedBoth4-L4', 'note.beamedBoth4-L5', 'note.beamedBoth4-L6', 'note.beamedBoth4-L7', 'note.beamedBoth4-S-1', 'note.beamedBoth4-S0', 'note.beamedBoth4-S1', 'note.beamedBoth4-S2', 'note.beamedBoth4-S3', 'note.beamedBoth4-S4', 'note.beamedBoth4-S5', 'note.beamedBoth4-S6', 'note.beamedBoth4-S7', 'note.beamedBoth5-L0', 'note.beamedBoth5-L1', 'note.beamedLeft0-L1', 'note.beamedLeft0-L2', 'note.beamedLeft0-L3', 'note.beamedLeft0-L4', 'note.beamedLeft0-L5', 'note.beamedLeft0-L6', 'note.beamedLeft0-L7', 'note.beamedLeft0-S-2', 'note.beamedLeft0-S-3', 'note.beamedLeft0-S1', 'note.beamedLeft0-S2', 'note.beamedLeft0-S3', 'note.beamedLeft0-S4', 'note.beamedLeft0-S5', 'note.beamedLeft0-S6', 'note.beamedLeft0-S7', 'note.beamedLeft1-L-1', 'note.beamedLeft1-L-2', 'note.beamedLeft1-L0', 'note.beamedLeft1-L1', 'note.beamedLeft1-L2', 'note.beamedLeft1-L3', 'note.beamedLeft1-L4', 'note.beamedLeft1-L5', 'note.beamedLeft1-L6', 'note.beamedLeft1-L7', 'note.beamedLeft1-L8', 'note.beamedLeft1-S-1', 'note.beamedLeft1-S-2', 'note.beamedLeft1-S-3', 'note.beamedLeft1-S0', 'note.beamedLeft1-S1', 'note.beamedLeft1-S2', 'note.beamedLeft1-S3', 'note.beamedLeft1-S4', 'note.beamedLeft1-S5', 'note.beamedLeft1-S6', 'note.beamedLeft1-S7', 'note.beamedLeft1-S8', 'note.beamedLeft2-L-1', 'note.beamedLeft2-L-2', 'note.beamedLeft2-L0', 'note.beamedLeft2-L1', 'note.beamedLeft2-L2', 'note.beamedLeft2-L3', 'note.beamedLeft2-L4', 'note.beamedLeft2-L5', 'note.beamedLeft2-L6', 'note.beamedLeft2-L7', 'note.beamedLeft2-L8', 'note.beamedLeft2-S-1', 'note.beamedLeft2-S-2', 'note.beamedLeft2-S-3', 'note.beamedLeft2-S0', 'note.beamedLeft2-S1', 'note.beamedLeft2-S2', 'note.beamedLeft2-S3', 'note.beamedLeft2-S4', 'note.beamedLeft2-S5', 'note.beamedLeft2-S6', 'note.beamedLeft2-S7', 'note.beamedLeft2-S8', 'note.beamedLeft3-L-1', 'note.beamedLeft3-L-2', 'note.beamedLeft3-L0', 'note.beamedLeft3-L1', 'note.beamedLeft3-L2', 'note.beamedLeft3-L3', 'note.beamedLeft3-L4', 'note.beamedLeft3-L5', 'note.beamedLeft3-L6', 'note.beamedLeft3-L7', 'note.beamedLeft3-L8', 'note.beamedLeft3-S-1', 'note.beamedLeft3-S-2', 'note.beamedLeft3-S0', 'note.beamedLeft3-S1', 'note.beamedLeft3-S2', 'note.beamedLeft3-S3', 'note.beamedLeft3-S4', 'note.beamedLeft3-S5', 'note.beamedLeft3-S6', 'note.beamedLeft3-S7', 'note.beamedLeft3-S8', 'note.beamedLeft4-L0', 'note.beamedLeft4-L1', 'note.beamedLeft4-L2', 'note.beamedLeft4-L3', 'note.beamedLeft4-L4', 'note.beamedLeft4-L5', 'note.beamedLeft4-L6', 'note.beamedLeft4-L7', 'note.beamedLeft4-S-1', 'note.beamedLeft4-S0', 'note.beamedLeft4-S1', 'note.beamedLeft4-S2', 'note.beamedLeft4-S3', 'note.beamedLeft4-S4', 'note.beamedLeft4-S5', 'note.beamedLeft4-S6', 'note.beamedLeft5-S0', 'note.beamedLeft5-S1', 'note.beamedLeft5-S4', 'note.beamedRight0-L0', 'note.beamedRight0-L1', 'note.beamedRight0-L2', 'note.beamedRight0-L3', 'note.beamedRight0-L4', 'note.beamedRight0-L5', 'note.beamedRight0-L6', 'note.beamedRight0-L7', 'note.beamedRight0-S-1', 'note.beamedRight0-S0', 'note.beamedRight0-S1', 'note.beamedRight0-S2', 'note.beamedRight0-S3', 'note.beamedRight0-S4', 'note.beamedRight0-S5', 'note.beamedRight0-S6', 'note.beamedRight0-S7', 'note.beamedRight1-L-1', 'note.beamedRight1-L-2', 'note.beamedRight1-L-3', 'note.beamedRight1-L0', 'note.beamedRight1-L1', 'note.beamedRight1-L2', 'note.beamedRight1-L3', 'note.beamedRight1-L4', 'note.beamedRight1-L5', 'note.beamedRight1-L6', 'note.beamedRight1-L7', 'note.beamedRight1-L8', 'note.beamedRight1-S-1', 'note.beamedRight1-S-2', 'note.beamedRight1-S-3', 'note.beamedRight1-S0', 'note.beamedRight1-S1', 'note.beamedRight1-S2', 'note.beamedRight1-S3', 'note.beamedRight1-S4', 'note.beamedRight1-S5', 'note.beamedRight1-S6', 'note.beamedRight1-S7', 'note.beamedRight1-S8', 'note.beamedRight2-L-1', 'note.beamedRight2-L-2', 'note.beamedRight2-L-3', 'note.beamedRight2-L0', 'note.beamedRight2-L1', 'note.beamedRight2-L2', 'note.beamedRight2-L3', 'note.beamedRight2-L4', 'note.beamedRight2-L5', 'note.beamedRight2-L6', 'note.beamedRight2-L7', 'note.beamedRight2-L8', 'note.beamedRight2-S-1', 'note.beamedRight2-S-2', 'note.beamedRight2-S-3', 'note.beamedRight2-S0', 'note.beamedRight2-S1', 'note.beamedRight2-S2', 'note.beamedRight2-S3', 'note.beamedRight2-S4', 'note.beamedRight2-S5', 'note.beamedRight2-S6', 'note.beamedRight2-S7', 'note.beamedRight2-S8', 'note.beamedRight3-L-1', 'note.beamedRight3-L0', 'note.beamedRight3-L1', 'note.beamedRight3-L2', 'note.beamedRight3-L3', 'note.beamedRight3-L4', 'note.beamedRight3-L5', 'note.beamedRight3-L6', 'note.beamedRight3-L7', 'note.beamedRight3-L8', 'note.beamedRight3-S-1', 'note.beamedRight3-S-2', 'note.beamedRight3-S-3', 'note.beamedRight3-S0', 'note.beamedRight3-S1', 'note.beamedRight3-S2', 'note.beamedRight3-S3', 'note.beamedRight3-S4', 'note.beamedRight3-S5', 'note.beamedRight3-S6', 'note.beamedRight3-S7', 'note.beamedRight3-S8', 'note.beamedRight4-L0', 'note.beamedRight4-L1', 'note.beamedRight4-L2', 'note.beamedRight4-L3', 'note.beamedRight4-L4', 'note.beamedRight4-L5', 'note.beamedRight4-L6', 'note.beamedRight4-L7', 'note.beamedRight4-S-1', 'note.beamedRight4-S-2', 'note.beamedRight4-S0', 'note.beamedRight4-S1', 'note.beamedRight4-S2', 'note.beamedRight4-S3', 'note.beamedRight4-S4', 'note.beamedRight4-S5', 'note.beamedRight4-S6', 'note.beamedRight4-S7', 'note.double_whole-L0', 'note.double_whole-L1', 'note.double_whole-L2', 'note.double_whole-L3', 'note.double_whole-L4', 'note.double_whole-L5', 'note.double_whole-L6', 'note.double_whole-L7', 'note.double_whole-S-1', 'note.double_whole-S0', 'note.double_whole-S1', 'note.double_whole-S2', 'note.double_whole-S3', 'note.double_whole-S4', 'note.double_whole-S5', 'note.double_whole-S6', 'note.double_whole-S7', 'note.eighth-L-1', 'note.eighth-L-2', 'note.eighth-L-3', 'note.eighth-L0', 'note.eighth-L1', 'note.eighth-L2', 'note.eighth-L3', 'note.eighth-L4', 'note.eighth-L5', 'note.eighth-L6', 'note.eighth-L7', 'note.eighth-L8', 'note.eighth-S-1', 'note.eighth-S-2', 'note.eighth-S-3', 'note.eighth-S0', 'note.eighth-S1', 'note.eighth-S2', 'note.eighth-S3', 'note.eighth-S4', 'note.eighth-S5', 'note.eighth-S6', 'note.eighth-S7', 'note.eighth-S8', 'note.half-L-1', 'note.half-L-2', 'note.half-L-3', 'note.half-L0', 'note.half-L1', 'note.half-L2', 'note.half-L3', 'note.half-L4', 'note.half-L5', 'note.half-L6', 'note.half-L7', 'note.half-L8', 'note.half-S-1', 'note.half-S-2', 'note.half-S-3', 'note.half-S0', 'note.half-S1', 'note.half-S2', 'note.half-S3', 'note.half-S4', 'note.half-S5', 'note.half-S6', 'note.half-S7', 'note.half-S8', 'note.quadruple_whole-L1', 'note.quadruple_whole-L2', 'note.quadruple_whole-L3', 'note.quadruple_whole-L4', 'note.quadruple_whole-L5', 'note.quadruple_whole-S0', 'note.quadruple_whole-S1', 'note.quadruple_whole-S2', 'note.quadruple_whole-S3', 'note.quadruple_whole-S4', 'note.quadruple_whole-S5', 'note.quarter-L-1', 'note.quarter-L-2', 'note.quarter-L-3', 'note.quarter-L0', 'note.quarter-L1', 'note.quarter-L2', 'note.quarter-L3', 'note.quarter-L4', 'note.quarter-L5', 'note.quarter-L6', 'note.quarter-L7', 'note.quarter-L8', 'note.quarter-S-1', 'note.quarter-S-2', 'note.quarter-S-3', 'note.quarter-S0', 'note.quarter-S1', 'note.quarter-S2', 'note.quarter-S3', 'note.quarter-S4', 'note.quarter-S5', 'note.quarter-S6', 'note.quarter-S7', 'note.quarter-S8', 'note.sixteenth-L-1', 'note.sixteenth-L-2', 'note.sixteenth-L0', 'note.sixteenth-L1', 'note.sixteenth-L2', 'note.sixteenth-L3', 'note.sixteenth-L4', 'note.sixteenth-L5', 'note.sixteenth-L6', 'note.sixteenth-L7', 'note.sixteenth-L8', 'note.sixteenth-S-1', 'note.sixteenth-S-2', 'note.sixteenth-S0', 'note.sixteenth-S1', 'note.sixteenth-S2', 'note.sixteenth-S3', 'note.sixteenth-S4', 'note.sixteenth-S5', 'note.sixteenth-S6', 'note.sixteenth-S7', 'note.sixteenth-S8', 'note.thirty_second-L-1', 'note.thirty_second-L-2', 'note.thirty_second-L0', 'note.thirty_second-L1', 'note.thirty_second-L2', 'note.thirty_second-L3', 'note.thirty_second-L4', 'note.thirty_second-L5', 'note.thirty_second-L6', 'note.thirty_second-L7', 'note.thirty_second-S-1', 'note.thirty_second-S0', 'note.thirty_second-S1', 'note.thirty_second-S2', 'note.thirty_second-S3', 'note.thirty_second-S4', 'note.thirty_second-S5', 'note.thirty_second-S6', 'note.whole-L-1', 'note.whole-L0', 'note.whole-L1', 'note.whole-L2', 'note.whole-L3', 'note.whole-L4', 'note.whole-L5', 'note.whole-L6', 'note.whole-L7', 'note.whole-S-1', 'note.whole-S-2', 'note.whole-S0', 'note.whole-S1', 'note.whole-S2', 'note.whole-S3', 'note.whole-S4', 'note.whole-S5', 'note.whole-S6', 'note.whole-S7', 'note.whole-S8', 'rest.eighth-L3', 'rest.half-L3', 'rest.quadruple_whole-L3', 'rest.quarter-L3', 'rest.sixteenth-L3', 'rest.sixty_fourth-L3', 'rest.thirty_second-L3', 'rest.whole-L4', 'slur.end-L-1', 'slur.end-L-2', 'slur.end-L0', 'slur.end-L1', 'slur.end-L2', 'slur.end-L3', 'slur.end-L4', 'slur.end-L5', 'slur.end-L6', 'slur.end-L7', 'slur.end-L8', 'slur.end-S-1', 'slur.end-S-2', 'slur.end-S0', 'slur.end-S1', 'slur.end-S2', 'slur.end-S3', 'slur.end-S4', 'slur.end-S5', 'slur.end-S6', 'slur.end-S7', 'slur.start-L-1', 'slur.start-L-2', 'slur.start-L0', 'slur.start-L1', 'slur.start-L2', 'slur.start-L3', 'slur.start-L4', 'slur.start-L5', 'slur.start-L6', 'slur.start-L7', 'slur.start-L8', 'slur.start-S-1', 'slur.start-S-2', 'slur.start-S0', 'slur.start-S1', 'slur.start-S2', 'slur.start-S3', 'slur.start-S4', 'slur.start-S5', 'slur.start-S6', 'slur.start-S7']
    convertor = Sym_conv(data)

    # general symbol type
    convertor._replace_dict(
        {
            'barline-L1': '|',
            'accidental.flat-': 'b',
            'accidental.sharp-': '#',
            'accidental.natural-': '\\',
            'clef.C-': 'c',
            'clef.F-': 'f',
            'clef.G-': 'g',
            'digit.': '',
            'dot-': '.',
            'fermata.above-S6': '^',
            'gracenote.': 'G',
            'note.': 'N',
            'metersign.C-L3': '<',
            'metersign.C/-L3': '>',
            'multirest-L3': 'm',
            'slur.start-': 's',
            'slur.end-': 'e',
            'rest.': 'r',
            '-L': 'L',
            '-S': 'S'
        }
    )

    # Symbol positions
    pos_lines = {f'L{i}': f'/{i * 2}' for i in range(10)}
    pos_neg_lines = {f'L-{i}': f'/-{i * 2}' for i in range(4)}
    pos_spaces = {f'S{i}': f'/{(i * 2) - 1}' for i in range(10)}
    pos_neg_spaces = {f'S-{i}': f'/-{(i * 2) + 1}' for i in range(1, 4)}

    convertor._replace_dict(pos_lines)
    convertor._replace_dict(pos_neg_lines)
    convertor._replace_dict(pos_spaces)
    convertor._replace_dict(pos_neg_spaces)

    # symbol (notes, gracenotes, rest...) lengths
    convertor._replace_dict({
        'beamedBoth': 'B',
        'beamedLeft': 'L',
        'beamedRight': 'R',
        'double_whole': 'D',
        'eighth': 'E',
        'half': 'H',
        'quarter': 'q',
        'quadruple_whole': 'Q',
        'thirty_second': 'T',
        'hundred_twenty': 'h',
        'sixteenth': 'S',
        'sixty_fourth': 's',
        'whole': 'W'
        })

    convertor.finalize()

    # %%


if __name__ == '__main__':
    main()

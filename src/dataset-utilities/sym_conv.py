"""NOT A STAND-ALONE script... 
    It was used Manually as a in-line script for simpler creation 
    of symbol conversion dictionary.
"""

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

    def replace_two_lists(self, keys: list, values: list):
        assert len(keys) == len(values), (f"Lists muset have same length. "
                                          f"Keys: {len(keys)} values: {len(values)}")
        for k, v in zip(keys, values):
            self._replace(k, v)

    def replace_dict(self, dictos: dict = {}):
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
            print(f'WARNING: Repeated symbols are: {self.repeated}')

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
    agnotic_data = ['accidental.flat-L-1', 'accidental.flat-L0', 'accidental.flat-L1', 'accidental.flat-L2', 'accidental.flat-L3', 'accidental.flat-L4', 'accidental.flat-L5', 'accidental.flat-L6', 'accidental.flat-L7', 'accidental.flat-L8', 'accidental.flat-S-1', 'accidental.flat-S-2', 'accidental.flat-S0', 'accidental.flat-S1', 'accidental.flat-S2', 'accidental.flat-S3', 'accidental.flat-S4', 'accidental.flat-S5', 'accidental.flat-S6', 'accidental.flat-S7', 'accidental.natural-L-1', 'accidental.natural-L-2', 'accidental.natural-L0', 'accidental.natural-L1', 'accidental.natural-L2', 'accidental.natural-L3', 'accidental.natural-L4', 'accidental.natural-L5', 'accidental.natural-L6', 'accidental.natural-L7', 'accidental.natural-L8', 'accidental.natural-S-1', 'accidental.natural-S-2', 'accidental.natural-S-3', 'accidental.natural-S0', 'accidental.natural-S1', 'accidental.natural-S2', 'accidental.natural-S3', 'accidental.natural-S4', 'accidental.natural-S5', 'accidental.natural-S6', 'accidental.natural-S7', 'accidental.sharp-L-1', 'accidental.sharp-L-2', 'accidental.sharp-L0', 'accidental.sharp-L1', 'accidental.sharp-L2', 'accidental.sharp-L3', 'accidental.sharp-L4', 'accidental.sharp-L5', 'accidental.sharp-L6', 'accidental.sharp-L7', 'accidental.sharp-L8', 'accidental.sharp-S-1', 'accidental.sharp-S-2', 'accidental.sharp-S0', 'accidental.sharp-S1', 'accidental.sharp-S2', 'accidental.sharp-S3', 'accidental.sharp-S4', 'accidental.sharp-S5', 'accidental.sharp-S6', 'accidental.sharp-S7', 'accidental.sharp-S8', 'barline-L1', 'clef.C-L1', 'clef.C-L2', 'clef.C-L3', 'clef.C-L4', 'clef.C-L5', 'clef.F-L3', 'clef.F-L4', 'clef.F-L5', 'clef.G-L1', 'clef.G-L2', 'digit.0-S5', 'digit.1-L2', 'digit.1-L4', 'digit.1-S5', 'digit.11-L4', 'digit.12-L2', 'digit.12-L4', 'digit.16-L2', 'digit.2-L2', 'digit.2-L4', 'digit.2-S5', 'digit.24-L4', 'digit.3-L2', 'digit.3-L4', 'digit.3-S5', 'digit.4-L2', 'digit.4-L4', 'digit.4-S5', 'digit.48-L2', 'digit.5-L4', 'digit.5-S5', 'digit.6-L2', 'digit.6-L4', 'digit.6-S5', 'digit.7-L4', 'digit.7-S5', 'digit.8-L2', 'digit.8-L4', 'digit.8-S5', 'digit.9-L4', 'digit.9-S5', 'dot-S-1', 'dot-S-2', 'dot-S-3', 'dot-S0', 'dot-S1', 'dot-S2', 'dot-S3', 'dot-S4', 'dot-S5', 'dot-S6', 'dot-S7', 'dot-S8', 'fermata.above-S6', 'gracenote.beamedBoth1-L1', 'gracenote.beamedBoth1-L2', 'gracenote.beamedBoth1-L3', 'gracenote.beamedBoth1-L4', 'gracenote.beamedBoth1-L5', 'gracenote.beamedBoth1-L6', 'gracenote.beamedBoth1-S0', 'gracenote.beamedBoth1-S1', 'gracenote.beamedBoth1-S2', 'gracenote.beamedBoth1-S3', 'gracenote.beamedBoth1-S4', 'gracenote.beamedBoth1-S5', 'gracenote.beamedBoth2-L-1', 'gracenote.beamedBoth2-L0', 'gracenote.beamedBoth2-L1', 'gracenote.beamedBoth2-L2', 'gracenote.beamedBoth2-L3', 'gracenote.beamedBoth2-L4', 'gracenote.beamedBoth2-L5', 'gracenote.beamedBoth2-L6', 'gracenote.beamedBoth2-S-1', 'gracenote.beamedBoth2-S0', 'gracenote.beamedBoth2-S1', 'gracenote.beamedBoth2-S2', 'gracenote.beamedBoth2-S3', 'gracenote.beamedBoth2-S4', 'gracenote.beamedBoth2-S5', 'gracenote.beamedBoth3-L1', 'gracenote.beamedBoth3-L2', 'gracenote.beamedBoth3-L3', 'gracenote.beamedBoth3-L4', 'gracenote.beamedBoth3-L5', 'gracenote.beamedBoth3-L6', 'gracenote.beamedBoth3-S1', 'gracenote.beamedBoth3-S2', 'gracenote.beamedBoth3-S3', 'gracenote.beamedBoth3-S4', 'gracenote.beamedBoth3-S5', 'gracenote.beamedRight0-S2', 'gracenote.beamedRight1-L5', 'gracenote.double_whole-L5', 'gracenote.eighth-L-1', 'gracenote.eighth-L0', 'gracenote.eighth-L1', 'gracenote.eighth-L2', 'gracenote.eighth-L3', 'gracenote.eighth-L4', 'gracenote.eighth-L5', 'gracenote.eighth-L6', 'gracenote.eighth-S-1', 'gracenote.eighth-S0', 'gracenote.eighth-S1', 'gracenote.eighth-S2', 'gracenote.eighth-S3', 'gracenote.eighth-S4', 'gracenote.eighth-S5', 'gracenote.half-L2', 'gracenote.half-L3', 'gracenote.half-L4', 'gracenote.half-L5', 'gracenote.half-L6', 'gracenote.half-S2', 'gracenote.half-S3', 'gracenote.half-S4', 'gracenote.half-S5', 'gracenote.quarter-L0', 'gracenote.quarter-L1', 'gracenote.quarter-L2', 'gracenote.quarter-L3', 'gracenote.quarter-L4', 'gracenote.quarter-L5', 'gracenote.quarter-L6', 'gracenote.quarter-S0', 'gracenote.quarter-S1', 'gracenote.quarter-S2', 'gracenote.quarter-S3', 'gracenote.quarter-S4', 'gracenote.quarter-S5', 'gracenote.sixteenth-L-1', 'gracenote.sixteenth-L-2', 'gracenote.sixteenth-L0', 'gracenote.sixteenth-L1', 'gracenote.sixteenth-L2', 'gracenote.sixteenth-L3', 'gracenote.sixteenth-L4', 'gracenote.sixteenth-L5', 'gracenote.sixteenth-L6', 'gracenote.sixteenth-S-1', 'gracenote.sixteenth-S-2', 'gracenote.sixteenth-S0', 'gracenote.sixteenth-S1', 'gracenote.sixteenth-S2', 'gracenote.sixteenth-S3', 'gracenote.sixteenth-S4', 'gracenote.sixteenth-S5', 'gracenote.thirty_second-L-1', 'gracenote.thirty_second-L0', 'gracenote.thirty_second-L1', 'gracenote.thirty_second-L2', 'gracenote.thirty_second-L3', 'gracenote.thirty_second-L4', 'gracenote.thirty_second-L5', 'gracenote.thirty_second-L6', 'gracenote.thirty_second-S-1', 'gracenote.thirty_second-S-2', 'gracenote.thirty_second-S0', 'gracenote.thirty_second-S1', 'gracenote.thirty_second-S2', 'gracenote.thirty_second-S3', 'gracenote.thirty_second-S4', 'gracenote.thirty_second-S5', 'metersign.C-L3', 'metersign.C/-L3', 'multirest-L3', 'note.beamedBoth0-L0', 'note.beamedBoth0-L1', 'note.beamedBoth0-L2', 'note.beamedBoth0-L3', 'note.beamedBoth0-L4', 'note.beamedBoth0-L5', 'note.beamedBoth0-L6', 'note.beamedBoth0-L7', 'note.beamedBoth0-S-1', 'note.beamedBoth0-S-3', 'note.beamedBoth0-S0', 'note.beamedBoth0-S1', 'note.beamedBoth0-S2', 'note.beamedBoth0-S3', 'note.beamedBoth0-S4', 'note.beamedBoth0-S5', 'note.beamedBoth0-S6', 'note.beamedBoth1-L-1', 'note.beamedBoth1-L-2', 'note.beamedBoth1-L-3', 'note.beamedBoth1-L0', 'note.beamedBoth1-L1', 'note.beamedBoth1-L2', 'note.beamedBoth1-L3', 'note.beamedBoth1-L4', 'note.beamedBoth1-L5', 'note.beamedBoth1-L6', 'note.beamedBoth1-L7', 'note.beamedBoth1-L8', 'note.beamedBoth1-S-1', 'note.beamedBoth1-S-2', 'note.beamedBoth1-S-3', 'note.beamedBoth1-S0', 'note.beamedBoth1-S1', 'note.beamedBoth1-S2', 'note.beamedBoth1-S3', 'note.beamedBoth1-S4', 'note.beamedBoth1-S5', 'note.beamedBoth1-S6', 'note.beamedBoth1-S7', 'note.beamedBoth1-S8', 'note.beamedBoth2-L-1', 'note.beamedBoth2-L-2', 'note.beamedBoth2-L-3', 'note.beamedBoth2-L0', 'note.beamedBoth2-L1', 'note.beamedBoth2-L2', 'note.beamedBoth2-L3', 'note.beamedBoth2-L4', 'note.beamedBoth2-L5', 'note.beamedBoth2-L6', 'note.beamedBoth2-L7', 'note.beamedBoth2-L8', 'note.beamedBoth2-S-1', 'note.beamedBoth2-S-2', 'note.beamedBoth2-S-3', 'note.beamedBoth2-S0', 'note.beamedBoth2-S1', 'note.beamedBoth2-S2', 'note.beamedBoth2-S3', 'note.beamedBoth2-S4', 'note.beamedBoth2-S5', 'note.beamedBoth2-S6', 'note.beamedBoth2-S7', 'note.beamedBoth2-S8', 'note.beamedBoth3-L-1', 'note.beamedBoth3-L-2', 'note.beamedBoth3-L0', 'note.beamedBoth3-L1', 'note.beamedBoth3-L2', 'note.beamedBoth3-L3', 'note.beamedBoth3-L4', 'note.beamedBoth3-L5', 'note.beamedBoth3-L6', 'note.beamedBoth3-L7', 'note.beamedBoth3-L8', 'note.beamedBoth3-S-1', 'note.beamedBoth3-S-2', 'note.beamedBoth3-S0', 'note.beamedBoth3-S1', 'note.beamedBoth3-S2', 'note.beamedBoth3-S3', 'note.beamedBoth3-S4', 'note.beamedBoth3-S5', 'note.beamedBoth3-S6', 'note.beamedBoth3-S7', 'note.beamedBoth3-S8', 'note.beamedBoth4-L-1', 'note.beamedBoth4-L0', 'note.beamedBoth4-L1', 'note.beamedBoth4-L2', 'note.beamedBoth4-L3', 'note.beamedBoth4-L4', 'note.beamedBoth4-L5', 'note.beamedBoth4-L6', 'note.beamedBoth4-L7', 'note.beamedBoth4-S-1', 'note.beamedBoth4-S0', 'note.beamedBoth4-S1', 'note.beamedBoth4-S2', 'note.beamedBoth4-S3', 'note.beamedBoth4-S4', 'note.beamedBoth4-S5', 'note.beamedBoth4-S6', 'note.beamedBoth4-S7', 'note.beamedBoth5-L0', 'note.beamedBoth5-L1', 'note.beamedLeft0-L1', 'note.beamedLeft0-L2', 'note.beamedLeft0-L3', 'note.beamedLeft0-L4', 'note.beamedLeft0-L5', 'note.beamedLeft0-L6', 'note.beamedLeft0-L7', 'note.beamedLeft0-S-2', 'note.beamedLeft0-S-3', 'note.beamedLeft0-S1', 'note.beamedLeft0-S2', 'note.beamedLeft0-S3', 'note.beamedLeft0-S4', 'note.beamedLeft0-S5', 'note.beamedLeft0-S6', 'note.beamedLeft0-S7', 'note.beamedLeft1-L-1', 'note.beamedLeft1-L-2', 'note.beamedLeft1-L0', 'note.beamedLeft1-L1', 'note.beamedLeft1-L2', 'note.beamedLeft1-L3', 'note.beamedLeft1-L4', 'note.beamedLeft1-L5', 'note.beamedLeft1-L6', 'note.beamedLeft1-L7', 'note.beamedLeft1-L8', 'note.beamedLeft1-S-1', 'note.beamedLeft1-S-2', 'note.beamedLeft1-S-3', 'note.beamedLeft1-S0', 'note.beamedLeft1-S1', 'note.beamedLeft1-S2', 'note.beamedLeft1-S3', 'note.beamedLeft1-S4', 'note.beamedLeft1-S5', 'note.beamedLeft1-S6', 'note.beamedLeft1-S7', 'note.beamedLeft1-S8', 'note.beamedLeft2-L-1', 'note.beamedLeft2-L-2', 'note.beamedLeft2-L0', 'note.beamedLeft2-L1', 'note.beamedLeft2-L2', 'note.beamedLeft2-L3', 'note.beamedLeft2-L4', 'note.beamedLeft2-L5', 'note.beamedLeft2-L6', 'note.beamedLeft2-L7', 'note.beamedLeft2-L8', 'note.beamedLeft2-S-1', 'note.beamedLeft2-S-2', 'note.beamedLeft2-S-3', 'note.beamedLeft2-S0', 'note.beamedLeft2-S1', 'note.beamedLeft2-S2', 'note.beamedLeft2-S3', 'note.beamedLeft2-S4', 'note.beamedLeft2-S5', 'note.beamedLeft2-S6', 'note.beamedLeft2-S7', 'note.beamedLeft2-S8', 'note.beamedLeft3-L-1', 'note.beamedLeft3-L-2', 'note.beamedLeft3-L0', 'note.beamedLeft3-L1', 'note.beamedLeft3-L2', 'note.beamedLeft3-L3', 'note.beamedLeft3-L4', 'note.beamedLeft3-L5', 'note.beamedLeft3-L6', 'note.beamedLeft3-L7', 'note.beamedLeft3-L8', 'note.beamedLeft3-S-1', 'note.beamedLeft3-S-2', 'note.beamedLeft3-S0', 'note.beamedLeft3-S1', 'note.beamedLeft3-S2', 'note.beamedLeft3-S3', 'note.beamedLeft3-S4', 'note.beamedLeft3-S5', 'note.beamedLeft3-S6', 'note.beamedLeft3-S7', 'note.beamedLeft3-S8', 'note.beamedLeft4-L0', 'note.beamedLeft4-L1', 'note.beamedLeft4-L2', 'note.beamedLeft4-L3', 'note.beamedLeft4-L4', 'note.beamedLeft4-L5', 'note.beamedLeft4-L6', 'note.beamedLeft4-L7', 'note.beamedLeft4-S-1', 'note.beamedLeft4-S0', 'note.beamedLeft4-S1', 'note.beamedLeft4-S2', 'note.beamedLeft4-S3', 'note.beamedLeft4-S4', 'note.beamedLeft4-S5', 'note.beamedLeft4-S6', 'note.beamedLeft5-S0', 'note.beamedLeft5-S1', 'note.beamedLeft5-S4', 'note.beamedRight0-L0', 'note.beamedRight0-L1', 'note.beamedRight0-L2', 'note.beamedRight0-L3', 'note.beamedRight0-L4', 'note.beamedRight0-L5', 'note.beamedRight0-L6', 'note.beamedRight0-L7', 'note.beamedRight0-S-1', 'note.beamedRight0-S0', 'note.beamedRight0-S1', 'note.beamedRight0-S2', 'note.beamedRight0-S3', 'note.beamedRight0-S4', 'note.beamedRight0-S5', 'note.beamedRight0-S6', 'note.beamedRight0-S7', 'note.beamedRight1-L-1', 'note.beamedRight1-L-2', 'note.beamedRight1-L-3', 'note.beamedRight1-L0', 'note.beamedRight1-L1', 'note.beamedRight1-L2', 'note.beamedRight1-L3', 'note.beamedRight1-L4', 'note.beamedRight1-L5', 'note.beamedRight1-L6', 'note.beamedRight1-L7', 'note.beamedRight1-L8', 'note.beamedRight1-S-1', 'note.beamedRight1-S-2', 'note.beamedRight1-S-3', 'note.beamedRight1-S0', 'note.beamedRight1-S1', 'note.beamedRight1-S2', 'note.beamedRight1-S3', 'note.beamedRight1-S4', 'note.beamedRight1-S5', 'note.beamedRight1-S6', 'note.beamedRight1-S7', 'note.beamedRight1-S8', 'note.beamedRight2-L-1', 'note.beamedRight2-L-2', 'note.beamedRight2-L-3', 'note.beamedRight2-L0', 'note.beamedRight2-L1', 'note.beamedRight2-L2', 'note.beamedRight2-L3', 'note.beamedRight2-L4', 'note.beamedRight2-L5', 'note.beamedRight2-L6', 'note.beamedRight2-L7', 'note.beamedRight2-L8', 'note.beamedRight2-S-1', 'note.beamedRight2-S-2', 'note.beamedRight2-S-3', 'note.beamedRight2-S0', 'note.beamedRight2-S1', 'note.beamedRight2-S2', 'note.beamedRight2-S3', 'note.beamedRight2-S4', 'note.beamedRight2-S5', 'note.beamedRight2-S6', 'note.beamedRight2-S7', 'note.beamedRight2-S8', 'note.beamedRight3-L-1', 'note.beamedRight3-L0', 'note.beamedRight3-L1', 'note.beamedRight3-L2', 'note.beamedRight3-L3', 'note.beamedRight3-L4', 'note.beamedRight3-L5', 'note.beamedRight3-L6', 'note.beamedRight3-L7', 'note.beamedRight3-L8', 'note.beamedRight3-S-1', 'note.beamedRight3-S-2', 'note.beamedRight3-S-3', 'note.beamedRight3-S0', 'note.beamedRight3-S1', 'note.beamedRight3-S2', 'note.beamedRight3-S3', 'note.beamedRight3-S4', 'note.beamedRight3-S5', 'note.beamedRight3-S6', 'note.beamedRight3-S7', 'note.beamedRight3-S8', 'note.beamedRight4-L0', 'note.beamedRight4-L1', 'note.beamedRight4-L2', 'note.beamedRight4-L3', 'note.beamedRight4-L4', 'note.beamedRight4-L5', 'note.beamedRight4-L6', 'note.beamedRight4-L7', 'note.beamedRight4-S-1', 'note.beamedRight4-S-2', 'note.beamedRight4-S0', 'note.beamedRight4-S1', 'note.beamedRight4-S2', 'note.beamedRight4-S3', 'note.beamedRight4-S4', 'note.beamedRight4-S5', 'note.beamedRight4-S6', 'note.beamedRight4-S7', 'note.double_whole-L0', 'note.double_whole-L1', 'note.double_whole-L2', 'note.double_whole-L3', 'note.double_whole-L4', 'note.double_whole-L5', 'note.double_whole-L6', 'note.double_whole-L7', 'note.double_whole-S-1', 'note.double_whole-S0', 'note.double_whole-S1', 'note.double_whole-S2', 'note.double_whole-S3', 'note.double_whole-S4', 'note.double_whole-S5', 'note.double_whole-S6', 'note.double_whole-S7', 'note.eighth-L-1', 'note.eighth-L-2', 'note.eighth-L-3', 'note.eighth-L0', 'note.eighth-L1', 'note.eighth-L2', 'note.eighth-L3', 'note.eighth-L4', 'note.eighth-L5', 'note.eighth-L6', 'note.eighth-L7', 'note.eighth-L8', 'note.eighth-S-1', 'note.eighth-S-2', 'note.eighth-S-3', 'note.eighth-S0', 'note.eighth-S1', 'note.eighth-S2', 'note.eighth-S3', 'note.eighth-S4', 'note.eighth-S5', 'note.eighth-S6', 'note.eighth-S7', 'note.eighth-S8', 'note.half-L-1', 'note.half-L-2', 'note.half-L-3', 'note.half-L0', 'note.half-L1', 'note.half-L2', 'note.half-L3', 'note.half-L4', 'note.half-L5', 'note.half-L6', 'note.half-L7', 'note.half-L8', 'note.half-S-1', 'note.half-S-2', 'note.half-S-3', 'note.half-S0', 'note.half-S1', 'note.half-S2', 'note.half-S3', 'note.half-S4', 'note.half-S5', 'note.half-S6', 'note.half-S7', 'note.half-S8', 'note.quadruple_whole-L1', 'note.quadruple_whole-L2', 'note.quadruple_whole-L3', 'note.quadruple_whole-L4', 'note.quadruple_whole-L5', 'note.quadruple_whole-S0', 'note.quadruple_whole-S1', 'note.quadruple_whole-S2', 'note.quadruple_whole-S3', 'note.quadruple_whole-S4', 'note.quadruple_whole-S5', 'note.quarter-L-1', 'note.quarter-L-2', 'note.quarter-L-3', 'note.quarter-L0', 'note.quarter-L1', 'note.quarter-L2', 'note.quarter-L3', 'note.quarter-L4', 'note.quarter-L5', 'note.quarter-L6', 'note.quarter-L7', 'note.quarter-L8', 'note.quarter-S-1', 'note.quarter-S-2', 'note.quarter-S-3', 'note.quarter-S0', 'note.quarter-S1', 'note.quarter-S2', 'note.quarter-S3', 'note.quarter-S4', 'note.quarter-S5', 'note.quarter-S6', 'note.quarter-S7', 'note.quarter-S8', 'note.sixteenth-L-1', 'note.sixteenth-L-2', 'note.sixteenth-L0', 'note.sixteenth-L1', 'note.sixteenth-L2', 'note.sixteenth-L3', 'note.sixteenth-L4', 'note.sixteenth-L5', 'note.sixteenth-L6', 'note.sixteenth-L7', 'note.sixteenth-L8', 'note.sixteenth-S-1', 'note.sixteenth-S-2', 'note.sixteenth-S0', 'note.sixteenth-S1', 'note.sixteenth-S2', 'note.sixteenth-S3', 'note.sixteenth-S4', 'note.sixteenth-S5', 'note.sixteenth-S6', 'note.sixteenth-S7', 'note.sixteenth-S8', 'note.thirty_second-L-1', 'note.thirty_second-L-2', 'note.thirty_second-L0', 'note.thirty_second-L1', 'note.thirty_second-L2', 'note.thirty_second-L3', 'note.thirty_second-L4', 'note.thirty_second-L5', 'note.thirty_second-L6', 'note.thirty_second-L7', 'note.thirty_second-S-1', 'note.thirty_second-S0', 'note.thirty_second-S1', 'note.thirty_second-S2', 'note.thirty_second-S3', 'note.thirty_second-S4', 'note.thirty_second-S5', 'note.thirty_second-S6', 'note.whole-L-1', 'note.whole-L0', 'note.whole-L1', 'note.whole-L2', 'note.whole-L3', 'note.whole-L4', 'note.whole-L5', 'note.whole-L6', 'note.whole-L7', 'note.whole-S-1', 'note.whole-S-2', 'note.whole-S0', 'note.whole-S1', 'note.whole-S2', 'note.whole-S3', 'note.whole-S4', 'note.whole-S5', 'note.whole-S6', 'note.whole-S7', 'note.whole-S8', 'rest.eighth-L3', 'rest.half-L3', 'rest.quadruple_whole-L3', 'rest.quarter-L3', 'rest.sixteenth-L3', 'rest.sixty_fourth-L3', 'rest.thirty_second-L3', 'rest.whole-L4', 'slur.end-L-1', 'slur.end-L-2', 'slur.end-L0', 'slur.end-L1', 'slur.end-L2', 'slur.end-L3', 'slur.end-L4', 'slur.end-L5', 'slur.end-L6', 'slur.end-L7', 'slur.end-L8', 'slur.end-S-1', 'slur.end-S-2', 'slur.end-S0', 'slur.end-S1', 'slur.end-S2', 'slur.end-S3', 'slur.end-S4', 'slur.end-S5', 'slur.end-S6', 'slur.end-S7', 'slur.start-L-1', 'slur.start-L-2', 'slur.start-L0', 'slur.start-L1', 'slur.start-L2', 'slur.start-L3', 'slur.start-L4', 'slur.start-L5', 'slur.start-L6', 'slur.start-L7', 'slur.start-L8', 'slur.start-S-1', 'slur.start-S-2', 'slur.start-S0', 'slur.start-S1', 'slur.start-S2', 'slur.start-S3', 'slur.start-S4', 'slur.start-S5', 'slur.start-S6', 'slur.start-S7']
    semantic_data = [
        "barline",
        "multirest-1", "multirest-10", "multirest-100", "multirest-105", "multirest-107", "multirest-11", "multirest-1111", "multirest-112", "multirest-115", "multirest-119", "multirest-12", "multirest-123", "multirest-124", "multirest-126", "multirest-128", "multirest-13", "multirest-14", "multirest-143", "multirest-15", "multirest-16", "multirest-164", "multirest-17", "multirest-18", "multirest-19", "multirest-193", "multirest-2", "multirest-20", "multirest-21", "multirest-22", "multirest-225", "multirest-23", "multirest-24", "multirest-25", "multirest-26", "multirest-27", "multirest-28", "multirest-29", "multirest-3", "multirest-30", "multirest-31", "multirest-32", "multirest-33", "multirest-34", "multirest-35", "multirest-36", "multirest-37", "multirest-38", "multirest-39", "multirest-4", "multirest-40", "multirest-41", "multirest-42", "multirest-43", "multirest-44", "multirest-45", "multirest-46", "multirest-47", "multirest-48", "multirest-49", "multirest-5", "multirest-50", "multirest-51", "multirest-52", "multirest-53", "multirest-54", "multirest-55", "multirest-56", "multirest-57", "multirest-58", "multirest-59", "multirest-6", "multirest-60", "multirest-63", "multirest-64", "multirest-65", "multirest-66", "multirest-67", "multirest-68", "multirest-69", "multirest-7", "multirest-70", "multirest-71", "multirest-72", "multirest-73", "multirest-76", "multirest-77", "multirest-79", "multirest-8", "multirest-80", "multirest-81", "multirest-88", "multirest-89", "multirest-9", "multirest-91", "multirest-94", "multirest-96", "multirest-98", "multirest-99", 
        "clef-C1", "clef-C2", "clef-C3", "clef-C4", "clef-C5", "clef-F3", "clef-F4", "clef-F5", "clef-G1", "clef-G2",
        "keySignature-AM", "keySignature-AbM", "keySignature-BM", "keySignature-BbM", "keySignature-C#M", "keySignature-CM", "keySignature-DM", "keySignature-DbM", "keySignature-EM", "keySignature-EbM", "keySignature-F#M", "keySignature-FM", "keySignature-GM", "keySignature-GbM",
        "tie",
        "rest-eighth", "rest-eighth.", "rest-eighth..", "rest-eighth._fermata", "rest-eighth_fermata", "rest-half", "rest-half.", "rest-half._fermata", "rest-half_fermata", "rest-quadruple_whole", "rest-quarter", "rest-quarter.", "rest-quarter..", "rest-quarter.._fermata", "rest-quarter._fermata", "rest-quarter_fermata", "rest-sixteenth", "rest-sixteenth.", "rest-sixteenth_fermata", "rest-sixty_fourth", "rest-thirty_second", "rest-whole", "rest-whole.", "rest-whole_fermata",
        "gracenote-A#3_eighth", "gracenote-A#3_sixteenth", "gracenote-A#4_eighth", "gracenote-A#4_half", "gracenote-A#4_quarter", "gracenote-A#4_sixteenth", "gracenote-A#4_thirty_second", "gracenote-A#5_eighth", "gracenote-A2_eighth", "gracenote-A2_quarter", "gracenote-A2_sixteenth", "gracenote-A3_eighth", "gracenote-A3_half", "gracenote-A3_quarter", "gracenote-A3_sixteenth", "gracenote-A3_thirty_second", "gracenote-A4_eighth", "gracenote-A4_half", "gracenote-A4_quarter", "gracenote-A4_sixteenth", "gracenote-A4_thirty_second", "gracenote-A5_eighth", "gracenote-A5_quarter", "gracenote-A5_sixteenth", "gracenote-A5_sixteenth.", "gracenote-A5_thirty_second", "gracenote-Ab3_double_whole", "gracenote-Ab3_eighth", "gracenote-Ab3_sixteenth", "gracenote-Ab3_thirty_second", "gracenote-Ab4_eighth", "gracenote-Ab4_half", "gracenote-Ab4_quarter", "gracenote-Ab4_sixteenth", "gracenote-Ab4_thirty_second", "gracenote-Ab5_eighth", "gracenote-Ab5_quarter", "gracenote-Ab5_sixteenth", "gracenote-Ab5_thirty_second", "gracenote-B#3_sixteenth", "gracenote-B#4_eighth", "gracenote-B#4_quarter", "gracenote-B#4_sixteenth", "gracenote-B2_sixteenth", "gracenote-B3_eighth", "gracenote-B3_quarter", "gracenote-B3_sixteenth", "gracenote-B3_thirty_second", "gracenote-B4_eighth", "gracenote-B4_quarter", "gracenote-B4_sixteenth", "gracenote-B4_sixteenth.", "gracenote-B4_thirty_second", "gracenote-B5_eighth", "gracenote-Bb3_eighth", "gracenote-Bb3_quarter", "gracenote-Bb3_sixteenth", "gracenote-Bb3_thirty_second", "gracenote-Bb4_eighth", "gracenote-Bb4_eighth.", "gracenote-Bb4_half", "gracenote-Bb4_quarter", "gracenote-Bb4_sixteenth", "gracenote-Bb4_thirty_second", "gracenote-Bb5_eighth", "gracenote-C#3_eighth", "gracenote-C#3_sixteenth", "gracenote-C#4_eighth", "gracenote-C#4_eighth.", "gracenote-C#4_quarter", "gracenote-C#4_sixteenth", "gracenote-C#4_thirty_second", "gracenote-C#5_eighth", "gracenote-C#5_eighth.", "gracenote-C#5_half", "gracenote-C#5_quarter", "gracenote-C#5_sixteenth", "gracenote-C#5_sixteenth.", "gracenote-C#5_thirty_second", "gracenote-C3_eighth", "gracenote-C3_quarter", "gracenote-C3_sixteenth", "gracenote-C4_eighth", "gracenote-C4_quarter", "gracenote-C4_sixteenth", "gracenote-C4_thirty_second", "gracenote-C5_eighth", "gracenote-C5_half", "gracenote-C5_quarter", "gracenote-C5_sixteenth", "gracenote-C5_thirty_second", "gracenote-Cb5_eighth", "gracenote-Cb5_quarter", "gracenote-Cb5_thirty_second", "gracenote-D#3_quarter", "gracenote-D#3_sixteenth", "gracenote-D#4_eighth", "gracenote-D#4_quarter", "gracenote-D#4_sixteenth", "gracenote-D#4_thirty_second", "gracenote-D#5_eighth", "gracenote-D#5_quarter", "gracenote-D#5_sixteenth", "gracenote-D#5_thirty_second", "gracenote-D3_eighth", "gracenote-D3_quarter", "gracenote-D3_sixteenth", "gracenote-D4_eighth", "gracenote-D4_quarter", "gracenote-D4_sixteenth", "gracenote-D4_thirty_second", "gracenote-D5_eighth", "gracenote-D5_half", "gracenote-D5_quarter", "gracenote-D5_sixteenth", "gracenote-D5_sixteenth.", "gracenote-D5_thirty_second", "gracenote-Db4_eighth", "gracenote-Db4_sixteenth", "gracenote-Db5_eighth", "gracenote-Db5_half", "gracenote-Db5_quarter", "gracenote-Db5_sixteenth", "gracenote-Db5_thirty_second", "gracenote-E#4_eighth", "gracenote-E#4_sixteenth", "gracenote-E#5_eighth", "gracenote-E#5_quarter", "gracenote-E#5_sixteenth", "gracenote-E3_eighth", "gracenote-E3_quarter", "gracenote-E3_sixteenth", "gracenote-E4_eighth", "gracenote-E4_quarter", "gracenote-E4_sixteenth", "gracenote-E4_thirty_second", "gracenote-E5_eighth", "gracenote-E5_half", "gracenote-E5_quarter", "gracenote-E5_sixteenth", "gracenote-E5_thirty_second", "gracenote-Eb3_eighth", "gracenote-Eb3_quarter", "gracenote-Eb3_sixteenth", "gracenote-Eb4_eighth", "gracenote-Eb4_quarter", "gracenote-Eb4_sixteenth", "gracenote-Eb4_thirty_second", "gracenote-Eb5_eighth", "gracenote-Eb5_quarter", "gracenote-Eb5_quarter.", "gracenote-Eb5_sixteenth", "gracenote-Eb5_thirty_second", "gracenote-F#2_quarter", "gracenote-F#3_eighth", "gracenote-F#3_quarter", "gracenote-F#3_sixteenth", "gracenote-F#4_eighth", "gracenote-F#4_quarter", "gracenote-F#4_sixteenth", "gracenote-F#4_thirty_second", "gracenote-F#5_eighth", "gracenote-F#5_quarter", "gracenote-F#5_sixteenth", "gracenote-F#5_thirty_second", "gracenote-F2_eighth", "gracenote-F3_eighth", "gracenote-F3_quarter", "gracenote-F3_sixteenth", "gracenote-F3_thirty_second", "gracenote-F4_eighth", "gracenote-F4_quarter", "gracenote-F4_sixteenth", "gracenote-F4_thirty_second", "gracenote-F5_eighth", "gracenote-F5_half", "gracenote-F5_quarter", "gracenote-F5_sixteenth", "gracenote-F5_sixteenth.", "gracenote-F5_thirty_second", "gracenote-G#3_eighth", "gracenote-G#3_sixteenth", "gracenote-G#3_thirty_second", "gracenote-G#4_eighth", "gracenote-G#4_quarter", "gracenote-G#4_sixteenth", "gracenote-G#4_thirty_second", "gracenote-G#5_eighth", "gracenote-G#5_quarter", "gracenote-G#5_sixteenth", "gracenote-G#5_thirty_second", "gracenote-G3_eighth", "gracenote-G3_quarter", "gracenote-G3_sixteenth", "gracenote-G3_thirty_second", "gracenote-G4_eighth", "gracenote-G4_eighth.", "gracenote-G4_half", "gracenote-G4_quarter", "gracenote-G4_sixteenth", "gracenote-G4_thirty_second", "gracenote-G5_eighth", "gracenote-G5_half", "gracenote-G5_quarter", "gracenote-G5_sixteenth", "gracenote-G5_sixteenth.", "gracenote-G5_thirty_second", "gracenote-Gb4_eighth", "gracenote-Gb4_quarter", "gracenote-Gb5_thirty_second",
        "timeSignature-1/2", "timeSignature-1/4", "timeSignature-11/4", "timeSignature-12/16", "timeSignature-12/4", "timeSignature-12/8", "timeSignature-2/1", "timeSignature-2/2", "timeSignature-2/3", "timeSignature-2/4", "timeSignature-2/48", "timeSignature-2/8", "timeSignature-24/16", "timeSignature-3/1", "timeSignature-3/2", "timeSignature-3/4", "timeSignature-3/6", "timeSignature-3/8", "timeSignature-4/1", "timeSignature-4/2", "timeSignature-4/4", "timeSignature-4/8", "timeSignature-5/4", "timeSignature-5/8", "timeSignature-6/16", "timeSignature-6/2", "timeSignature-6/4", "timeSignature-6/8", "timeSignature-7/4", "timeSignature-8/12", "timeSignature-8/16", "timeSignature-8/2", "timeSignature-8/4", "timeSignature-8/8", "timeSignature-9/16", "timeSignature-9/4", "timeSignature-9/8", "timeSignature-C", "timeSignature-C/",
        "note-A#2_eighth", "note-A#2_half", "note-A#2_quarter", "note-A#2_quarter.", "note-A#2_sixteenth", "note-A#2_sixteenth.", "note-A#2_whole", "note-A#3_eighth", "note-A#3_eighth.", "note-A#3_half", "note-A#3_half.", "note-A#3_half_fermata", "note-A#3_quarter", "note-A#3_quarter.", "note-A#3_sixteenth", "note-A#3_sixteenth.", "note-A#3_sixty_fourth", "note-A#3_thirty_second", "note-A#3_whole", "note-A#4_eighth", "note-A#4_eighth.", "note-A#4_half", "note-A#4_half.", "note-A#4_half_fermata", "note-A#4_quarter", "note-A#4_quarter.", "note-A#4_quarter_fermata", "note-A#4_sixteenth", "note-A#4_sixteenth.", "note-A#4_thirty_second", "note-A#4_whole", "note-A#4_whole.", "note-A#5_eighth", "note-A#5_eighth.", "note-A#5_half", "note-A#5_half.", "note-A#5_quarter", "note-A#5_quarter.", "note-A#5_sixteenth", "note-A#5_sixteenth.", "note-A#5_thirty_second", "note-A1_sixteenth", "note-A2_double_whole", "note-A2_double_whole.", "note-A2_double_whole_fermata", "note-A2_eighth", "note-A2_eighth.", "note-A2_half", "note-A2_half.", "note-A2_half_fermata", "note-A2_quadruple_whole", "note-A2_quadruple_whole_fermata", "note-A2_quarter", "note-A2_quarter.", "note-A2_quarter_fermata", "note-A2_sixteenth", "note-A2_sixteenth.", "note-A2_sixty_fourth", "note-A2_thirty_second", "note-A2_whole", "note-A2_whole.", "note-A2_whole_fermata", "note-A3_double_whole", "note-A3_double_whole.", "note-A3_double_whole_fermata", "note-A3_eighth", "note-A3_eighth.", "note-A3_eighth..", "note-A3_eighth._fermata", "note-A3_eighth_fermata", "note-A3_half", "note-A3_half.", "note-A3_half._fermata", "note-A3_half_fermata", "note-A3_quadruple_whole", "note-A3_quarter", "note-A3_quarter.", "note-A3_quarter..", "note-A3_quarter_fermata", "note-A3_sixteenth", "note-A3_sixteenth.", "note-A3_sixty_fourth", "note-A3_thirty_second", "note-A3_whole", "note-A3_whole.", "note-A3_whole_fermata", "note-A4_double_whole", "note-A4_double_whole.", "note-A4_double_whole_fermata", "note-A4_eighth", "note-A4_eighth.", "note-A4_eighth..", "note-A4_eighth_fermata", "note-A4_half", "note-A4_half.", "note-A4_half..", "note-A4_half._fermata", "note-A4_half_fermata", "note-A4_quadruple_whole", "note-A4_quadruple_whole.", "note-A4_quarter", "note-A4_quarter.", "note-A4_quarter..", "note-A4_quarter._fermata", "note-A4_quarter_fermata", "note-A4_sixteenth", "note-A4_sixteenth.", "note-A4_sixty_fourth", "note-A4_thirty_second", "note-A4_thirty_second.", "note-A4_whole", "note-A4_whole.", "note-A4_whole._fermata", "note-A4_whole_fermata", "note-A5_double_whole", "note-A5_eighth", "note-A5_eighth.", "note-A5_eighth..", "note-A5_eighth_fermata", "note-A5_half", "note-A5_half.", "note-A5_half._fermata", "note-A5_half_fermata", "note-A5_quarter", "note-A5_quarter.", "note-A5_quarter..", "note-A5_quarter._fermata", "note-A5_quarter_fermata", "note-A5_sixteenth", "note-A5_sixteenth.", "note-A5_sixty_fourth", "note-A5_thirty_second", "note-A5_thirty_second.", "note-A5_whole", "note-A5_whole.", "note-A5_whole_fermata", "note-Ab2_eighth", "note-Ab2_eighth.", "note-Ab2_half", "note-Ab2_half.", "note-Ab2_half_fermata", "note-Ab2_quarter", "note-Ab2_quarter.", "note-Ab2_sixteenth", "note-Ab2_thirty_second", "note-Ab2_whole", "note-Ab3_eighth", "note-Ab3_eighth.", "note-Ab3_half", "note-Ab3_half.", "note-Ab3_quarter", "note-Ab3_quarter.", "note-Ab3_quarter..", "note-Ab3_sixteenth", "note-Ab3_sixteenth.", "note-Ab3_thirty_second", "note-Ab3_whole", "note-Ab4_eighth", "note-Ab4_eighth.", "note-Ab4_eighth..", "note-Ab4_half", "note-Ab4_half.", "note-Ab4_half._fermata", "note-Ab4_half_fermata", "note-Ab4_quarter", "note-Ab4_quarter.", "note-Ab4_quarter..", "note-Ab4_quarter_fermata", "note-Ab4_sixteenth", "note-Ab4_sixteenth.", "note-Ab4_sixty_fourth", "note-Ab4_thirty_second", "note-Ab4_thirty_second.", "note-Ab4_whole", "note-Ab4_whole.", "note-Ab4_whole_fermata", "note-Ab5_eighth", "note-Ab5_eighth.", "note-Ab5_eighth..", "note-Ab5_half", "note-Ab5_half.", "note-Ab5_half._fermata", "note-Ab5_quarter", "note-Ab5_quarter.", "note-Ab5_quarter_fermata", "note-Ab5_sixteenth", "note-Ab5_sixteenth.", "note-Ab5_sixty_fourth", "note-Ab5_thirty_second", "note-Ab5_whole", "note-B#2_eighth", "note-B#2_eighth.", "note-B#2_half", "note-B#2_quarter", "note-B#2_sixteenth", "note-B#2_whole", "note-B#3_double_whole", "note-B#3_double_whole.", "note-B#3_eighth", "note-B#3_eighth.", "note-B#3_half", "note-B#3_half.", "note-B#3_quarter", "note-B#3_quarter.", "note-B#3_sixteenth", "note-B#3_thirty_second", "note-B#3_whole", "note-B#4_double_whole", "note-B#4_double_whole_fermata", "note-B#4_eighth", "note-B#4_eighth.", "note-B#4_half", "note-B#4_half.", "note-B#4_quarter", "note-B#4_quarter.", "note-B#4_sixteenth", "note-B#4_sixteenth.", "note-B#4_thirty_second", "note-B#4_whole", "note-B#4_whole.", "note-B#5_eighth", "note-B#5_quarter", "note-B#5_sixteenth", "note-B1_quarter", "note-B2_double_whole", "note-B2_eighth", "note-B2_eighth.", "note-B2_half", "note-B2_half.", "note-B2_half_fermata", "note-B2_quarter", "note-B2_quarter.", "note-B2_sixteenth", "note-B2_sixteenth.", "note-B2_sixty_fourth", "note-B2_thirty_second", "note-B2_whole", "note-B2_whole.", "note-B3_double_whole", "note-B3_double_whole.", "note-B3_double_whole_fermata", "note-B3_eighth", "note-B3_eighth.", "note-B3_eighth_fermata", "note-B3_half", "note-B3_half.", "note-B3_half_fermata", "note-B3_quarter", "note-B3_quarter.", "note-B3_quarter..", "note-B3_quarter_fermata", "note-B3_sixteenth", "note-B3_sixteenth.", "note-B3_sixty_fourth", "note-B3_thirty_second", "note-B3_thirty_second.", "note-B3_whole", "note-B3_whole.", "note-B3_whole_fermata", "note-B4_double_whole", "note-B4_double_whole.", "note-B4_double_whole_fermata", "note-B4_eighth", "note-B4_eighth.", "note-B4_eighth..", "note-B4_eighth._fermata", "note-B4_eighth_fermata", "note-B4_half", "note-B4_half.", "note-B4_half._fermata", "note-B4_half_fermata", "note-B4_quadruple_whole", "note-B4_quarter", "note-B4_quarter.", "note-B4_quarter..", "note-B4_quarter._fermata", "note-B4_quarter_fermata", "note-B4_sixteenth", "note-B4_sixteenth.", "note-B4_sixteenth._fermata", "note-B4_sixteenth_fermata", "note-B4_sixty_fourth", "note-B4_thirty_second", "note-B4_thirty_second.", "note-B4_whole", "note-B4_whole.", "note-B4_whole._fermata", "note-B4_whole_fermata", "note-B5_double_whole", "note-B5_eighth", "note-B5_eighth.", "note-B5_eighth..", "note-B5_half", "note-B5_half.", "note-B5_half_fermata", "note-B5_quarter", "note-B5_quarter.", "note-B5_quarter..", "note-B5_sixteenth", "note-B5_sixteenth.", "note-B5_sixty_fourth", "note-B5_thirty_second", "note-B5_whole", "note-B5_whole.", "note-Bb1_half", "note-Bb2_double_whole", "note-Bb2_eighth", "note-Bb2_eighth.", "note-Bb2_half", "note-Bb2_half.", "note-Bb2_quarter", "note-Bb2_quarter.", "note-Bb2_quarter._fermata", "note-Bb2_quarter_fermata", "note-Bb2_sixteenth", "note-Bb2_sixteenth.", "note-Bb2_sixteenth_fermata", "note-Bb2_thirty_second", "note-Bb2_whole", "note-Bb2_whole.", "note-Bb3_double_whole", "note-Bb3_double_whole.", "note-Bb3_eighth", "note-Bb3_eighth.", "note-Bb3_eighth..", "note-Bb3_half", "note-Bb3_half.", "note-Bb3_half._fermata", "note-Bb3_half_fermata", "note-Bb3_quadruple_whole", "note-Bb3_quarter", "note-Bb3_quarter.", "note-Bb3_quarter..", "note-Bb3_quarter._fermata", "note-Bb3_quarter_fermata", "note-Bb3_sixteenth", "note-Bb3_sixteenth.", "note-Bb3_sixty_fourth", "note-Bb3_thirty_second", "note-Bb3_thirty_second.", "note-Bb3_whole", "note-Bb3_whole.", "note-Bb3_whole_fermata", "note-Bb4_double_whole", "note-Bb4_double_whole.", "note-Bb4_eighth", "note-Bb4_eighth.", "note-Bb4_eighth..", "note-Bb4_eighth_fermata", "note-Bb4_half", "note-Bb4_half.", "note-Bb4_half._fermata", "note-Bb4_half_fermata", "note-Bb4_quadruple_whole", "note-Bb4_quarter", "note-Bb4_quarter.", "note-Bb4_quarter..", "note-Bb4_quarter._fermata", "note-Bb4_quarter_fermata", "note-Bb4_sixteenth", "note-Bb4_sixteenth.", "note-Bb4_sixty_fourth", "note-Bb4_thirty_second", "note-Bb4_thirty_second.", "note-Bb4_whole", "note-Bb4_whole.", "note-Bb4_whole._fermata", "note-Bb4_whole_fermata", "note-Bb5_double_whole", "note-Bb5_eighth", "note-Bb5_eighth.", "note-Bb5_eighth..", "note-Bb5_half", "note-Bb5_half.", "note-Bb5_half_fermata", "note-Bb5_quarter", "note-Bb5_quarter.", "note-Bb5_quarter..", "note-Bb5_quarter_fermata", "note-Bb5_sixteenth", "note-Bb5_sixteenth.", "note-Bb5_sixty_fourth", "note-Bb5_thirty_second", "note-Bb5_thirty_second.", "note-Bb5_whole", "note-Bb5_whole.", "note-Bb5_whole_fermata", "note-C#2_eighth", "note-C#2_eighth.", "note-C#2_quarter", "note-C#2_quarter.", "note-C#2_sixteenth", "note-C#2_whole", "note-C#3_double_whole", "note-C#3_eighth", "note-C#3_eighth.", "note-C#3_half", "note-C#3_half.", "note-C#3_quarter", "note-C#3_quarter.", "note-C#3_sixteenth", "note-C#3_sixteenth.", "note-C#3_thirty_second", "note-C#3_whole", "note-C#4_eighth", "note-C#4_eighth.", "note-C#4_eighth..", "note-C#4_eighth_fermata", "note-C#4_half", "note-C#4_half.", "note-C#4_half_fermata", "note-C#4_quadruple_whole_fermata", "note-C#4_quarter", "note-C#4_quarter.", "note-C#4_quarter..", "note-C#4_quarter._fermata", "note-C#4_quarter_fermata", "note-C#4_sixteenth", "note-C#4_sixteenth.", "note-C#4_sixty_fourth", "note-C#4_thirty_second", "note-C#4_whole", "note-C#4_whole.", "note-C#4_whole_fermata", "note-C#5_double_whole", "note-C#5_eighth", "note-C#5_eighth.", "note-C#5_eighth..", "note-C#5_eighth._fermata", "note-C#5_eighth_fermata", "note-C#5_half", "note-C#5_half.", "note-C#5_half._fermata", "note-C#5_half_fermata", "note-C#5_quarter", "note-C#5_quarter.", "note-C#5_quarter..", "note-C#5_quarter._fermata", "note-C#5_quarter_fermata", "note-C#5_sixteenth", "note-C#5_sixteenth.", "note-C#5_sixteenth._fermata", "note-C#5_sixty_fourth", "note-C#5_sixty_fourth.", "note-C#5_thirty_second", "note-C#5_whole", "note-C#5_whole.", "note-C#5_whole_fermata", "note-C#6_eighth", "note-C#6_eighth.", "note-C#6_half", "note-C#6_half.", "note-C#6_half_fermata", "note-C#6_quarter", "note-C#6_quarter.", "note-C#6_quarter..", "note-C#6_sixteenth", "note-C#6_sixteenth.", "note-C#6_sixty_fourth", "note-C#6_thirty_second", "note-C#6_whole_fermata", "note-C2_double_whole.", "note-C2_eighth", "note-C2_eighth.", "note-C2_half", "note-C2_half.", "note-C2_half_fermata", "note-C2_quarter", "note-C2_quarter.", "note-C2_sixteenth", "note-C2_thirty_second", "note-C2_whole", "note-C3_double_whole", "note-C3_double_whole.", "note-C3_double_whole_fermata", "note-C3_eighth", "note-C3_eighth.", "note-C3_half", "note-C3_half.", "note-C3_half_fermata", "note-C3_quadruple_whole", "note-C3_quadruple_whole.", "note-C3_quarter", "note-C3_quarter.", "note-C3_quarter_fermata", "note-C3_sixteenth", "note-C3_sixteenth.", "note-C3_sixty_fourth", "note-C3_thirty_second", "note-C3_whole", "note-C3_whole.", "note-C3_whole_fermata", "note-C4_double_whole", "note-C4_double_whole.", "note-C4_double_whole_fermata", "note-C4_eighth", "note-C4_eighth.", "note-C4_eighth..", "note-C4_eighth_fermata", "note-C4_half", "note-C4_half.", "note-C4_half._fermata", "note-C4_half_fermata", "note-C4_hundred_twenty_eighth", "note-C4_quadruple_whole", "note-C4_quadruple_whole.", "note-C4_quarter", "note-C4_quarter.", "note-C4_quarter..", "note-C4_quarter._fermata", "note-C4_quarter_fermata", "note-C4_sixteenth", "note-C4_sixteenth.", "note-C4_sixty_fourth", "note-C4_thirty_second", "note-C4_thirty_second.", "note-C4_whole", "note-C4_whole.", "note-C4_whole_fermata", "note-C5_double_whole", "note-C5_double_whole.", "note-C5_double_whole._fermata", "note-C5_double_whole_fermata", "note-C5_eighth", "note-C5_eighth.", "note-C5_eighth..", "note-C5_eighth._fermata", "note-C5_eighth_fermata", "note-C5_half", "note-C5_half.", "note-C5_half._fermata", "note-C5_half_fermata", "note-C5_quadruple_whole", "note-C5_quadruple_whole.", "note-C5_quadruple_whole_fermata", "note-C5_quarter", "note-C5_quarter.", "note-C5_quarter..", "note-C5_quarter._fermata", "note-C5_quarter_fermata", "note-C5_sixteenth", "note-C5_sixteenth.", "note-C5_sixteenth_fermata", "note-C5_sixty_fourth", "note-C5_thirty_second", "note-C5_thirty_second.", "note-C5_whole", "note-C5_whole.", "note-C5_whole._fermata", "note-C5_whole_fermata", "note-C6_eighth", "note-C6_eighth.", "note-C6_eighth..", "note-C6_half", "note-C6_half.", "note-C6_half..", "note-C6_half._fermata", "note-C6_half_fermata", "note-C6_quarter", "note-C6_quarter.", "note-C6_quarter..", "note-C6_sixteenth", "note-C6_sixteenth.", "note-C6_sixty_fourth", "note-C6_thirty_second", "note-C6_thirty_second.", "note-C6_whole", "note-C6_whole_fermata", "note-Cb3_eighth", "note-Cb3_quarter", "note-Cb3_thirty_second", "note-Cb4_eighth", "note-Cb4_eighth.", "note-Cb4_quarter", "note-Cb4_quarter.", "note-Cb4_sixteenth", "note-Cb4_whole", "note-Cb5_eighth", "note-Cb5_eighth.", "note-Cb5_half", "note-Cb5_half.", "note-Cb5_quarter", "note-Cb5_quarter.", "note-Cb5_sixteenth", "note-Cb5_thirty_second", "note-Cb5_whole", "note-Cb6_eighth", "note-Cb6_half", "note-Cb6_quarter", "note-Cb6_sixteenth", "note-Cb6_thirty_second", "note-D#2_quarter", "note-D#2_sixteenth", "note-D#3_eighth", "note-D#3_eighth.", "note-D#3_half", "note-D#3_half_fermata", "note-D#3_quarter", "note-D#3_quarter.", "note-D#3_sixteenth", "note-D#3_sixteenth.", "note-D#3_thirty_second", "note-D#3_whole", "note-D#4_eighth", "note-D#4_eighth.", "note-D#4_half", "note-D#4_half.", "note-D#4_quarter", "note-D#4_quarter.", "note-D#4_sixteenth", "note-D#4_sixteenth.", "note-D#4_thirty_second", "note-D#4_whole", "note-D#5_double_whole", "note-D#5_eighth", "note-D#5_eighth.", "note-D#5_eighth..", "note-D#5_eighth_fermata", "note-D#5_half", "note-D#5_half.", "note-D#5_half_fermata", "note-D#5_quarter", "note-D#5_quarter.", "note-D#5_quarter..", "note-D#5_quarter_fermata", "note-D#5_sixteenth", "note-D#5_sixteenth.", "note-D#5_sixty_fourth", "note-D#5_thirty_second", "note-D#5_whole", "note-D#5_whole_fermata", "note-D#6_eighth", "note-D#6_eighth..", "note-D#6_half", "note-D#6_quarter", "note-D#6_sixteenth", "note-D#6_thirty_second", "note-D2_double_whole", "note-D2_eighth", "note-D2_eighth.", "note-D2_half", "note-D2_half.", "note-D2_half_fermata", "note-D2_quarter", "note-D2_quarter.", "note-D2_quarter._fermata", "note-D2_sixteenth", "note-D2_thirty_second", "note-D2_whole", "note-D3_double_whole", "note-D3_double_whole.", "note-D3_double_whole_fermata", "note-D3_eighth", "note-D3_eighth.", "note-D3_eighth_fermata", "note-D3_half", "note-D3_half.", "note-D3_half_fermata", "note-D3_quadruple_whole", "note-D3_quadruple_whole_fermata", "note-D3_quarter", "note-D3_quarter.", "note-D3_quarter..", "note-D3_quarter._fermata", "note-D3_quarter_fermata", "note-D3_sixteenth", "note-D3_sixteenth.", "note-D3_sixty_fourth", "note-D3_thirty_second", "note-D3_whole", "note-D3_whole.", "note-D3_whole_fermata", "note-D4_double_whole", "note-D4_double_whole.", "note-D4_double_whole_fermata", "note-D4_eighth", "note-D4_eighth.", "note-D4_eighth..", "note-D4_eighth._fermata", "note-D4_eighth_fermata", "note-D4_half", "note-D4_half.", "note-D4_half._fermata", "note-D4_half_fermata", "note-D4_hundred_twenty_eighth", "note-D4_quadruple_whole", "note-D4_quadruple_whole_fermata", "note-D4_quarter", "note-D4_quarter.", "note-D4_quarter..", "note-D4_quarter.._fermata", "note-D4_quarter._fermata", "note-D4_quarter_fermata", "note-D4_sixteenth", "note-D4_sixteenth.", "note-D4_sixteenth_fermata", "note-D4_sixty_fourth", "note-D4_thirty_second", "note-D4_thirty_second.", "note-D4_whole", "note-D4_whole.", "note-D4_whole_fermata", "note-D5_double_whole", "note-D5_double_whole.", "note-D5_double_whole_fermata", "note-D5_eighth", "note-D5_eighth.", "note-D5_eighth..", "note-D5_eighth._fermata", "note-D5_eighth_fermata", "note-D5_half", "note-D5_half.", "note-D5_half._fermata", "note-D5_half_fermata", "note-D5_quadruple_whole", "note-D5_quadruple_whole_fermata", "note-D5_quarter", "note-D5_quarter.", "note-D5_quarter..", "note-D5_quarter._fermata", "note-D5_quarter_fermata", "note-D5_sixteenth", "note-D5_sixteenth.", "note-D5_sixty_fourth", "note-D5_thirty_second", "note-D5_thirty_second.", "note-D5_whole", "note-D5_whole.", "note-D5_whole._fermata", "note-D5_whole_fermata", "note-D6_eighth", "note-D6_eighth.", "note-D6_eighth..", "note-D6_eighth_fermata", "note-D6_half", "note-D6_half.", "note-D6_half..", "note-D6_half_fermata", "note-D6_quarter", "note-D6_quarter.", "note-D6_quarter..", "note-D6_quarter._fermata", "note-D6_quarter_fermata", "note-D6_sixteenth", "note-D6_sixteenth.", "note-D6_sixty_fourth", "note-D6_thirty_second", "note-D6_whole", "note-D6_whole.", "note-D6_whole_fermata", "note-Db3_eighth", "note-Db3_eighth.", "note-Db3_half", "note-Db3_half.", "note-Db3_quarter", "note-Db3_quarter.", "note-Db3_sixteenth", "note-Db3_thirty_second", "note-Db4_double_whole", "note-Db4_eighth", "note-Db4_eighth.", "note-Db4_eighth..", "note-Db4_half", "note-Db4_half.", "note-Db4_quarter", "note-Db4_quarter.", "note-Db4_sixteenth", "note-Db4_sixteenth.", "note-Db4_thirty_second", "note-Db4_whole", "note-Db4_whole._fermata", "note-Db5_double_whole", "note-Db5_eighth", "note-Db5_eighth.", "note-Db5_eighth..", "note-Db5_half", "note-Db5_half.", "note-Db5_half_fermata", "note-Db5_quarter", "note-Db5_quarter.", "note-Db5_quarter..", "note-Db5_sixteenth", "note-Db5_sixteenth.", "note-Db5_sixty_fourth", "note-Db5_thirty_second", "note-Db5_whole", "note-Db5_whole.", "note-Db5_whole_fermata", "note-Db6_eighth", "note-Db6_eighth.", "note-Db6_half", "note-Db6_quarter", "note-Db6_quarter.", "note-Db6_sixteenth", "note-Db6_sixteenth.", "note-Db6_thirty_second", "note-E#2_sixteenth", "note-E#3_eighth", "note-E#3_eighth.", "note-E#3_half", "note-E#3_quarter", "note-E#3_sixteenth", "note-E#4_eighth", "note-E#4_eighth.", "note-E#4_eighth..", "note-E#4_half", "note-E#4_quarter", "note-E#4_quarter.", "note-E#4_sixteenth", "note-E#4_sixty_fourth", "note-E#4_thirty_second", "note-E#4_whole", "note-E#4_whole.", "note-E#5_eighth", "note-E#5_eighth.", "note-E#5_half", "note-E#5_half.", "note-E#5_half_fermata", "note-E#5_quarter", "note-E#5_quarter.", "note-E#5_sixteenth", "note-E#5_sixteenth.", "note-E#5_thirty_second", "note-E#5_whole", "note-E#6_sixteenth", "note-E2_eighth", "note-E2_eighth.", "note-E2_half", "note-E2_half.", "note-E2_quarter", "note-E2_quarter.", "note-E2_quarter_fermata", "note-E2_sixteenth", "note-E2_thirty_second", "note-E2_whole", "note-E2_whole_fermata", "note-E3_double_whole", "note-E3_double_whole.", "note-E3_double_whole_fermata", "note-E3_eighth", "note-E3_eighth.", "note-E3_half", "note-E3_half.", "note-E3_half._fermata", "note-E3_half_fermata", "note-E3_quadruple_whole", "note-E3_quarter", "note-E3_quarter.", "note-E3_quarter._fermata", "note-E3_quarter_fermata", "note-E3_sixteenth", "note-E3_sixteenth.", "note-E3_sixty_fourth", "note-E3_thirty_second", "note-E3_whole", "note-E3_whole.", "note-E3_whole_fermata", "note-E4_double_whole", "note-E4_double_whole.", "note-E4_double_whole._fermata", "note-E4_double_whole_fermata", "note-E4_eighth", "note-E4_eighth.", "note-E4_eighth..", "note-E4_eighth_fermata", "note-E4_half", "note-E4_half.", "note-E4_half._fermata", "note-E4_half_fermata", "note-E4_quadruple_whole", "note-E4_quadruple_whole.", "note-E4_quadruple_whole_fermata", "note-E4_quarter", "note-E4_quarter.", "note-E4_quarter..", "note-E4_quarter._fermata", "note-E4_quarter_fermata", "note-E4_sixteenth", "note-E4_sixteenth.", "note-E4_sixty_fourth", "note-E4_thirty_second", "note-E4_whole", "note-E4_whole.", "note-E4_whole_fermata", "note-E5_double_whole", "note-E5_double_whole.", "note-E5_double_whole_fermata", "note-E5_eighth", "note-E5_eighth.", "note-E5_eighth..", "note-E5_eighth_fermata", "note-E5_half", "note-E5_half.", "note-E5_half..", "note-E5_half._fermata", "note-E5_half_fermata", "note-E5_quadruple_whole_fermata", "note-E5_quarter", "note-E5_quarter.", "note-E5_quarter..", "note-E5_quarter._fermata", "note-E5_quarter_fermata", "note-E5_sixteenth", "note-E5_sixteenth.", "note-E5_sixteenth_fermata", "note-E5_sixty_fourth", "note-E5_thirty_second", "note-E5_thirty_second.", "note-E5_whole", "note-E5_whole.", "note-E5_whole._fermata", "note-E5_whole_fermata", "note-E6_eighth", "note-E6_eighth.", "note-E6_eighth..", "note-E6_half", "note-E6_half.", "note-E6_quarter", "note-E6_quarter.", "note-E6_sixteenth", "note-E6_sixteenth.", "note-E6_thirty_second", "note-E6_whole", "note-Eb2_eighth", "note-Eb2_half", "note-Eb2_quarter", "note-Eb2_quarter.", "note-Eb2_quarter._fermata", "note-Eb2_sixteenth", "note-Eb2_sixteenth.", "note-Eb2_thirty_second", "note-Eb2_whole", "note-Eb3_eighth", "note-Eb3_eighth.", "note-Eb3_half", "note-Eb3_half.", "note-Eb3_half._fermata", "note-Eb3_half_fermata", "note-Eb3_quarter", "note-Eb3_quarter.", "note-Eb3_quarter_fermata", "note-Eb3_sixteenth", "note-Eb3_sixteenth.", "note-Eb3_thirty_second", "note-Eb3_whole", "note-Eb3_whole.", "note-Eb4_double_whole", "note-Eb4_eighth", "note-Eb4_eighth.", "note-Eb4_eighth..", "note-Eb4_eighth._fermata", "note-Eb4_eighth_fermata", "note-Eb4_half", "note-Eb4_half.", "note-Eb4_half._fermata", "note-Eb4_half_fermata", "note-Eb4_hundred_twenty_eighth", "note-Eb4_quarter", "note-Eb4_quarter.", "note-Eb4_quarter..", "note-Eb4_quarter._fermata", "note-Eb4_quarter_fermata", "note-Eb4_sixteenth", "note-Eb4_sixteenth.", "note-Eb4_sixty_fourth", "note-Eb4_thirty_second", "note-Eb4_whole", "note-Eb4_whole.", "note-Eb4_whole_fermata", "note-Eb5_double_whole", "note-Eb5_eighth", "note-Eb5_eighth.", "note-Eb5_eighth..", "note-Eb5_eighth_fermata", "note-Eb5_half", "note-Eb5_half.", "note-Eb5_half..", "note-Eb5_half._fermata", "note-Eb5_half_fermata", "note-Eb5_hundred_twenty_eighth", "note-Eb5_quarter", "note-Eb5_quarter.", "note-Eb5_quarter..", "note-Eb5_quarter._fermata", "note-Eb5_quarter_fermata", "note-Eb5_sixteenth", "note-Eb5_sixteenth.", "note-Eb5_sixteenth_fermata", "note-Eb5_sixty_fourth", "note-Eb5_thirty_second", "note-Eb5_thirty_second.", "note-Eb5_whole", "note-Eb5_whole.", "note-Eb5_whole._fermata", "note-Eb5_whole_fermata", "note-Eb6_eighth", "note-Eb6_eighth.", "note-Eb6_eighth..", "note-Eb6_half", "note-Eb6_half.", "note-Eb6_quarter", "note-Eb6_quarter.", "note-Eb6_quarter..", "note-Eb6_sixteenth", "note-Eb6_sixteenth.", "note-Eb6_thirty_second", "note-F#2_eighth", "note-F#2_eighth.", "note-F#2_half", "note-F#2_half.", "note-F#2_quarter", "note-F#2_quarter.", "note-F#2_sixteenth", "note-F#2_whole", "note-F#3_double_whole", "note-F#3_eighth", "note-F#3_eighth.", "note-F#3_half", "note-F#3_half.", "note-F#3_half_fermata", "note-F#3_quarter", "note-F#3_quarter.", "note-F#3_quarter_fermata", "note-F#3_sixteenth", "note-F#3_sixteenth.", "note-F#3_sixty_fourth", "note-F#3_thirty_second", "note-F#3_whole", "note-F#3_whole.", "note-F#4_double_whole", "note-F#4_double_whole_fermata", "note-F#4_eighth", "note-F#4_eighth.", "note-F#4_eighth..", "note-F#4_eighth_fermata", "note-F#4_half", "note-F#4_half.", "note-F#4_half_fermata", "note-F#4_quadruple_whole_fermata", "note-F#4_quarter", "note-F#4_quarter.", "note-F#4_quarter..", "note-F#4_quarter._fermata", "note-F#4_quarter_fermata", "note-F#4_sixteenth", "note-F#4_sixteenth.", "note-F#4_sixty_fourth", "note-F#4_thirty_second", "note-F#4_thirty_second.", "note-F#4_whole", "note-F#4_whole.", "note-F#4_whole._fermata", "note-F#4_whole_fermata", "note-F#5_double_whole", "note-F#5_eighth", "note-F#5_eighth.", "note-F#5_eighth..", "note-F#5_eighth._fermata", "note-F#5_eighth_fermata", "note-F#5_half", "note-F#5_half.", "note-F#5_half._fermata", "note-F#5_half_fermata", "note-F#5_quarter", "note-F#5_quarter.", "note-F#5_quarter..", "note-F#5_quarter._fermata", "note-F#5_quarter_fermata", "note-F#5_sixteenth", "note-F#5_sixteenth.", "note-F#5_sixty_fourth", "note-F#5_thirty_second", "note-F#5_whole", "note-F#5_whole.", "note-F#5_whole_fermata", "note-F#6_eighth", "note-F#6_eighth.", "note-F#6_half", "note-F#6_half.", "note-F#6_quarter", "note-F#6_quarter.", "note-F#6_sixteenth", "note-F#6_thirty_second", "note-F#6_whole", "note-F2_double_whole", "note-F2_double_whole.", "note-F2_double_whole_fermata", "note-F2_eighth", "note-F2_eighth.", "note-F2_half", "note-F2_half.", "note-F2_half_fermata", "note-F2_quadruple_whole", "note-F2_quarter", "note-F2_quarter.", "note-F2_quarter..", "note-F2_sixteenth", "note-F2_sixteenth.", "note-F2_thirty_second", "note-F2_whole", "note-F2_whole.", "note-F3_double_whole", "note-F3_double_whole.", "note-F3_double_whole_fermata", "note-F3_eighth", "note-F3_eighth.", "note-F3_half", "note-F3_half.", "note-F3_half_fermata", "note-F3_quadruple_whole", "note-F3_quarter", "note-F3_quarter.", "note-F3_quarter..", "note-F3_sixteenth", "note-F3_sixteenth.", "note-F3_thirty_second", "note-F3_whole", "note-F3_whole.", "note-F3_whole_fermata", "note-F4_double_whole", "note-F4_double_whole.", "note-F4_double_whole_fermata", "note-F4_eighth", "note-F4_eighth.", "note-F4_eighth..", "note-F4_eighth_fermata", "note-F4_half", "note-F4_half.", "note-F4_half..", "note-F4_half._fermata", "note-F4_half_fermata", "note-F4_hundred_twenty_eighth", "note-F4_quadruple_whole", "note-F4_quadruple_whole.", "note-F4_quadruple_whole_fermata", "note-F4_quarter", "note-F4_quarter.", "note-F4_quarter..", "note-F4_quarter._fermata", "note-F4_quarter_fermata", "note-F4_sixteenth", "note-F4_sixteenth.", "note-F4_sixty_fourth", "note-F4_thirty_second", "note-F4_whole", "note-F4_whole.", "note-F4_whole_fermata", "note-F5_double_whole", "note-F5_eighth", "note-F5_eighth.", "note-F5_eighth..", "note-F5_half", "note-F5_half.", "note-F5_half._fermata", "note-F5_half_fermata", "note-F5_quarter", "note-F5_quarter.", "note-F5_quarter..", "note-F5_quarter._fermata", "note-F5_quarter_fermata", "note-F5_sixteenth", "note-F5_sixteenth.", "note-F5_sixty_fourth", "note-F5_thirty_second", "note-F5_thirty_second.", "note-F5_whole", "note-F5_whole.", "note-F5_whole_fermata", "note-F6_eighth", "note-F6_eighth.", "note-F6_half", "note-F6_half.", "note-F6_quarter", "note-F6_quarter.", "note-F6_sixteenth", "note-F6_sixteenth.", "note-F6_thirty_second", "note-Fb3_eighth", "note-Fb3_half", "note-Fb3_quarter", "note-Fb3_sixteenth", "note-Fb3_thirty_second", "note-Fb4_eighth", "note-Fb4_half", "note-Fb4_quarter", "note-Fb4_quarter.", "note-Fb4_sixteenth", "note-Fb4_sixteenth.", "note-Fb4_thirty_second", "note-Fb5_eighth", "note-Fb5_eighth.", "note-Fb5_half", "note-Fb5_sixteenth", "note-Fb5_thirty_second", "note-G#2_eighth", "note-G#2_eighth.", "note-G#2_half", "note-G#2_half.", "note-G#2_quarter", "note-G#2_quarter.", "note-G#2_sixteenth", "note-G#2_thirty_second", "note-G#2_whole", "note-G#3_eighth", "note-G#3_eighth.", "note-G#3_eighth..", "note-G#3_half", "note-G#3_half.", "note-G#3_half_fermata", "note-G#3_quarter", "note-G#3_quarter.", "note-G#3_sixteenth", "note-G#3_sixteenth.", "note-G#3_sixty_fourth", "note-G#3_thirty_second", "note-G#3_whole", "note-G#4_double_whole", "note-G#4_double_whole_fermata", "note-G#4_eighth", "note-G#4_eighth.", "note-G#4_eighth..", "note-G#4_eighth._fermata", "note-G#4_half", "note-G#4_half.", "note-G#4_half._fermata", "note-G#4_half_fermata", "note-G#4_quarter", "note-G#4_quarter.", "note-G#4_quarter_fermata", "note-G#4_sixteenth", "note-G#4_sixteenth.", "note-G#4_sixty_fourth", "note-G#4_thirty_second", "note-G#4_thirty_second.", "note-G#4_whole", "note-G#4_whole.", "note-G#4_whole_fermata", "note-G#5_eighth", "note-G#5_eighth.", "note-G#5_eighth_fermata", "note-G#5_half", "note-G#5_half.", "note-G#5_half_fermata", "note-G#5_quarter", "note-G#5_quarter.", "note-G#5_quarter..", "note-G#5_quarter_fermata", "note-G#5_sixteenth", "note-G#5_sixteenth.", "note-G#5_sixty_fourth", "note-G#5_thirty_second", "note-G#5_whole", "note-G#5_whole.", "note-G2_double_whole", "note-G2_double_whole.", "note-G2_double_whole_fermata", "note-G2_eighth", "note-G2_eighth.", "note-G2_half", "note-G2_half.", "note-G2_half_fermata", "note-G2_quadruple_whole", "note-G2_quarter", "note-G2_quarter.", "note-G2_quarter_fermata", "note-G2_sixteenth", "note-G2_sixteenth.", "note-G2_thirty_second", "note-G2_whole", "note-G2_whole.", "note-G2_whole_fermata", "note-G3_double_whole", "note-G3_double_whole.", "note-G3_eighth", "note-G3_eighth.", "note-G3_eighth..", "note-G3_eighth._fermata", "note-G3_eighth_fermata", "note-G3_half", "note-G3_half.", "note-G3_half._fermata", "note-G3_half_fermata", "note-G3_quadruple_whole", "note-G3_quarter", "note-G3_quarter.", "note-G3_quarter..", "note-G3_quarter._fermata", "note-G3_quarter_fermata", "note-G3_sixteenth", "note-G3_sixteenth.", "note-G3_sixty_fourth", "note-G3_thirty_second", "note-G3_whole", "note-G3_whole.", "note-G3_whole_fermata", "note-G4_double_whole", "note-G4_double_whole.", "note-G4_double_whole_fermata", "note-G4_eighth", "note-G4_eighth.", "note-G4_eighth..", "note-G4_eighth_fermata", "note-G4_half", "note-G4_half.", "note-G4_half._fermata", "note-G4_half_fermata", "note-G4_quadruple_whole", "note-G4_quadruple_whole.", "note-G4_quadruple_whole_fermata", "note-G4_quarter", "note-G4_quarter.", "note-G4_quarter..", "note-G4_quarter._fermata", "note-G4_quarter_fermata", "note-G4_sixteenth", "note-G4_sixteenth.", "note-G4_sixteenth..", "note-G4_sixteenth._fermata", "note-G4_sixty_fourth", "note-G4_thirty_second", "note-G4_thirty_second.", "note-G4_whole", "note-G4_whole.", "note-G4_whole._fermata", "note-G4_whole_fermata", "note-G5_double_whole", "note-G5_double_whole.", "note-G5_eighth", "note-G5_eighth.", "note-G5_eighth..", "note-G5_eighth_fermata", "note-G5_half", "note-G5_half.", "note-G5_half..", "note-G5_half._fermata", "note-G5_half_fermata", "note-G5_quadruple_whole.", "note-G5_quarter", "note-G5_quarter.", "note-G5_quarter..", "note-G5_quarter._fermata", "note-G5_quarter_fermata", "note-G5_sixteenth", "note-G5_sixteenth.", "note-G5_sixty_fourth", "note-G5_thirty_second", "note-G5_thirty_second.", "note-G5_whole", "note-G5_whole.", "note-G5_whole_fermata", "note-Gb2_quarter", "note-Gb2_sixteenth", "note-Gb3_eighth", "note-Gb3_eighth.", "note-Gb3_half", "note-Gb3_quarter", "note-Gb3_quarter.", "note-Gb3_quarter..", "note-Gb3_sixteenth", "note-Gb3_thirty_second", "note-Gb3_whole", "note-Gb4_eighth", "note-Gb4_eighth.", "note-Gb4_eighth..", "note-Gb4_half", "note-Gb4_half.", "note-Gb4_quarter", "note-Gb4_quarter.", "note-Gb4_sixteenth", "note-Gb4_sixteenth.", "note-Gb4_sixty_fourth", "note-Gb4_thirty_second", "note-Gb4_whole", "note-Gb5_eighth", "note-Gb5_eighth.", "note-Gb5_half", "note-Gb5_half.", "note-Gb5_quarter", "note-Gb5_quarter.", "note-Gb5_quarter..", "note-Gb5_sixteenth", "note-Gb5_sixteenth.", "note-Gb5_thirty_second", "note-Gb5_whole",
    ]

    print(len(semantic_data))
    convertor = Sym_conv(semantic_data)

    # general AGNOSTIC symbol type
    # convertor.replace_dict(
    #     {
    #         'barline-L1': '|',
    #         'accidental.flat-': 'b',
    #         'accidental.sharp-': '#',
    #         'accidental.natural-': '\\',
    #         'clef.C-': 'c',
    #         'clef.F-': 'f',
    #         'clef.G-': 'g',
    #         'digit.': '',
    #         'dot-': '.',
    #         'fermata.above-S6': '^',
    #         'gracenote.': 'G',
    #         'note.': 'N',
    #         'metersign.C-L3': '<',
    #         'metersign.C/-L3': '>',
    #         'multirest-L3': 'm',
    #         'slur.start-': 's',
    #         'slur.end-': 'e',
    #         'rest.': 'r',
    #         '-L': 'L',
    #         '-S': 'S'
    #     }
    # )

    # general SEMANTIC symbol type
    convertor.replace_dict(
        {
            'barline': '|',
            "clef-C1": "á",
            "clef-C2": "č",
            "clef-C3": "ď",
            "clef-C4": "é",
            "clef-C5": "ě",
            "clef-F3": "í",
            "clef-F4": "ň",
            "clef-F5": "ó",
            "clef-G1": "ř",
            "clef-G2": "š",
        }
    )
    # Notes and gracenotes
    convertor.replace_dict(
        {
            'gracenote-A': 'a',
            'gracenote-B': 'b',
            'gracenote-C': 'c',
            'gracenote-D': 'd',
            'gracenote-E': 'e',
            'gracenote-F': 'f',
            'gracenote-G': 'g',
            'note-A': 'A',
            'note-B': 'B',
            'note-C': 'C',
            'note-D': 'D',
            'note-E': 'E',
            'note-F': 'F',
            'note-G': 'G',
            'multirest-': '-'
        }
    )

    # # AGNOSTIC Symbol positions
    # pos_lines = {f'L{i}': f'/{i * 2}' for i in range(10)}
    # pos_neg_lines = {f'L-{i}': f'/-{i * 2}' for i in range(4)}
    # pos_spaces = {f'S{i}': f'/{(i * 2) - 1}' for i in range(10)}
    # pos_neg_spaces = {f'S-{i}': f'/-{(i * 2) + 1}' for i in range(1, 4)}

    # convertor.replace_dict(pos_lines)
    # convertor.replace_dict(pos_neg_lines)
    # convertor.replace_dict(pos_spaces)
    # convertor.replace_dict(pos_neg_spaces)

    # Semantic clefs:


    # symbol (notes, gracenotes, rest...) lengths
    convertor.replace_dict({
        # 'beamedBoth': 'B',
        # 'beamedLeft': 'L',
        # 'beamedRight': 'R',
        '_double_whole': 'Á',
        '_eighth': 'Č',
        '_half': 'Ď',
        '_quarter': 'É',
        '_quadruple_whole': 'Ě',
        '_thirty_second': 'Í',
        '_hundred_twenty': 'Ň',
        '_sixteenth': 'Ó',
        '_sixty_fourth': 'Ř',
        '_whole': 'Š',

        '-double_whole': 'Á',
        '-eighth': 'Č',
        '-half': 'Ď',
        '-quarter': 'É',
        '-quadruple_whole': 'Ě',
        '-thirty_second': 'Í',
        '-hundred_twenty': 'Ň',
        '-sixteenth': 'Ó',
        '-sixty_fourth': 'Ř',
        '-whole': 'Š',
        })

    convertor.replace_two_lists(
        ["keySignature-AM", "keySignature-AbM", "keySignature-BM", "keySignature-BbM", "keySignature-C#M", "keySignature-CM", "keySignature-DM", "keySignature-DbM", "keySignature-EM", "keySignature-EbM", "keySignature-F#M", "keySignature-FM", "keySignature-GM", "keySignature-GbM"],
        ['À', 'Ą', 'Ⱥ', 'Ā', 'Å', 'Â', 'Ǡ', 'à', 'â', 'ã', 'ā', 'ą', 'ȧ', 'ⱥ']
    )

    convertor.replace_dict(
        {
            'rest': ';',
            'tie': ':',
            '_fermata': '~',
        }
    )

    convertor.replace_two_lists(
        ["timeSignature-1/2", "timeSignature-1/4", "timeSignature-11/4", "timeSignature-12/16", "timeSignature-12/4", "timeSignature-12/8", "timeSignature-2/1", "timeSignature-2/2", "timeSignature-2/3", "timeSignature-2/4", "timeSignature-2/48", "timeSignature-2/8", "timeSignature-24/16", "timeSignature-3/1", "timeSignature-3/2", "timeSignature-3/4", "timeSignature-3/6", "timeSignature-3/8", "timeSignature-4/1", "timeSignature-4/2", "timeSignature-4/4", "timeSignature-4/8", "timeSignature-5/4", "timeSignature-5/8", "timeSignature-6/16", "timeSignature-6/2", "timeSignature-6/4", "timeSignature-6/8", "timeSignature-7/4", "timeSignature-8/12", "timeSignature-8/16", "timeSignature-8/2", "timeSignature-8/4", "timeSignature-8/8", "timeSignature-9/16", "timeSignature-9/4", "timeSignature-9/8", "timeSignature-C", "timeSignature-C/"],
        ['ꝛ', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж']
    )

    convertor.finalize()

    # %%


if __name__ == '__main__':
    main()


# %% Charsets:

all_chars = []
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

latin = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
         's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

symbols = ['!', '¡', '?', '¿', ',', '—', '.', '·', ':', ';', '\\', '_', '&', '#', '@', '(', ')', '[', ']', '{', '}', '+',
           '-', '*', '/', '±', '=', '≠', '<', '>', '≤', '≥', 'ϵ', '∞', '%', '‰', '£', '€', '$', '§', '©', '®', '℥', "'",
           '‘', '’', '`', '„', '“', '"', '»', '«', '›', '‹', '☞', '☜', '^', '~', '°', '˛', '†', '|', '⁂', '⊥', '¬', '¤']

latin_special = ['À', 'Ą', 'Ⱥ', 'Ā', 'Å', 'Â', 'Ǡ', 'à', 'â', 'ã', 'ā', 'ą', 'ȧ', 'ⱥ', 'å', 'ă', 'ạ', 'ǎ', 'ȃ', 'ả', 'Ç',
                 'Ć', 'Ċ', 'ç', 'ć', 'ċ', 'ĉ', 'đ', 'È', 'Ę', 'Ɇ', 'Ê', 'Ë', 'è', 'ê', 'ë', 'ē', 'ę', 'ɇ', 'ẽ', 'ĕ', 'ė',
                 'ƒ', 'ġ', 'ǵ',  'Į', 'İ', 'Ì', 'Ï', 'ì', 'î', 'ï', 'ī', 'ı', 'ĭ', 'ǐ', 'ĩ', 'ḱ', 'Ł', 'Ľ', 'ĺ', 'ľ', 'ł',
                 'ḿ', 'ṁ', 'Ñ', 'ñ', 'ń', 'ṅ', 'ǹ', 'Ô', 'Ō', 'Ŏ', 'Ò', 'ò', 'ô', 'õ', 'ŏ', 'ō', 'ȍ', 'ő', 'ȯ', 'ọ', 'ø',
                 'ᵱ', 'ꝓ', 'ꝑ', 'ṗ', 'ṕ', 'ꝙ', 'ꝗ', 'Ŕ', 'ṙ', 'ŕ', 'Ş', 'Ś', 'Ș', 'ś', 'ṡ', 'ş', 'ŝ', 'Ù', 'ù', 'û', 'ũ',
                 'ū', 'ű', 'ŭ', 'ữ', 'ǔ', 'ꝟ', 'Ẃ', 'ẃ', 'ẇ', 'ẁ', 'ẉ', 'ÿ', 'ŷ', 'ỹ', 'ẏ', 'ȳ', 'ỳ', 'Ż', 'Ź', 'ź', 'ż',
                 'Æ', 'æ', 'Œ', 'œ', 'ə', 'ŋ', 'ʃ', 'ʒ', 'Ɛ']

all_chars += numbers + latin + symbols

czech_special = ['Á', 'Č', 'Ď', 'É', 'Ě', 'Í', 'Ň', 'Ó', 'Ř', 'Š', 'Ť', 'Ú', 'Ů', 'Ý', 'Ž',
                 'á', 'č', 'ď', 'é', 'ě', 'í', 'ň', 'ó', 'ř', 'š', 'ť', 'ú', 'ů', 'ý', 'ž']

german_special = ['Ä', 'Ö', 'Ü', 'ẞ', 'ä', 'ö', 'ü', 'ß', 'ſ', 'ꝛ']

russian = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
           'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
           'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

russian_special = ['Є', 'Ѕ', 'Ꙃ', 'Ꙁ', 'І', 'Ї', 'Ꙋ', 'Ѡ', 'Ѣ', 'Ꙗ', 'Ѥ', 'Ѫ', 'Ѭ', 'Ѧ', 'Ѩ', 'Ѯ', 'Ѱ', 'Ѳ', 'Ѵ',
                   'Ҁ', 'є', 'ѕ', 'ꙃ', 'ꙁ', 'і', 'ї', 'ꙋ', 'ѡ', 'ѣ', 'ꙗ', 'ѥ', 'ѫ', 'ѭ', 'ѧ', 'ѩ', 'ѯ', 'ѱ', 'ѳ',
                   'ѵ', 'ҁ', 'ӥ', 'Ұ', 'ј', 'њ', 'љ', 'ӣ', 'ѝ', 'ѓ', 'џ', 'ћ', 'ђ', 'ә', 'Ӕ', 'ӕ']


greek = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Ϲ', 'Τ', 'Υ', 'Φ',
         'Χ', 'Ψ', 'Ω', 'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς',
         'ϲ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']

greek_special = ['ϳ', 'ϝ']

historic_german_umlauted_chars = ['Aͤ', 'Oͤ', 'aͤ', 'eͤ', 'iͤ', 'oͤ', 'uͤ']

historic_german_mapping = {'Aͤ': 'Ä', 'Oͤ': 'Ö', 'aͤ': 'ä', 'eͤ': 'ë', 'iͤ': 'ï', 'oͤ': 'ö', 'uͤ': 'ü', 'ſ': 's'}

parzival_characters = ['ẘ', '̾', '̃', 'ṽ', 'ǒ', '̊']

orthogonal_accents_canonical = ['ͤ', '́', '̸', '̃', '̛', '̊', '̑', '̆', '̂', '̈', '̦', '̇', '̋', '̄', '̏', '̉', '̧', '̨', '̀', '̌', '̣']
orthogonal_base_canonical =  ['�', ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                               'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                               'u', 'v', 'w', 'x', 'y', 'z', '!', '¡', '?', '¿', ',', '—', '.', '·', ':', ';',
                               '\\', '_', '&', '#', '@', '(', ')', '[', ']', '{', '}', '+', '-', '*', '/', '±',
                               '=', '<', '>', '≤', '≥', 'ϵ', '∞', '%', '‰', '£', '€', '$', '§', '©', '®', '℥',
                               "'", '‘', '’', '`', '„', '“', '"', '»', '«', '›', '‹', '☞', '☜', '^', '~', '°',
                               '˛', '†', '|', '⁂', '⊥', '¬', '¤', '0', '1', '2', '3', '4', '5', '6', '7', '8',
                               '9', 'ẞ', 'ß', 'ſ', 'ꝛ', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л',
                               'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы',
                               'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к', 'л', 'м',
                               'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
                               'э', 'ю', 'я', 'Є', 'Ѕ', 'Ꙃ', 'Ꙁ', 'І', 'Ꙋ', 'Ѡ', 'Ѣ', 'Ꙗ', 'Ѥ', 'Ѫ', 'Ѭ', 'Ѧ',
                               'Ѩ', 'Ѯ', 'Ѱ', 'Ѳ', 'Ѵ', 'Ҁ', 'є', 'ѕ', 'ꙃ', 'ꙁ', 'і', 'ꙋ', 'ѡ', 'ѣ', 'ꙗ', 'ѥ',
                               'ѫ', 'ѭ', 'ѧ', 'ѩ', 'ѯ', 'ѱ', 'ѳ', 'ѵ', 'ҁ', 'Ұ', 'ј', 'њ', 'љ', 'џ', 'ћ', 'ђ',
                               'ә', 'Ӕ', 'ӕ', 'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν',
                               'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Ϲ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω', 'α', 'β', 'γ', 'δ',
                               'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'ϲ',
                               'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'ϳ', 'ϝ', 'Ⱥ', 'ⱥ', 'đ', 'Ɇ', 'ɇ', 'ƒ', 'ı', 'Ł',
                               'ł', 'ø', 'ᵱ', 'ꝓ', 'ꝑ', 'ꝙ', 'ꝗ', 'ꝟ', 'Æ', 'æ', 'Œ', 'œ', 'ə', 'ŋ', 'ʃ', 'ʒ',
                               'Ɛ', '¶']

orthogonal_accents_compatible = ['ͤ', '́', '̑', '̸', '̆', '̏', '̉', '̂', '̇', '̧', '̈', '̨', '̀', '̌', '̋', '̃', '̛', '̊', '̣', '̄', '̦']
orthogonal_base_compatible = ['�', ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                               'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                               'u', 'v', 'w', 'x', 'y', 'z', '!', '¡', '?', '¿', ',', '—', '.', '·', ':', ';',
                               '\\', '_', '&', '#', '@', '(', ')', '[', ']', '{', '}', '+', '-', '*', '/', '±',
                               '=', '<', '>', '≤', '≥', '∞', '%', '‰', '£', '€', '$', '§', '©', '®', '℥', "'",
                               '‘', '’', '`', '„', '“', '"', '»', '«', '›', '‹', '☞', '☜', '^', '~', '°', '†',
                               '|', '⁂', '⊥', '¬', '¤', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ẞ',
                               'ß', 'ꝛ', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О',
                               'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю',
                               'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к', 'л', 'м', 'н', 'о', 'п',
                               'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
                               'Є', 'Ѕ', 'Ꙃ', 'Ꙁ', 'І', 'Ꙋ', 'Ѡ', 'Ѣ', 'Ꙗ', 'Ѥ', 'Ѫ', 'Ѭ', 'Ѧ', 'Ѩ', 'Ѯ', 'Ѱ',
                               'Ѳ', 'Ѵ', 'Ҁ', 'є', 'ѕ', 'ꙃ', 'ꙁ', 'і', 'ꙋ', 'ѡ', 'ѣ', 'ꙗ', 'ѥ', 'ѫ', 'ѭ', 'ѧ',
                               'ѩ', 'ѯ', 'ѱ', 'ѳ', 'ѵ', 'ҁ', 'Ұ', 'ј', 'њ', 'љ', 'џ', 'ћ', 'ђ', 'ә', 'Ӕ', 'ӕ',
                               'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π',
                               'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω', 'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ',
                               'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ', 'φ', 'χ', 'ψ',
                               'ω', 'ϳ', 'ϝ', 'Ⱥ', 'ⱥ', 'đ', 'Ɇ', 'ɇ', 'ƒ', 'ı', 'Ł', 'ł', 'ø', 'ᵱ', 'ꝓ', 'ꝑ',
                               'ꝙ', 'ꝗ', 'ꝟ', 'Æ', 'æ', 'Œ', 'œ', 'ə', 'ŋ', 'ʃ', 'ʒ', 'Ɛ', '¶']

orthogonal_canonical_with_padding = orthogonal_canonical + [chr(ord('􁀐') + i) for i in range(383-len(orthogonal_canonical))]
orthogonal_compatible_with_padding = orthogonal_compatible + [chr(ord('􁀐') + i) for i in range(383-len(orthogonal_compatible))]

arabic = ['ا', 'ل', 'ي', 'م', 'و', 'ن', 'ر', 'ت', 'ع', 'ب', 'ه', 'د', 'ة', 'ف', 'ق', 'س', 'ك', 'ح', 'أ', 'ج', 'ش', 'خ',
          'ص', 'ط', 'ض', 'ذ', 'ى', '،', 'ز', 'ث', 'إ', 'ئ', 'ء', 'غ', 'ظ', 'ً', 'ؤ', 'ـ', '؟', 'آ', '؛', 'ّ', 'ُ', 'َ', 'ِ',
          'ٍ', 'ْ', 'ٌ']

madcat = base + latin + symbols + numbers + arabic

dta_chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
             'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', ']', '_', 'a',
             'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
             'w', 'x', 'y', 'z', '|', '}', '~', '£', '§', '«', '¬', '°', '±', '¶', '·', '»', 'Ä', 'Å', 'Æ', 'Ç', 'È',
             'É', 'Ó', 'Ô', 'Ö', 'Ü', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î',
             'ï', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'ÿ', 'Ā', 'ā', 'ă', 'ą', 'ć', 'Č', 'č',
             'ď', 'đ', 'ē', 'ĕ', 'ė', 'ę', 'ě', 'ī', 'ĭ', 'ı', 'ľ', 'ń', 'ň', 'ō', 'ŏ', 'œ', 'ř', 'ś', 'Š', 'š', 'ũ',
             'ū', 'ŭ', 'Ů', 'ů', 'ű', 'ŷ', 'ź', 'ż', 'Ž', 'ž', 'ſ', 'Ɛ', 'ǎ', 'ǵ', 'ə', 'ʒ', 'ͤ', 'Α', 'Γ', 'Δ', 'Ε',
             'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω', 'α', 'β',
             'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'ς', 'σ', 'τ', 'υ', 'φ', 'χ',
             'ψ', 'ω', 'ϝ', 'ϲ', 'ϳ', 'ϵ', 'Б', 'Э', 'и', 'й', 'н', 'о', 'т', 'ш', 'ӕ', 'ᵱ', 'ḱ', 'ṁ', 'ṅ', 'ẽ', '—',
             '‘', '’', '“', '„', '†', '‰', '›', '⁂', '℥', '∞', '⊥', '☜', '☞', 'ꝑ', 'ꝓ', 'ꝗ', 'ꝙ', 'ꝛ', 'ꝟ']

symbols_mapping = {'\t': ' ', '…': '...', '‥': '..', '⸗': '=', '–': '—', '‒': '—',  '­': '', '₤': '£', '×': 'x',
                   '‧': '·', '·': '·', '⋅': '·', '•': '·', '∙': '·', '−': '-', '∆': 'Δ', '⁎': '*', '¦': '|', '│': '|',
                   '℔': 'lb', '℞': 'R', '〃': '//',
                   'ˮ': '"', '‟': '"', '”': '"', 'ʺ': '"', '″': '"', '´': '’', 'ʼ': '’', '′': "'",  '´': '‘',
                   '⁋': '¶', '❡': '¶', '⸿': '¶', '‑': '-'}

fractions_mapping = {'¼': '1/4', '½': '1/2', '¾': '3/4', '⅐': '1/7', '⅑': '1/9', '⅒': '1/10', '⅓': '1/3', '⅔': '2/3',
                     '⅕': '1/5', '⅖': '2/5', '⅗': '3/5', '⅘': '4/5', '⅙': '1/6', '⅚': '5/6', '⅛': '1/8', '⅜': '3/8',
                     '⅝': '5/8', '⅞': '7/8', '⅟': '1/', '↉': '0/3'}

ligatures_mapping = {'': 'ſt', '': 'ſi', '': 'll', '': 'ſſ', 'ﬁ': 'fi', 'ĳ': 'ij', '': 'ct', 'ﬀ': 'ff', '': 'ſl',
                     'ﬂ': 'fl', '': 'ſſi', 'ﬃ': 'ffi', 'ﬆ': 'śt', 'Ĳ': 'IJ', 'ﬄ': 'ffl'}

index_mapping = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
                 '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'}

greek_mapping = {'ϑ': 'θ', 'ϖ': 'π', 'ϕ': 'φ', 'ϰ': 'κ', 'ϐ': 'β', 'µ': 'μ',
                 'ά': 'α', 'ἀ': 'α', 'ἄ': 'α', 'ὰ': 'α', 'ᾳ': 'α', 'ᾶ': 'α', 'ᾷ': 'α', 'ἅ': 'α', 'ᾱ': 'α', 'ἁ': 'α',
                 'ἆ': 'α',
                 'Ἀ': 'Α', 'Ἄ': 'Α', 'Ἅ': 'Α',
                 'ἐ': 'ε', 'έ': 'ε', 'ἔ': 'ε', 'ἑ': 'ε', 'ὲ': 'ε', 'ἕ': 'ε', 'ἓ': 'ε',
                 'Ἐ': 'Ε', 'Ἔ': 'Ε', 'Ἓ': 'Ε', 'Ἒ': 'Ε',
                 'ὸ': 'ο', 'ὁ': 'ο', 'ὀ': 'ο', 'ὅ': 'ο', 'ὄ': 'ο', 'ὃ': 'ο', 'Ὁ': 'Ο', 'ὂ': 'ο', 'ό': 'ο',
                 'ύ': 'υ', 'ῦ': 'υ', 'ὑ': 'υ', 'ὐ': 'υ', 'ὺ': 'υ', 'ὕ': 'υ', 'ὗ': 'υ', 'ὖ': 'υ', 'ὔ': 'υ',
                 'ῶ': 'ω', 'ῳ': 'ω', 'ῷ': 'ω', 'ὦ': 'ω', 'ὼ': 'ω', 'ὡ': 'ω', 'ὤ': 'ω', 'ὠ': 'ω', 'ὧ': 'ω', 'ᾧ': 'ω',
                 'ῴ': 'ω', 'ώ': 'ω',
                 'ὴ': 'η', 'ῆ': 'η', 'ἡ': 'η', 'ἦ': 'η', 'ῇ': 'η', 'ἠ': 'η', 'ῃ': 'η', 'ἧ': 'η', 'ἥ': 'η', 'ἤ': 'η',
                 'ἢ': 'η', 'ή': 'η',
                 'ϱ': 'ρ', 'ῥ': 'ρ', 'ῤ': 'ρ',
                 'ὶ': 'ι', 'ἰ': 'ι', 'ῖ': 'ι', 'ἱ': 'ι', 'ἴ': 'ι', 'ἶ': 'ι', 'ί': 'ι', 'ἷ': 'ι', 'ἵ': 'ι', 'ῒ': 'ι',
                 'ί': 'ι',
                 'Ὠ': 'Ω'}

roman_mapping = {'Ⅰ': 'I', 'Ⅴ': 'V', 'Ⅹ': 'X', 'Ⅼ': 'L', 'Ⅽ': 'C', 'Ⅾ': 'D', 'Ⅿ': 'M'}

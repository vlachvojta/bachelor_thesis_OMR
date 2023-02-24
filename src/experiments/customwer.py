"""Module with one class CustomWer."""

import jiwer


class CustomWer:
    """Class for adding continues lines to count WER from many lines."""

    dele = 0
    hits = 0
    ins = 0
    sub = 0

    def __init__(self):
        self.dele = 0
        self.hits = 0
        self.ins = 0
        self.sub = 0

    def add_lines(self, gt, pred) -> bool:
        """Add single or multiple lines to count WER from."""
        measures = jiwer.compute_measures(gt, pred)

        if ('deletions' in measures and
            'hits' in measures and
            'insertions' in measures and
                'substitutions' in measures):

            self.dele += measures['deletions']
            self.hits += measures['hits']
            self.ins += measures['insertions']
            self.sub += measures['substitutions']
            return True
        else:
            print('ERROR: unsuccessfull wer measurement')
            return False

    def __call__(self) -> float:
        """Return final WER for all lines in percents."""
        try:
            return (float(self.sub + self.dele + self.ins) /
                    float(self.hits + self.sub + self.dele) * 100)
        except ZeroDivisionError as error:
            print(f'ERROR: ZeroDivisionError: unsuccessfull final wer '
                  f'calculations {str(error)}')
            return 0.0

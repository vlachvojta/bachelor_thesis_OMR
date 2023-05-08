"""Module with one class CustomWer.

Author: Vojtěch Vlach
Contact: xvlach22@vutbr.cz
"""

import jiwer
import Levenshtein


class CustomWer:
    """Class for adding continues lines to count WER from many lines."""

    dele = 0
    hits = 0
    ins = 0
    sub = 0

    cer_err = 0
    cer_total = 0

    seq_err = 0
    seq_total = 0

    def __init__(self):
        self.dele = 0
        self.hits = 0
        self.ins = 0
        self.sub = 0
        self.cer_err = 0
        self.cer_total = 0

    def add_lines(self, truth, pred) -> bool:
        """Add single or multiple lines to count WER and CER from."""
        measures = jiwer.compute_measures(truth, pred)
        cer_success = self.add_cer(truth, pred)

        if ('deletions' in measures and
            'hits' in measures and
            'insertions' in measures and
                'substitutions' in measures):

            self.dele += measures['deletions']
            self.hits += measures['hits']
            self.ins += measures['insertions']
            self.sub += measures['substitutions']
            return True & cer_success
        else:
            print('ERROR: unsuccessfull wer measurement')
            return False

    def add_cer(self, ground_truth, predictions) -> bool:
        """Add single or multiple lines to count CER from."""

        if isinstance(ground_truth, str) and isinstance(predictions, str):
            err = Levenshtein.distance(ground_truth, predictions)
            self.cer_err += err
            self.cer_total += len(ground_truth)

            self.seq_total += 1
            if not ground_truth == predictions:
                self.seq_err += 1

            return True

        # otherwise, assume it's a list of strings
        if len(ground_truth) != len(predictions):
            raise ValueError(
                f"Number of ground truth inputs ({len(ground_truth)}) "
                f"and hypothesis inputs ({len(predictions)}) must match.")

        for truth, pred in zip(ground_truth, predictions):
            err = Levenshtein.distance(truth, pred)
            self.cer_err += err
            self.cer_total += len(truth)

            self.seq_total += 1
            if not truth == pred:
                self.seq_err += 1
        return True

    def __call__(self, get: str='wer') -> float:
        """Return final rates for all lines in percents.
        
        Args:
            get (str): 'wer' or 'cer'
        """
        try:
            if get == 'wer':
                true_wer = 100 * (float(self.sub + self.dele + self.ins) /
                            float(self.hits + self.sub + self.dele))
                return round(true_wer, 4)
            elif get == 'cer':
                true_cer = 100.0 * self.cer_err / self.cer_total
                return round(true_cer, 4)
            elif get == 'seqer':
                true_seqer = 100.0 * self.seq_err / self.seq_total
                return round(true_seqer, 4)
        except ZeroDivisionError as error:
            print(f'ERROR: ZeroDivisionError: unsuccessfull final wer '
                  f'calculations {str(error)}')
            return 0.0

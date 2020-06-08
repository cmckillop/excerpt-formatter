import re
from datetime import datetime

from models import FormattedInput

_offset_pattern = re.compile(r'([\d][\d]?:[\d][\d]?:[\d][\d]\t?\n?)')
_speaker_pattern = re.compile(
    r'\s+\s(?:[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?(?:\s[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?\s?(?:[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+,?)?:\s\s')
_new_paragraph_pattern = re.compile(r' {3}(X{13})?')
_line_number_pattern = re.compile(r'(?:\d+/\d+\s+)(?=[\d][\d]?:[\d][\d]?:[\d][\d]\t?\n?)')
_part_number_pattern = re.compile(r'(?:[P|p]art [\d][\d]?[\d]?)')
_time_format = '%H:%M:%S'


class TextFormatter:

    def __init__(self):
        self.start_date_time = datetime.now()

    def _parse_offset(self, time_str):
        time_str = time_str.strip()
        date_time = datetime.strptime(time_str, _time_format)
        date_time = date_time.replace(
            year=self.start_date_time.year,
            month=self.start_date_time.month,
            day=self.start_date_time.day
        )
        time_delta = date_time - self.start_date_time
        return str(time_delta)

    @staticmethod
    def _parse_speaker(matched_speaker):
        speaker = matched_speaker[0].strip().replace(':', '')
        if speaker.isupper() or speaker.islower():
            speaker = speaker.title()
        if ' Mp' in speaker:
            speaker = speaker.replace(' Mp', ' MP')
        return speaker

    def get_lines(self, text, preserve_paragraphs=False, no_offset=False):
        lines = text.splitlines()

        i = 0
        formatted_text = ''
        speaker: str
        offset = '0:00:00'
        word_count = 0
        excerpt_number = 0

        while i <= len(lines) - 1:
            is_new_paragraph = False
            line = re.sub(_line_number_pattern, '', lines[i])

            if re.match(_part_number_pattern, line):
                excerpt_number = int(re.findall(_part_number_pattern, line)[0].split()[1])
                line = re.sub(_part_number_pattern, '', line)

            if re.match(_new_paragraph_pattern, line):
                is_new_paragraph = True

            if re.match(_offset_pattern, line):
                offset = self._parse_offset(line)
            elif re.match(_speaker_pattern, line):
                speaker = self._parse_speaker(re.findall(_speaker_pattern, line))
                if no_offset:
                    formatted_text += f'\n\n{speaker}\n{re.split(_speaker_pattern, line)[1].strip()}'
                else:
                    formatted_text += f'\n\n{speaker}\n[{offset}] {re.split(_speaker_pattern, line)[1].strip()}'
            else:
                if preserve_paragraphs:
                    if is_new_paragraph:
                        formatted_text += f'\n{line.strip()}'
                    else:
                        formatted_text += f' {line.strip()}'
                else:
                    formatted_text += f' {line.strip()}'
                word_count += len(line.strip().split())
            i += 1

        return FormattedInput(
            excerpt_number,
            formatted_text.strip(),
            word_count
        )

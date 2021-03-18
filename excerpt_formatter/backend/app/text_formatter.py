import re
from datetime import time, datetime, timedelta

from models import FormattedInput

_speaker_pattern = re.compile(
    r"\[((?:[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?(?:\s[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?"
    r"(?:-[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?"
    r"(?:-[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?\s?(?:[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?"
    r"(?:-[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?(?:-[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?"
    r"(?:-[A-Za-zÀ-ÖØ-öø-ÿ'-]+,?)?(?:\s\d+)?)]:"
)
_audience_speaker_pattern = re.compile(r"(Audience Member)", re.IGNORECASE)
_speaker_prefix = "AudienceMember"

_part_number_pattern = re.compile(r"([P|p]art [\d][\d]?[\d]?)")
_time_format = "%H:%M:%S"

_line_number_pattern = re.compile(r"\d\d\d / \d\d\d?")
_offset_pattern = re.compile(r" ?\t?([\d][\d]?:[\d][\d]?:[\d][\d])")
_new_paragraph_pattern = re.compile(r"\d\d\d / \d\d\d?	 {15}")

_done_tag_pattern = re.compile(r"\[DONE]")


class TextFormatter:
    def __init__(self):
        self.programme_id = ""
        self.feed_delay = time(0, 0, 0)
        self.audience_member_idx = 0

    def _parse_offset(self, time_str):
        offset_time = datetime.strptime(time_str.strip(), _time_format).time()
        offset_time_delta = timedelta(
            hours=offset_time.hour,
            minutes=offset_time.minute,
            seconds=offset_time.second,
        )
        feed_delay_time_delta = timedelta(
            hours=self.feed_delay.hour,
            minutes=self.feed_delay.minute,
            seconds=self.feed_delay.second,
        )
        time_delta = offset_time_delta - feed_delay_time_delta
        return str(time_delta)

    def generate_audience_member_id(self):
        audience_member_id = (
            f"{_speaker_prefix} {self.programme_id}"
            f"{str(self.audience_member_idx).zfill(2)}"
        )
        self.audience_member_idx += 1
        return audience_member_id

    def _parse_speaker(self, matched_speaker):
        speaker = matched_speaker.strip()
        if re.search(_audience_speaker_pattern, matched_speaker):
            speaker = self.generate_audience_member_id()
        if speaker.isupper() or speaker.islower():
            speaker = speaker.title()
        if " Mp" in speaker:
            speaker = speaker.replace(" Mp", " MP")
        return speaker

    def get_lines(self, text, preserve_paragraphs=False, no_offset=False):
        lines = text.splitlines()

        i = 0
        formatted_text = ""
        offset = "0:00:00"
        word_count = 0
        excerpt_number = 0
        is_new_paragraph = False

        while i <= len(lines) - 1:
            line: str = lines[i]

            if re.match(_new_paragraph_pattern, line):
                is_new_paragraph = True

            line = re.sub(_line_number_pattern, "", line).strip()
            line = re.sub(_done_tag_pattern, "", line).strip()

            # To-Do Include the option to search for part numbers!!
            if re.match(_part_number_pattern, line):
                excerpt_number = int(
                    re.findall(_part_number_pattern, line)[0].split()[1]
                )
                i += 1
                continue

            # If the line starts with an Offset, ignore and continue
            if re.match(_offset_pattern, line):
                i += 1
                continue

            if re.search(_offset_pattern, line):
                # Send capture group (offset without the whitespace)
                # into the offset parsing function
                offset = self._parse_offset(
                    re.search(_offset_pattern, line).group(1)
                )
                line = re.sub(_offset_pattern, "", line).strip()

            if re.search(_speaker_pattern, line):
                # Send capture group (speaker without redundant characters)
                # into the speaker parsing function
                speaker = self._parse_speaker(
                    re.search(_speaker_pattern, line).group(1)
                )
                line = re.sub(_speaker_pattern, "", line).strip()

                if no_offset:
                    formatted_text += f"\n\n{speaker}\n{line.strip()}"
                else:
                    formatted_text += (
                        f"\n\n{speaker}\n[{offset}] {line.strip()}"
                    )
            else:
                line = re.sub(_line_number_pattern, "", line)
                if preserve_paragraphs:
                    if is_new_paragraph:
                        formatted_text += f"\n\t{line.strip()}"
                        is_new_paragraph = False
                    else:
                        formatted_text += f" {line.strip()}"
                else:
                    formatted_text += f" {line.strip()}"
                word_count += len(line.strip().split())
            i += 1

        formatted_text = formatted_text.replace("  ", " ")
        return FormattedInput(
            excerpt_number,
            self.audience_member_idx,
            formatted_text.strip(),
            word_count,
        )

import logging
from typing import List, Optional, Union

from wcmatch.pathlib import Path

from demisto_sdk.commands.common.constants import FileType
from demisto_sdk.commands.common.content.objects.abstract_objects import \
    TextObject
from demisto_sdk.commands.common.tools import MARKETPLACE_TAG_PARSER


class Readme(TextObject):
    def __init__(self, path: Union[Path, str]):
        self._path = path
        self.contributors = None
        super().__init__(path)

    def type(self):
        return FileType.README

    def mention_contributors_in_readme(self):
        """Mention contributors in pack readme"""
        try:
            if self.contributors:
                with open(self.contributors.path, 'r') as contributors_file:
                    contributor_data = contributors_file.read()
                with open(self._path, 'a+') as readme_file:
                    readme_file.write(contributor_data)
        except Exception as e:
            print(e)

    def handle_marketplace_tags(self):
        """Remove marketplace tags depending on marketplace version"""
        try:
            with open(self._path, 'r+') as f:
                text = f.read()
                parsed_text = MARKETPLACE_TAG_PARSER.parse_text(text)
                if len(text) != len(parsed_text):
                    f.seek(0)
                    f.write(parsed_text)
                    f.truncate()
        except Exception as e:
            logging.error(e)

    def dump(self, dest_dir: Optional[Union[Path, str]] = None) -> List[Path]:
        self.mention_contributors_in_readme()
        self.handle_marketplace_tags()
        return super().dump(dest_dir)

from dataclasses import dataclass
import re
from typing import Dict

@dataclass
class DocstringSection:
    """Represents a section of a docstring with its content."""
    name: str
    content: str


class DocstringParser:
    """Parser for Python docstrings that extracts structured information."""
    
    SECTION_MARKERS = [
        "Arguments:", "Args:", "Parameters:",
        "Returns:", "Return:", "Raises:",
        "Example:", "Examples:", "Note:",
        "---", "----"
    ]

    @staticmethod
    def clean_line(line: str) -> str:
        """Clean a single line of docstring formatting."""
        line = line.strip()
        line = re.sub(r'^\s*[\*\-]\s*', '', line)
        return line

    @classmethod
    def parse(cls, doc: str) -> Dict[str, DocstringSection]:
        """Parse a docstring into structured sections."""
        if not doc:
            return {}

        lines = [cls.clean_line(line) for line in doc.split('\n')]
        sections = {}
        current_section = None
        current_content = []
        description_content = []

        for line in lines:
            if any(line.startswith(marker) for marker in cls.SECTION_MARKERS):
                # If we were collecting description content, save it
                if not current_section and description_content:
                    sections['Description'] = DocstringSection(
                        'Description',
                        ' '.join(description_content).strip()
                    )
                    description_content = []
                
                # If we were in a section, save it
                if current_section:
                    sections[current_section] = DocstringSection(
                        current_section,
                        '\n'.join(current_content).strip()
                    )
                
                current_section = line.rstrip(':')
                current_content = []
            elif not current_section:
                if line:
                    description_content.append(line)
            else:
                current_content.append(line)

        # Add the last section
        if current_section:
            sections[current_section] = DocstringSection(
                current_section,
                '\n'.join(current_content).strip()
            )
        # Add description if we collected any and haven't added it yet
        elif description_content:
            sections['Description'] = DocstringSection(
                'Description',
                ' '.join(description_content).strip()
            )

        return sections

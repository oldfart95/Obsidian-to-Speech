# Obsidian to Speech Converter

A Python-based tool that converts Markdown files from Obsidian to clean, readable text files optimized for text-to-speech applications.

## Features

- Converts Markdown files while preserving readability and flow
- Maintains chapter numbers and section headers
- Removes Obsidian-specific syntax and formatting
- Handles both single files and entire directories
- Preserves proper spacing and paragraph structure
- Cleans up common formatting issues

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/obsidian-to-speech.git
cd obsidian-to-speech
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The tool provides two main commands:

### Convert a Single File

```bash
python obsidian_to_speech.py convert-file <input_file> <output_file>
```

Example:
```bash
python obsidian_to_speech.py convert-file "My Document.md" "output.txt"
```

### Convert an Entire Directory

```bash
python obsidian_to_speech.py convert-directory <input_directory> <output_directory>
```

Example:
```bash
python obsidian_to_speech.py convert-directory "My Obsidian Vault/Notes" "converted_text"
```

## Features in Detail

1. **Markdown Cleanup**
   - Removes headers (#, ##, etc.)
   - Removes bold and italic formatting
   - Removes links and image references
   - Removes Obsidian-specific syntax

2. **Text Formatting**
   - Preserves chapter numbers (e.g., "Chapter 1: Introduction")
   - Maintains proper section headers
   - Ensures consistent paragraph spacing
   - Handles lists and bullet points
   - Fixes common spacing issues

3. **Structure Preservation**
   - Maintains document hierarchy
   - Preserves important formatting for readability
   - Keeps logical flow of content

## Requirements

- Python 3.6 or higher
- Click (for CLI interface)
- BeautifulSoup4 (for HTML parsing)
- Markdown (for initial conversion)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Obsidian team for their excellent note-taking application
- Thanks to all contributors who helped improve this tool

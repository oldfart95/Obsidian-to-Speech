#!/usr/bin/env python3

import re
import os
import click
from markdown import markdown
from bs4 import BeautifulSoup
from pathlib import Path

def clean_markdown_text(text):
    # Initial cleanup of markdown and Obsidian syntax
    text = re.sub(r'#\s+', '', text)            # Remove heading markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Remove italics
    text = re.sub(r'`([^`]+)`', r'\1', text)    # Remove code blocks
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Remove links
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)  # Remove wiki links
    text = re.sub(r'\!\[\[([^\]]+)\]\]', '', text)   # Remove image links
    text = re.sub(r'\^[a-zA-Z0-9-]+', '', text)      # Remove block references
    text = re.sub(r'#([a-zA-Z0-9-]+)', '', text)     # Remove tags
    
    # Remove section numbers and other artifacts
    text = re.sub(r'^\s*--+\s*$', '', text, flags=re.MULTILINE)  # Remove horizontal rules
    text = re.sub(r'^\s*\d+\.\d+\s*$', '', text, flags=re.MULTILINE)  # Remove standalone section numbers
    text = re.sub(r'^\s*\d+\.\s*$', '', text, flags=re.MULTILINE)  # Remove standalone numbers
    text = re.sub(r'^\s*\.\d+\s*$', '', text, flags=re.MULTILINE)  # Remove standalone decimals
    text = re.sub(r'^\s*-\s*', '', text, flags=re.MULTILINE)  # Remove bullet points at start of lines
    text = re.sub(r'^\s*#\.\d+\.\d+\s+', '', text, flags=re.MULTILINE)  # Remove section numbers like "#.4.1"
    text = re.sub(r'^\s*#\.\d+\s+', '', text, flags=re.MULTILINE)  # Remove section numbers like "#.4"
    
    # Clean up chapter numbers and titles
    text = re.sub(r'^\s*Chapter\s+(\d+)\s*[:.]\s*([^\n]+)', r'Chapter \1: \2', text, flags=re.MULTILINE)
    
    # Split text into lines and process each one
    lines = text.split('\n')
    processed_lines = []
    current_paragraph = []
    
    for line in lines:
        # Clean up the line
        line = line.strip()
        if not line:
            if current_paragraph:
                processed_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            continue
            
        # Fix word spacing and line breaks
        line = re.sub(r'(?<=[a-zA-Z])(?=[A-Z][a-z])', ' ', line)  # Add space between camelCase words
        line = re.sub(r'([a-zA-Z])to([A-Z])', r'\1 to \2', line)  # Fix "to" getting stuck between words
        line = re.sub(r'([a-zA-Z])([A-Z])', r'\1 \2', line)  # Add space between words
        line = re.sub(r'([A-Z])\s+([A-Z])\s+([A-Z])', r'\1\2\3', line)  # Fix split acronyms like W S O P
        line = re.sub(r'([A-Z])\s+([A-Z])', r'\1\2', line)  # Fix split acronyms like W S
        
        # Clean up any remaining section numbers or bullet points
        line = re.sub(r'^\s*\d+\.\d+\s+', '', line)  # Remove section numbers like "1.1"
        line = re.sub(r'^\s*\d+\.\s+', '', line)  # Remove standalone numbers
        line = re.sub(r'^\s*\.\d+\s+', '', line)  # Remove standalone decimals
        line = re.sub(r'^\s*-\s+', '', line)  # Remove bullet points
        
        # Skip if line is empty after cleanup
        if not line:
            continue
        
        # Handle chapter titles specially
        chapter_match = re.match(r'^Chapter\s+(\d+):\s*(.+)$', line)
        if chapter_match:
            if current_paragraph:
                processed_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            if processed_lines:
                processed_lines.append('')
            processed_lines.append(f"Chapter {chapter_match.group(1)}: {chapter_match.group(2)}")
            processed_lines.append('')
            continue
        
        # Check if this line is a section header
        if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\s*$', line):
            if current_paragraph:
                processed_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            if processed_lines and processed_lines[-1]:
                processed_lines.append('')
            processed_lines.append(line)
            processed_lines.append('')
            continue
        
        # Handle key points sections
        if line == 'Key Milestones:':
            if current_paragraph:
                processed_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            if processed_lines and processed_lines[-1]:
                processed_lines.append('')
            processed_lines.append(line)
            processed_lines.append('')
            continue
        
        # Add to current paragraph
        current_paragraph.append(line)
    
    # Add any remaining paragraph
    if current_paragraph:
        processed_lines.append(' '.join(current_paragraph))

    # Join paragraphs with proper spacing
    text = '\n\n'.join(line for line in processed_lines if line is not None and line.strip())
    
    # Clean up whitespace and formatting
    text = re.sub(r'\n{3,}', '\n\n', text)  # Replace 3+ newlines with 2
    text = re.sub(r' +', ' ', text)  # Remove multiple spaces
    text = text.strip()  # Remove leading/trailing whitespace
    
    return text

@click.group()
def cli():
    """Convert Obsidian Markdown files to clean text for speech synthesis."""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
def convert(input_file, output_file):
    """Convert a single Markdown file to clean text."""
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read and convert the file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean the text
    clean_text = clean_markdown_text(content)
    
    # Write the cleaned text
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_text)
    
    click.echo(f"Converted {input_path} to {output_path}")

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
def convert_directory(input_dir, output_dir):
    """Convert all Markdown files in a directory to clean text."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process all markdown files
    for markdown_file in input_path.glob('**/*.md'):
        # Create relative path for output file
        rel_path = markdown_file.relative_to(input_path)
        output_file = output_path / rel_path.with_suffix('.txt')
        
        # Create output subdirectories if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Read and convert the file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean the text
        clean_text = clean_markdown_text(content)
        
        # Write the cleaned text
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        
        click.echo(f"Converted {markdown_file} to {output_file}")

if __name__ == '__main__':
    cli()

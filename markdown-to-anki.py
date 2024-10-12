import genanki
import os
import markdown

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

markdown_file_path = '/Users/vmitchell/Documents/Obsidian/Vault/Uni/Zusammenfassungen/Pharmakologie Zusammenfassung Kategorien.md'
text = read_markdown_file(markdown_file_path)

def markdown_to_html(text):
    if isinstance(text, list):
        text = '\n'.join(text)
    html = markdown.markdown(text, extensions=['extra', 'sane_lists'])
    return html

def parse_text_to_anki(text):
    lines = text.split('\n')
    deck = genanki.Deck(
        2059400110,
        'Pharma Medikamente'
    )
    model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    question = None
    answer = []
    has_bullet_points = False

    for line in lines:
        if line.startswith('## '):
            if question and has_bullet_points:
                note = genanki.Note(
                    model=model,
                    fields=[question, markdown_to_html(answer)]
                )
                deck.add_note(note)
            question = line[3:]
            answer = []
            has_bullet_points = False
        elif line.strip().startswith('- '):
            answer.append(line)
            has_bullet_points = True
        elif line.startswith('### '):
            if question and has_bullet_points:
                note = genanki.Note(
                    model=model,
                    fields=[question, markdown_to_html(answer)]
                )
                deck.add_note(note)
            question = line[4:]
            answer = []
            has_bullet_points = False
        elif line.startswith('#### '):
            if question and has_bullet_points:
                note = genanki.Note(
                    model=model,
                    fields=[question, markdown_to_html(answer)]
                )
                deck.add_note(note)
            question = line[5:]
            answer = []
            has_bullet_points = False
        elif line.startswith('##### '):
            if question and has_bullet_points:
                note = genanki.Note(
                    model=model,
                    fields=[question, markdown_to_html(answer)]
                )
                deck.add_note(note)
            question = line[6:]
            answer = []
            has_bullet_points = False

    if question and has_bullet_points:
        note = genanki.Note(
            model=model,
            fields=[question, markdown_to_html(answer)]
        )
        deck.add_note(note)

        def add_notes_for_heading_level(deck, model, text, heading_level):
            lines = text.split('\n')
            question = None
            answer = []
            has_bullet_points = False
            heading_prefix = '#' * heading_level + ' '
            subheading_prefix = '#' * (heading_level + 1) + ' '

            for line in lines:
                if line.startswith(heading_prefix):
                    if question and has_bullet_points:
                        note = genanki.Note(
                            model=model,
                            fields=[question, markdown_to_html(answer)]
                        )
                        deck.add_note(note)
                    question = line[len(heading_prefix):]
                    answer = []
                    has_bullet_points = False
                elif line.startswith(subheading_prefix):
                    answer.append(line[len(subheading_prefix):])
                    has_bullet_points = True

            if question and has_bullet_points:
                note = genanki.Note(
                    model=model,
                    fields=[question, markdown_to_html(answer)]
                )
                deck.add_note(note)

    add_notes_for_heading_level(deck, model, text, 2)
    add_notes_for_heading_level(deck, model, text, 3)
    add_notes_for_heading_level(deck, model, text, 4)
    return deck

anki_deck = parse_text_to_anki(text)
genanki.Package(anki_deck).write_to_file('markdown-anki-deck.apkg')
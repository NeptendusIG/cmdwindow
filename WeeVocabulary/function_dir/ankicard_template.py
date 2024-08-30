#####################################
#      Templates set - 28/12        #
#####################################
# NOTES :
"""
Templates set for Anki cards ;
Available : """
templates_and_fields = {
    "basic_qa": ["Front", "Back"],
    "basic_and_reversed": ["Front", "Back"],
    "images_pair": ["Front", "Back"],
}
# -- IMPORTS --
from genanki import Model, BASIC_MODEL

# -- VARIABLES INITIALISÉES --

basic_qa = Model(
    1,
    "Basic Q&A",
    fields=[
        {"name": "Front"},
        {"name": "Back"}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '<div style="font-size: 24px;">{{Front}}</div>',
            'afmt': '<div style="font-size: 18px;">{{Front}}<hr id="answer">{{Back}}</div>',
        },
    ]
)


basic_and_reversed = Model(
    2,
    "Basic QA and Reversed",
    fields=[
        {"name": "Front"},
        {"name": "Back"}
    ],
    templates=[
        {
            'name': 'reverse',
            'qfmt': '<div style="font-size: 24px;">{{Back}}</div>',
            'afmt': '<div style="font-size: 18px;">{{Back}}<hr id="answer">{{Front}}</div>',
        },
        {
            'name': 'right',
            'qfmt': '<div style="font-size: 24px;">{{Front}}</div>',
            'afmt': '<div style="font-size: 18px;">{{Front}}<hr id="answer">{{Back}}</div>',
        },
    ]
)


# This requires that the path is communicated to its package
# The 'Front' and 'Back' take only the filename (with its extension)
"""            'name': 'Card',
            'qfmt': '<id="front">{{Front}}',
            'afmt': '{{FrontSide}}<hr id="back">{{Back}}',"""
images_pair = Model(
    3,
    'Pair Images Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Card',
            'qfmt': '<img src={{Front}}>',
            'afmt': '{{FrontSide}}<hr><img src={{Back}}>',
        },
    ]
)


sound_to_word = Model(
    4,
    "Sound to Word",
    fields=[
        {"name": "Sound"},
        {"name": "Back"}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': "<div style='display:none;' Arial; font-size: 12px;'>{{Sound}}</div>",
            'afmt': '<hr><id="answer">{{Back}}</div>',
        },
    ]
)


cloze_deletion_model = Model(
    3,
    "Cloze Deletion",
    fields=[
        {"name": "Text"}
    ],
    templates=[
        {
            "name": "Card",
            "qfmt": '<div class="cloze">{{Text}}</div>',
        },
    ]
)


multiple_choice_model = Model(
    4,
    "Multiple Choice",
    fields=[
        {"name": "Question"},
        {"name": "Option1"},
        {"name": "Option2"},
        {"name": "Option3"},
        {"name": "Answer"}
    ],
    templates=[
        {
            "name": "Card",
            "qfmt": '<div class="question">{{Question}}</div><ul style="list-style-type:none;"><li>{{Option1}}</li><li>{{Option2}}</li><li>{{Option3}}</li></ul>',
            "afmt": '<div class="question">{{Question}}</div><ul style="list-style-type:none;"><li>{{Option1}}</li><li>{{Option2}}</li><li>{{Option3}}</li></ul><hr><div class="answer">{{Answer}}</div>',
        },
    ]
)



code_snippet_model = Model(
    5,
    "Code Snippet",
    fields=[
        {"name": "Task"},
        {"name": "Code"},
        {"name": "Explanation"}
    ],
    templates=[
        {
            "name": "Card",
            "qfmt": '<div class="task">{{Task}}</div><pre>{{Code}}</pre>',
            "afmt": '<div class="task">{{Task}}</div><pre>{{Code}}</pre><hr><div class="explanation">{{Explanation}}</div>',
        },
    ]
)





vocabulary_builder_latex_model = Model(
    6,
    "Vocabulary Builder (with LaTeX)",
    fields=[
        {"name": "Word"},
        {"name": "Definition"},
        {"name": "Example"}
    ],
    templates=[
        {
            "name": "Card",
            "qfmt": '<div class="word">{{Word}}</div>',
            "afmt": '<div class="word">{{Word}}</div><hr><div class="definition">{{Definition}}</div><br><div class="example">{{Example}}</div>',
        },
        {
            "name": "Card (Latex)",
            "qfmt": '<div class="word">{{Word}}</div>',
            "afmt": '<div class="word">{{Word}}</div><hr><div class="definition">{{Definition}}</div><br><div class="example">{{Example}}</div>',
            "latexPre": "\\documentclass[12pt]{article}\n\\usepackage{amsmath}\n\\pagestyle{empty}\n\\begin{document}\n",
            "latexPost": "\\end{document}",
        },
    ]
)



basic_cloze_model = Model(
    7,
    "Basic Cloze",
    fields=[
        {"name": "Text"},
        {"name": "Cloze"}
    ],
    templates=[
        {
            "name": "Card",
            "qfmt": '<div class="text">{{Text}}</div>',
            "afmt": '<div class="text">{{Text}}</div><hr><div class="cloze">{{Cloze}}</div>',
        },
    ]
)



basic_cloze_reversed_model = Model(
    8,
    "Basic Cloze (Reversed)",
    fields=[
        {"name": "Text"},
        {"name": "Cloze"}
    ],
    templates=[
        {
            "name": "Card",
            "qfmt": '<div class="cloze">{{Cloze}}</div>',
            "afmt": '<div class="cloze">{{Cloze}}</div><hr><div class="text">{{Text}}</div>',
        },
    ]
)


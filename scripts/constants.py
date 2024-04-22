PATH_TO_DATA = "/data/" # Path to main data folder

# Dictionary with words & corrections which are frequently transcribed incorrectly
REPLACEMENT_DICT = {
    "morfologenesis":"morphogenesis",
    }

# Header & Footer for creating Podcast transcript html pages
PRE_S = """
    <head><style>
            .text-block {
                width: 800px; /* Set the fixed width of the text block */
                padding: 10px; /* Optional: Adds some padding inside the text block */
                margin: 10px 0; /* Optional: Adds some margin outside the text block */
                word-wrap: break-word; /* Ensures long words are broken and wrapped to the next line */
                line-height: 1.3;
            }
            .main-header {
                text-decoration: underline;
                color: #348781;
            }
            body {
                font-family: sans-serif;
                font-size: 18px;
                color: #111;
                padding: 0 0 1em 0;
            }
            .l {
            color: #050;
            }
            .s {
                display: inline-block;
            }
            .e {
                display: inline-block;
            }
            .t {
                display: inline-block;
            }
        </style>
    </head>
    <a href="index.html">back to index</a>
    <h1 class="main-header"> Hamilton Morris Podcast</h1>
    """
    #<h2> \n\n  \n    \n    \n    \n    Hamilton Morris Podcast\n    \n  \n  \n    Youtube: Best Of Q&As\n  \n    \n </h2>
    #<a><img src="https://img.youtube.com/vi/LMhqTrAn56A/maxresdefault.jpg"> </a>"""
POST_S = """\n <a href='https://www.youtube.com/@HamiltonMorris'>YouTube Channel</a> | <a href='https://www.patreon.com/HamiltonMorris/'>Patreon</a>"""
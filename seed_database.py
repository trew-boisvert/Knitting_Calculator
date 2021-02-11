"""Script to seed database."""

# TODO What does sending it to the database as a list do?  
# What happens when I pull it out again later?  
# Where does JSON come into this?

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb knitting')
os.system('createdb knitting')

model.connect_to_db(server.app)
model.db.create_all()

stitch_library = [{
    "pattern_name": "Basket Weave Pattern",
    "pattern_description": "This is a simple English pattern that looks like the weave of a basket.",
    "pattern_instructions": ['Knit 1, Purl until last stitch in row, then knit 1 to finish.',
                             'Knit 1, purl 2.  Until last 5 stitches in row, repeat knitting 2 and purling 6.  Finish with knit 2, purl 2, knit 1.',
                              'Knit 3. Until last 5 stitches in row, repeat purling 2 and knitting 6.  Finish with purl 2, knit 3.', 
                              'Knit 1, purl 2.  Until last 5 stitches in row, repeat knitting 2 and purling 6.  Finish with knit 2, purl 2, knit 1.', 
                              'Knit 1, Purl until last stitch in row, then knit 1 to finish.', 
                              'Knit 1.  Until last 7 stitches in row, repeat purling 6 and knitting 2.  Finish with purl 6, knit 1.', 
                              'Knit 7, purl 2.  Until last 7 stitches in row, repeat knitting 6 and purling 2.  Finish with knit 7.',
                              'Knit 1.  Until last 7 stitches in row, repeat purling 6 and knitting 2.  Finish with purl 6, knit 1.'],
    "pattern_repeat_width": 8,
    "pattern_repeat_height": 8
},
{
    "pattern_name": "Bird's Eye Pattern",
    "pattern_description": "This has a lacy appearance when worked in fine yarn.",
    "pattern_instructions": ['Until the end of the row, knit 2 together, yarn over twice, knit 2 together.',
                            'Until last stitch of the row, knit 1, then knit 1 and purl 1 into the 2 yarnovers from last row.  Finish with knit 1.', 
                            'Knit 2.  Until last 2 stitches of row, knit 2 together, yarn over twice, knit 2 together. Finish with knit 2.', 
                            'Knit 2.  Until last 2 stitches of row, knit 1, then knit 1 and purl 1 into the 2 yarnovers from last row, then knit 1.  Finish with knit 2.'],
    "pattern_repeat_width": 4,
    "pattern_repeat_height": 4
},
{
    "pattern_name": "Block Pattern",
    "pattern_description": "A simple check design.",
    "pattern_instructions": ['Knit 5, purl 5, until the end of the row.', 
                            'Knit 5, purl 5, until the end of the row.',
                            'Knit 5, purl 5, until the end of the row.', 
                            'Knit 5, purl 5, until the end of the row.', 
                            'Knit 5, purl 5, until the end of the row.',
                            'Purl 5, Knit 5, until the end of the row.', 
                            'Purl 5, Knit 5, until the end of the row.', 
                            'Purl 5, Knit 5, until the end of the row.', 
                            'Purl 5, Knit 5, until the end of the row.', 
                            'Purl 5, Knit 5, until the end of the row.'],
    "pattern_repeat_width": 10,
    "pattern_repeat_height": 10
},
{
    "pattern_name": "Cat's Eye Pattern",
    "pattern_description": "A simple Shetland allover lace pattern.",
    "pattern_instructions": ['Purl 2. Until last 2 stitches of row, yarn over 1, purl 4 together.  Finish with purl 2.', 
                            'Knit 2.  Until last 2 stitches of row, knit 1, then, into the yarnover from last row, knit 1, purl 1, knit 1.  Finish with knit 2.', 
                            'Knit until end of row.'],
    "pattern_repeat_width": 4,
    "pattern_repeat_height": 3
},
{
    "pattern_name": "Dimple Eyelet",
    "pattern_description": "A dainty eyelet pattern.",
    "pattern_instructions": ['Knit until end of row.', 
                            'Purl until end of row.', 
                            'Purl 1.  Until last stitch of row, yarnover 1, purl 2 together. Finish by purling 1.', 
                            'Purl until end of row.', 
                            'Knit until end of row.',
                            'Purl until end of row', 
                            'Purl 2. Until end of row, yarnover 1, purl 2 together.', 
                            'Purl until end of row.'], 
    "pattern_repeat_width": 4,
    "pattern_repeat_height": 8
}
]


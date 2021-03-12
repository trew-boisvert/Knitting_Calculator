# Functions for backend calculations

def calculate_width(swatch_width, project_width, repeat_size):
    """Calculate number of stitches for knitting project width."""
    stitches = 0
    width = 0
    while width < project_width:
        stitches += repeat_size
        width += swatch_width
    return stitches

def calculate_height(swatch_height, project_height, repeat_size):
    rows = 0
    height = 0
    while height < project_height:
        rows += repeat_size
        height += swatch_height
    return rows

def get_instruction_array(list_of_objects):
    result = []
    for line in list_of_objects:
        result.append(line.instruction_text)
    return result

def get_project_object(list_of_objects):
    result = {}
    for obj in list_of_objects:
        result[obj.project_id] = obj.project_name
    return result
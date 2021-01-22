def checkered_throw_blanket():
    """Generates pattern for knitted checkered blanket based on stitch width and height.
    
    Calculates number of stiches for width and number of rows for height to create throw-sized blanket."""

    #print intro to program and instructions for user (includes pattern description and instructions to knit gauge swatch)
    #collect input - test gauge width and height
    blanket_size = 150

    test_swatch_width = float(input("How wide is your test swatch, in centimeters?    "))
    
    test_swatch_height = float(input("How tall/long is your test swatch, in centimeters?   "))

    design_pattern = ("Knit five, purl five, until the end of the row", "Purl five, Knit five, until the end of the row")
    #test swatch should have same number of stitches as one repeat of design
    def calculate_width(swatch_width, blanket_width):
        stitches = 0
        repeat_size = 10
        width = 0
        while width < blanket_width:
            stitches += repeat_size
            width += swatch_width
        return stitches
    cast_on = calculate_width(test_swatch_width, blanket_size)

    def calculate_height(swatch_height, blanket_height):
        rows = 0
        repeat_size = 10
        height = 0
        while height < blanket_height:
            rows += repeat_size
            height += swatch_height
        return rows
    row_total = calculate_height(test_swatch_height, blanket_size)
    print(cast_on)
    print(row_total)
checkered_throw_blanket()

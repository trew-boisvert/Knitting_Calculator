def checkered_throw_blanket():
    """Generates pattern for knitted checkered blanket based on stitch width and height.
    
    Calculates number of stiches for width and number of rows for height to create throw-sized blanket."""

    print('Checker-pattern Knitted Throw Blanket Calculator')
    print()
    print('________________________________________________')
    print()
    print('Welcome to my knitting calculator!')
    print('Usually knitting patterns have a set number of stitches and rows, and require you to adjust your stitch size to fit the pattern.')
    print('This calculator flips that around, and instead adjusts the number of stitches and rows in the pattern to work with your stitch size.')
    print('This gives you the freedom to pick any size needle or yarn you want to work with, and end up with a blanket of the correct size.')
    print('So exciting!')
    print('Bear in mind, you will still need to knit a swatch to collect some initial measurements from.')
    print("And it's important to note that this pattern will round calculations up to the next full repeat of the design, so your blanket might be slightly larger than the given finished size, which is 150cm x 150cm.")
    print('Currently this program only generates a pattern for a throw-sized blanket with a checkered pattern.')
    print("Let's get started!")
    print()
    print('First, please knit a swatch that is 10 stitches wide and 10 rows tall, using a Stockinette stitch.')
    print("That means alternate between knitting an entire row and then purling an entire row.")
    print('Measurements will need to be in centimeters, not inches.')
    print('When prompted, please only type the number for the measurement asked, and don\'t use any letters or unexpected symbols.')
    print('For example, type "10.3" and then hit enter.  Don\'t type "10.3 cm" because I haven\'t written the code to deal with unexpected input yet.')
    print("I'll do that later, but for now, this is a beta version, and I need you to be gentle with it.")
    print('Nothing bad will happen if you put in the wrong input right now, it just won\'t work.')
    print("Feedback, suggestions, and ideas for features to add are strongly encouraged!")
    print('Please contact me at the Twitter you got this link from.')
    print()
    print()
    
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

    print("The number of stitches you should cast on is:", cast_on)
    print("The number of rows you should knit is:", row_total)

    #figure out loop to iterate over design_pattern tuple and print instructions for each row, as well as track current row
    #must take input from user after printing row instructions to print next row
    #when loop ends, print cast-off instructions and quit program
checkered_throw_blanket()

let blanketSize = 150;

let testSwatchWidth = parseFloat(prompt("How wide is your test swatch, in centimeters?"));

let testSwatchHeight = parseFloat(prompt("How tall/long is your test swatch, in centimeters?"));

//test swatch should have same number of stitches as one repeat of design
const calculateWidth = (swatchWidth, blanketWidth) => {
    let stitches = 0
    let repeatSize = 10
    let width = 0

    while (width < blanketWidth){
        stitches += repeatSize;
        width += swatchWidth;
    }
    return stitches;
};

let castOn = calculateWidth(testSwatchWidth, blanketSize);

const calculateHeight = (swatchHeight, blanketHeight) => {
    let rows = 0
    let repeatSize = 10
    let height = 0

    while(height < blanketHeight){
        rows += repeatSize;
        height += swatchHeight;
    }
    return rows;
};

let rowTotal = calculateHeight(testSwatchHeight, blanketSize);

console.log(`The number of stitches you need to cast on is: ${castOn}`)
console.log(`The number of rows you'll need to knit is: ${rowTotal}`)

let designPattern = ["Knit five, purl five, until the end of the row", "Knit five, purl five, until the end of the row", "Knit five, purl five, until the end of the row", "Knit five, purl five, until the end of the row", "Knit five, purl five, until the end of the row", "Purl five, Knit five, until the end of the row", "Purl five, Knit five, until the end of the row", "Purl five, Knit five, until the end of the row", "Purl five, Knit five, until the end of the row", "Purl five, Knit five, until the end of the row"]

let currentRow = 0;

while(currentRow < rowTotal){
    for(let i = 0; i < designPattern.length; i++){
        console.log(`Row: ${currentRow + 1}`);
        console.log(designPattern[i]);
        currentRow++;
        let ready = prompt("Next Row?   ");
    }
}

console.log(`That's all the rows you need to knit!`);
console.log(`Just cast off and you're done!`);
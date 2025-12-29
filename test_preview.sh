#!/bin/bash
# Preview ZPL without printing
ZPL_FILE="akacia_250g_final.zpl"

echo "Testing ZPL at labelary.com preview service..."
echo ""
echo "URL to preview (paste in browser):"
echo "http://api.labelary.com/v1/printers/8dpmm/labels/2.25x1.25/0/"
echo ""
echo "Or run this curl command to get a PNG preview:"
echo "curl -X POST http://api.labelary.com/v1/printers/8dpmm/labels/2.25x1.25/0/ \\"
echo "  -d @${ZPL_FILE} \\"
echo "  -o preview.png"
echo ""
echo "Number of ^XA...^XZ blocks in file:"
grep -c "^XA" ${ZPL_FILE}
echo ""
echo "If this shows '1', it should print exactly 1 label."

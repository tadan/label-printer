#!/bin/bash
# Quick script to print shipping labels (102x152mm) to Zebra GK420d

PRINTER_NAME="Zebra_Technologies_ZTC_GK420d"
LABEL_DIR="shipping-labels"

# Check if file argument provided
if [ -z "$1" ]; then
    echo "Usage: ./print_shipping_label.sh <filename.pdf>"
    echo ""
    echo "Available labels in $LABEL_DIR:"
    ls -1 "$LABEL_DIR"/*.pdf 2>/dev/null | xargs -n1 basename
    exit 1
fi

# Check if file exists
if [ ! -f "$LABEL_DIR/$1" ]; then
    echo "Error: File not found: $LABEL_DIR/$1"
    exit 1
fi

# Print the label
echo "🖨️  Printing: $1"
echo "   To: $PRINTER_NAME"
lpr -P "$PRINTER_NAME" -o fit-to-page -o media=Custom.103x210mm "$LABEL_DIR/$1"

if [ $? -eq 0 ]; then
    echo "✅ Print job sent successfully!"
else
    echo "❌ Print failed"
    exit 1
fi

# Cuppino Label Printer

Swedish food compliance label printing system for Zebra GK420d thermal printer.

## Features

- 🏷️ **Two Label Types:**
  - **Full Compliance Labels** (250g, 500g jars, olive pates): All EU/Swedish mandatory information
  - **QR Code Labels** (50g jars): Minimal info + QR code linking to full details on Shopify

- 🌐 **Web Interface:** User-friendly form for selecting products and entering variable data
- 🖨️ **Multiple Connection Options:** USB, Network (Ethernet/WiFi), or File Export
- 📊 **Product Database:** All Swedish translations and compliance data in YAML format
- 🔧 **Easy Configuration:** Web-based printer setup

## Label Specifications

- **Size:** 75x51mm (split from 75x102mm sheets)
- **Printer:** Zebra GK420d (203 DPI)
- **Format:** ZPL (Zebra Programming Language)

## Products Supported

### Honey Products (Apicoltura Bianco)
- Acacia Honey: 50g (QR), 250g (Full), 500g (Full)
- Wildflower Honey (Millefiori): 50g (QR), 250g (Full)
- Honeydew Honey (Melata): 250g (Full)
- Chestnut Honey (Castagno): 250g (Full)

### Olive Products (Natural)
- Black Olive Pate: 190g (Full)
- Green Olive Pate: 190g (Full)

## Installation

### Prerequisites

- Python 3.8 or higher
- Zebra GK420d printer

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd label-printer
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify product database:**
   - Check `products.yaml` for all product information
   - Update TODO items for olive pate products (translate from Italian labels)
   - Add your complete Swedish address in the `common.importer_full` field

## Usage

### Starting the Application

```bash
python app.py
```

The web server will start at: **http://localhost:5000**

### Printer Configuration

1. Open **http://localhost:5000/config**
2. Select connection type:
   - **File Export:** Saves ZPL to file (good for testing)
   - **Network:** Requires printer IP address (recommended for production)
   - **USB:** Uses system printer name

#### Network Setup (Recommended)
- Ensure Zebra GK420d has a network adapter
- Find printer IP address (check printer network settings or router)
- Enter IP and port (default: 9100) in config page
- Test connection

#### USB Setup
- Connect printer via USB
- Add printer in system settings:
  - **macOS:** System Settings → Printers & Scanners
  - **Windows:** Control Panel → Devices and Printers
- Enter printer name in config page

### Printing Labels

1. **Select Product Category:** Honey or Olive Pates
2. **Choose Product:** Pick from dropdown (shows SKU, name, weight)
3. **Enter Variable Data:**
   - **Best Before Date:** Auto-suggested 24 months from today
   - **Batch ID:** Auto-filled with SKU (can customize)
   - **Quantity:** Number of labels to print
4. **Preview (Optional):** Click "Preview ZPL" to see generated code
5. **Print:** Click "Print Labels"

### Label Types

**Full Compliance Label** includes:
- Product name (Swedish)
- Net quantity
- Ingredients (Swedish)
- Allergens
- Nutrition declaration per 100g
- Storage instructions
- Best-before date
- Batch ID
- Origin, Producer, Importer

**QR Code Label** includes:
- Product name
- Net quantity
- Best-before date
- Batch ID
- QR code (→ Shopify product page with full Swedish compliance info)
- Producer/Importer details

## Product Database

Edit `products.yaml` to:
- Add new products
- Update Swedish translations
- Modify nutrition values
- Change QR code URLs

### Example Product Entry:

```yaml
AB-ACACIA-250:
  name_sv: "Akaciahonung"
  weight: "250g"
  label_type: "full"
  ingredients_sv: "100% Akaciahonung"
  allergens_sv: "Inga kända allergener"
  nutrition:
    energy_kj: "1340"
    energy_kcal: "320"
    fat: "0g"
    carbs: "82g"
    carbs_sugars: "82g"
    protein: "0,2g"
    salt: "0,01g"
  storage_sv: "Förvaras svalt och torrt, skyddad från ljus"
  origin: "Italien (Abruzzo, Guardiagrele)"
  producer: "Apicoltura Bianco, Guardiagrele (CH), Italien"
  importer: "GGMR AB (Cuppino)"
  qr_url: "https://cuppino.it/products/..."
```

## TODO: Complete Olive Pate Data

The olive pate products need Swedish translations from Italian labels:

1. Get Italian labels for:
   - NAT-907-BLACKOLIVE (Paté di Olive Nere)
   - NAT-908-GREENOLIVE (Paté di Olive Verdi)

2. Translate to Swedish:
   - Ingredients list (Ingredienser)
   - Allergen information (Allergener)
   - Nutrition facts (Näringsdeklaration)
   - Storage instructions (Förvaring)

3. Update `products.yaml` (replace TODO items)

## Shopify Integration

### Adding Swedish Compliance Info to Product Pages

For QR code labels to work properly, add Swedish compliance sections to Shopify:

1. Go to Shopify Admin → Products
2. For each honey product, add this section to description:

```html
<h3>PRODUKTINFORMATION (Svensk märkning)</h3>
<p><strong>Ingredienser:</strong> 100% [Honung typ]</p>
<p><strong>Allergener:</strong> Inga kända allergener</p>
<p><strong>Näringsdeklaration per 100g:</strong><br>
Energi: 1340 kJ / 320 kcal<br>
Fett: 0g<br>
Kolhydrater: 82g, varav sockerarter: 82g<br>
Protein: 0,2g<br>
Salt: 0,01g</p>
<p><strong>Förvaring:</strong> Förvaras svalt och torrt, skyddad från ljus</p>
<p><strong>Bäst före:</strong> Se etikett</p>
<p><strong>Ursprung:</strong> Italien (Abruzzo, Guardiagrele)</p>
<p><strong>Producent:</strong> Apicoltura Bianco, Guardiagrele (CH), Italien</p>
<p><strong>Importör:</strong> GGMR AB (Cuppino), [address]</p>
<p><strong>Partimärkning:</strong> Se etikett</p>
```

## File Structure

```
label-printer/
├── app.py                    # Main Flask application
├── printer.py                # Printer communication module
├── products.yaml             # Product database (Swedish translations)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── templates/
│   ├── index.html           # Main label printing interface
│   └── config.html          # Printer configuration page
├── static/
│   └── style.css            # Web interface styling
└── zpl_templates/
    ├── type_a_full.zpl      # Full compliance label template
    └── type_b_qr.zpl        # QR code label template
```

## Troubleshooting

### Labels not printing

1. **Check connection type in config**
2. **Network:** Verify printer IP, ensure printer is on network
3. **USB:** Check printer is connected and recognized by system
4. **Try File Export mode** to verify ZPL generation is working

### Text not displaying correctly

- Zebra GK420d supports limited character sets
- Swedish characters (å, ä, ö) should work with UTF-8 encoding
- If issues persist, test with simpler characters first

### Label size incorrect

- Verify label dimensions in printer settings
- Check ZPL templates (`^PW` and `^LL` commands)
- Current settings: 598x408 dots at 203 DPI = 75x51mm

### QR codes not working

- Test URL in browser first
- Ensure QR code size is appropriate (currently 6x scale)
- Verify printer can print QR codes (GK420d supports it)

## ZPL Manual Printing

If you prefer manual control, export ZPL files and send them directly:

### macOS/Linux (Network)
```bash
cat label_20250101_120000.zpl | nc 192.168.1.100 9100
```

### Windows (USB)
```cmd
type label_20250101_120000.zpl > \\localhost\Zebra_GK420d
```

## License

Proprietary - Cuppino / GGMR AB

## Support

For issues or questions, contact: [your contact info]

---

**Version:** 1.0
**Last Updated:** December 2025
**Printer Model:** Zebra GK420d (203 DPI)
**Label Size:** 75x51mm

# Quick Start Guide - Cuppino Label Printer

## Get Started in 5 Minutes

### 1. Install Dependencies

```bash
cd label-printer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Complete Product Data (Required)

Open `products.yaml` and update:

1. **Add your Swedish address:**

    ```yaml
    common:
        importer_full: 'GGMR AB (Cuppino), info@cuppino.se - Malmö, Sweden'
    ```

2. **Add olive pate data** (translate from Italian labels):
    - Search for "TODO" in products.yaml
    - Replace with Swedish ingredient lists, allergens, nutrition facts

### 3. Start the Application

```bash
python app.py
```

Open browser: **http://localhost:5000**

### 4. Configure Printer

**First time setup:**

1. Go to: http://localhost:5000/config
2. Choose connection type:
    - **Start with "File Export"** for testing
    - **Switch to "Network"** when ready for production
3. Save configuration

### 5. Print Your First Label

1. Select **"Honey"** category
2. Choose **"Akaciahonung - 250g"**
3. Keep default best-before date
4. Set quantity: **1**
5. Click **"Preview ZPL"** to see generated code
6. Click **"Print Labels"** (will save to file in test mode)

### 6. Test Label with Printer

**File Export Mode (Testing):**

-   ZPL saved to `label_YYYYMMDD_HHMMSS.zpl`
-   Send manually to printer or review code

**Network Mode (Production):**

1. Find your printer's IP address
2. Enter in config page: http://localhost:5000/config
3. Test connection
4. Print directly from web interface

## Next Steps

### Add Swedish Compliance to Shopify

For QR code labels (50g jars) to work, add Swedish compliance info to product pages:

**Example for Acacia 50g:**
https://cuppino.it/products/italian-acacia-honey-from-abruzzo-miele-di-acacia?variant=52781821395271

Add this section to the product description:

```
PRODUKTINFORMATION (Svensk märkning)

Ingredienser: 100% Akaciahonung
Allergener: Inga kända allergener

Näringsdeklaration per 100g:
Energi: 1340 kJ / 320 kcal
Fett: 0g
Kolhydrater: 82g, varav sockerarter: 82g
Protein: 0,2g
Salt: 0,01g

Förvaring: Förvaras svalt och torrt, skyddad från ljus
Bäst före: Se etikett
Ursprung: Italien (Abruzzo, Guardiagrele)
Producent: Apicoltura Bianco, Guardiagrele (CH), Italien
Importör: GGMR AB (Cuppino), [your address]
Partimärkning: Se etikett
```

### Complete Olive Pate Translations

Get the Italian labels for:

-   Black Olive Pate (Paté di Olive Nere)
-   Green Olive Pate (Paté di Olive Verdi)

Translate and add to `products.yaml`

## Troubleshooting

**"Module not found" error:**

```bash
pip install Flask PyYAML
```

**Can't access http://localhost:5000:**

-   Check firewall settings
-   Try http://127.0.0.1:5000

**Labels won't print (Network mode):**

-   Verify printer IP address
-   Check printer is connected to network
-   Test with File Export mode first

**Swedish characters not showing:**

-   Should work automatically with UTF-8
-   If issues, check printer firmware supports international characters

## Support

Full documentation: See `README.md`

Common tasks:

-   Add new products: Edit `products.yaml`
-   Adjust label layout: Edit ZPL templates in `zpl_templates/`
-   Change printer settings: http://localhost:5000/config

---

🎉 **You're ready to print Swedish compliance labels!**

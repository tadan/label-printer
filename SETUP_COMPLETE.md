# Cuppino Label Printer - Setup Complete! 🎉

**Date:** December 4, 2025
**Printer:** Zebra GK420d (USB connected)
**System Printer Name:** `Zebra_Technologies_ZTC_GK420d`

---

## ✅ What's Ready

### 1. Product Labels (57mm x 32mm)
- **Size:** 57mm x 32mm - Small supplementary labels
- **All products use QR code format** (Type B labels)
- **What's printed:**
  - Product name (Swedish)
  - Net weight
  - Best-before date
  - Batch ID
  - QR code → Full Swedish compliance on Shopify
  - Importer info

**Products configured:**
- Acacia Honey: 50g, 250g, 500g
- Wildflower Honey (Millefiori): 50g, 250g
- Honeydew Honey (Melata): 250g
- Chestnut Honey (Castagno): 250g
- Black Olive Pate: 190g
- Green Olive Pate: 190g

### 2. Shipping Labels (102mm x 152mm)
- **Size:** 102mm x 152mm (4" x 6" standard)
- **Format:** PDF from Shiplink
- **Print command:** Ready to use

---

## 🖨️ How to Print

### Product Labels (Web Interface)

```bash
cd "/Users/danieletatasciore/Documents/repos/claude/01 - Cuppino/label-printer"
python app.py
```

Then open: **http://localhost:5000**

1. Select product category (Honey/Olive)
2. Choose product from dropdown
3. Enter best-before date (auto-suggested)
4. Enter batch ID (auto-filled with SKU)
5. Set quantity
6. Click "Print Labels"

### Shipping Labels (Quick Script)

**Option 1: Quick script**
```bash
cd "/Users/danieletatasciore/Documents/repos/claude/01 - Cuppino/label-printer"
./print_shipping_label.sh erik-rabe-01.pdf
```

**Option 2: Direct command**
```bash
lpr -P Zebra_Technologies_ZTC_GK420d -o fit-to-page -o media=Custom.103x210mm shipping-labels/your-label.pdf
```

---

## 📦 Label Sizes You Ordered

**Product Labels:** 57mm x 32mm (Direct Thermal)
- For all jar sizes (50g, 250g, 500g, 190g)
- Supplementary labels with QR codes
- Won't cover much of Italian labels

**Shipping Labels:** 102mm x 152mm (Direct Thermal)
- Standard 4"x6" size
- Compatible with all carriers
- Works with Shiplink PDFs

---

## ⚠️ Important: Update Shopify Product Pages

Since all products now use QR code labels, you MUST add full Swedish compliance info to Shopify product pages.

### Add to Each Product Description:

```html
<h3>PRODUKTINFORMATION (Svensk märkning)</h3>

<p><strong>Ingredienser:</strong> 100% [Honung typ eller Olivkräm]</p>

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

<p><strong>Importör:</strong> GGMR AB (Cuppino), [YOUR ADDRESS]</p>

<p><strong>Partimärkning:</strong> Se etikett</p>
```

**For honey products:** Use honey-specific values (shown above)
**For olive pates:** Update with olive pate nutrition values (when you translate Italian labels)

---

## 📋 TODO: Complete Olive Pate Data

The olive pate products still need Swedish translations from Italian labels.

**Edit:** `/Users/danieletatasciore/Documents/repos/claude/01 - Cuppino/label-printer/products.yaml`

Search for **"TODO"** and replace with:
- Ingredients list (Swedish)
- Allergen information
- Nutrition facts
- Storage instructions

**Products needing translation:**
- NAT-907-BLACKOLIVE (Paté di Olive Nere)
- NAT-908-GREENOLIVE (Paté di Olive Verdi)

---

## 🔧 Printer Troubleshooting

### Red Blinking Light
- **Check:** Labels loaded correctly
- **Check:** Print head closed firmly (click sound)
- **Fix:** Hold FEED button for 2-3 seconds to calibrate

### Labels Print Partially
- Use the command with label size specified:
  ```bash
  lpr -P Zebra_Technologies_ZTC_GK420d -o fit-to-page -o media=Custom.103x210mm shipping-labels/file.pdf
  ```

### Printer Not Showing Up
- **Check:** USB cable connected
- **Check:** Printer powered on (green light)
- **Fix:** Go to System Settings → Printers & Scanners → Add Printer

---

## 📁 Project Structure

```
label-printer/
├── app.py                          # Web application
├── printer.py                      # Printer communication
├── products.yaml                   # Product database ⚠️ EDIT THIS
├── print_shipping_label.sh         # Quick shipping label script
├── templates/
│   ├── index.html                 # Main interface
│   └── config.html                # Printer settings
├── zpl_templates/
│   ├── type_qr.zpl                # 57x32mm QR label template
│   ├── type_qr_57x32.zpl          # (same, backup)
│   ├── type_b_qr.zpl              # (old 75x51mm, backup)
│   └── type_a_full.zpl            # (old full label, backup)
└── shipping-labels/
    └── *.pdf                       # Drop shipping PDFs here
```

---

## 🎯 Quick Reference Commands

**Print product labels (web interface):**
```bash
cd label-printer && python app.py
# Then open http://localhost:5000
```

**Print shipping label:**
```bash
cd label-printer
./print_shipping_label.sh your-label.pdf
```

**Check printer status:**
```bash
lpstat -p Zebra_Technologies_ZTC_GK420d
```

**List pending print jobs:**
```bash
lpq -P Zebra_Technologies_ZTC_GK420d
```

---

## ✨ System Features

✅ Two label sizes (57x32mm products, 102x152mm shipping)
✅ QR code labels link to Shopify for full compliance
✅ Web interface for easy product label printing
✅ Quick command-line shipping label printing
✅ All products configured (honey + olive pates)
✅ Swedish compliance data for honey products
✅ Zebra GK420d successfully connected via USB

---

**Next Steps:**
1. Update Shopify product pages with Swedish compliance info
2. Translate olive pate data from Italian labels
3. Test print some product labels when labels arrive
4. Add your full Swedish address to `products.yaml`

**System is ready to use as soon as labels arrive! 🚀**

---

*For detailed documentation, see README.md*
*For quick start, see QUICKSTART.md*

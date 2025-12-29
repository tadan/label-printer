"""
Cuppino Label Printer - Flask Web Application
Web interface for printing Swedish compliance labels on Zebra GK420d
"""

from flask import Flask, render_template, request, jsonify
import yaml
from datetime import datetime, timedelta
from printer import create_printer

app = Flask(__name__)

# Load product database
with open('products.yaml', 'r', encoding='utf-8') as f:
    product_data = yaml.safe_load(f)

# Printer configuration (can be modified via web interface)
printer_config = {
    'type': 'usb',  # USB mode configured
    'ip': None,
    'port': 9100,
    'printer_name': 'Zebra_Technologies_ZTC_GK420d'
}


@app.route('/')
def index():
    """Main page with product selection form"""
    products = product_data['products']

    # Group products by type
    honey_products = {k: v for k, v in products.items() if k.startswith('AB-')}
    olive_products = {k: v for k, v in products.items() if k.startswith('NAT-')}

    return render_template('index.html',
                         honey_products=honey_products,
                         olive_products=olive_products,
                         common=product_data['common'])


@app.route('/api/product/<sku>')
def get_product(sku):
    """Get product details by SKU"""
    product = product_data['products'].get(sku)
    if product:
        return jsonify({'status': 'success', 'product': product})
    return jsonify({'status': 'error', 'message': 'Product not found'}), 404


@app.route('/api/generate-zpl', methods=['POST'])
def generate_zpl():
    """Generate ZPL code from product data and user input"""
    data = request.json
    sku = data.get('sku')
    best_before = data.get('best_before')

    product = product_data['products'].get(sku)
    if not product:
        return jsonify({'status': 'error', 'message': 'Product not found'}), 404

    # Use batch from product data if available, otherwise from request, otherwise SKU
    batch = data.get('batch', product.get('batch', sku))
    quantity = int(data.get('quantity', 1))

    # Load QR label template (57x32mm)
    template_file = "zpl_templates/type_qr_57x32.zpl"
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            zpl_template = f.read()
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': f'Template not found: {template_file}'}), 500

    # Generate QR code label
    zpl_code = zpl_template.format(
        product_name=product['name_sv'],
        weight=product['weight'],
        best_before=best_before,
        batch=batch,
        disposal=product['disposal_sv'],
        qr_url=product['qr_url'],
        producer=product['producer'],
        importer=product['importer'],
        origin=product['origin']
    )

    return jsonify({
        'status': 'success',
        'zpl_code': zpl_code,
        'quantity': quantity,
        'label_type': product['label_type']
    })


@app.route('/api/print', methods=['POST'])
def print_label():
    """Print label(s) using configured printer"""
    data = request.json
    zpl_code = data.get('zpl_code')
    quantity = int(data.get('quantity', 1))

    if not zpl_code:
        return jsonify({'status': 'error', 'message': 'No ZPL code provided'}), 400

    # Create printer instance and print
    printer = create_printer(printer_config)
    result = printer.print_zpl(zpl_code, quantity)

    return jsonify(result)


@app.route('/api/config/printer', methods=['GET', 'POST'])
def printer_config_route():
    """Get or update printer configuration"""
    global printer_config

    if request.method == 'GET':
        return jsonify({'status': 'success', 'config': printer_config})

    elif request.method == 'POST':
        data = request.json
        printer_config.update({
            'type': data.get('type', printer_config['type']),
            'ip': data.get('ip', printer_config['ip']),
            'port': int(data.get('port', printer_config['port'])),
            'printer_name': data.get('printer_name', printer_config['printer_name'])
        })
        return jsonify({'status': 'success', 'message': 'Configuration updated', 'config': printer_config})


@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Test printer connection"""
    printer = create_printer(printer_config)
    result = printer.test_connection()
    return jsonify(result)


@app.route('/config')
def config_page():
    """Printer configuration page"""
    return render_template('config.html', config=printer_config)


@app.template_filter('suggest_best_before')
def suggest_best_before(months=24):
    """Template filter to suggest best-before date"""
    months = int(months) if months else 24
    date = datetime.now() + timedelta(days=months*30)
    return date.strftime('%Y-%m-%d')


if __name__ == '__main__':
    print("\n" + "="*60)
    print("   CUPPINO LABEL PRINTER")
    print("   Swedish Compliance Labels for Zebra GK420d")
    print("="*60)
    print("\n🌐 Starting web server...")
    print("📍 Open your browser to: http://localhost:5001")
    print("\n⚙️  Current printer configuration:")
    print(f"   Connection type: {printer_config['type']}")
    if printer_config['type'] == 'network':
        print(f"   IP: {printer_config['ip']}:{printer_config['port']}")
    elif printer_config['type'] == 'usb':
        print(f"   Printer: {printer_config['printer_name']}")
    print("\n💡 Change configuration at: http://localhost:5001/config")
    print("\n" + "="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5001)

#!/usr/bin/env python3
"""
Simple utility to print PDF shipping labels to Zebra GK420d
"""

import subprocess
import sys
import os
import platform


def list_printers():
    """List available printers on the system"""
    system = platform.system()

    if system == 'Darwin':  # macOS
        result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
        print("\nAvailable printers:")
        print(result.stdout)
    elif system == 'Windows':
        result = subprocess.run(['wmic', 'printer', 'get', 'name'],
                              capture_output=True, text=True)
        print("\nAvailable printers:")
        print(result.stdout)
    elif system == 'Linux':
        result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
        print("\nAvailable printers:")
        print(result.stdout)


def print_pdf(pdf_path, printer_name=None):
    """
    Print PDF to specified printer

    Args:
        pdf_path: Path to PDF file
        printer_name: Name of printer (if None, uses default)
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found: {pdf_path}")
        return False

    system = platform.system()

    try:
        if system == 'Darwin':  # macOS
            if printer_name:
                cmd = ['lpr', '-P', printer_name, pdf_path]
            else:
                cmd = ['lpr', pdf_path]

            print(f"\n🖨️  Printing: {os.path.basename(pdf_path)}")
            if printer_name:
                print(f"   To printer: {printer_name}")

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Print job sent successfully!")
                return True
            else:
                print(f"❌ Print failed: {result.stderr}")
                return False

        elif system == 'Windows':
            # Windows printing
            if printer_name:
                cmd = ['print', '/D:' + printer_name, pdf_path]
            else:
                cmd = ['print', pdf_path]

            print(f"\n🖨️  Printing: {os.path.basename(pdf_path)}")
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

            if result.returncode == 0:
                print("✅ Print job sent successfully!")
                return True
            else:
                print(f"❌ Print failed: {result.stderr}")
                return False

        elif system == 'Linux':
            # Linux printing
            if printer_name:
                cmd = ['lp', '-d', printer_name, pdf_path]
            else:
                cmd = ['lp', pdf_path]

            print(f"\n🖨️  Printing: {os.path.basename(pdf_path)}")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Print job sent successfully!")
                return True
            else:
                print(f"❌ Print failed: {result.stderr}")
                return False
        else:
            print(f"❌ Unsupported operating system: {system}")
            return False

    except FileNotFoundError as e:
        print(f"❌ Print command not found. Make sure your printer is installed.")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error printing: {e}")
        return False


def main():
    """Main function for CLI usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Print PDF shipping labels to Zebra GK420d'
    )
    parser.add_argument('pdf_file', nargs='?', help='PDF file to print')
    parser.add_argument('-p', '--printer', help='Printer name (optional)')
    parser.add_argument('-l', '--list', action='store_true',
                       help='List available printers')

    args = parser.parse_args()

    if args.list:
        list_printers()
        return

    if not args.pdf_file:
        print("❌ No PDF file specified")
        print("\nUsage:")
        print("  python print_pdf.py shipping-labels/rafael-vilen-01.pdf")
        print("  python print_pdf.py shipping-labels/rafael-vilen-01.pdf -p Zebra_GK420d")
        print("  python print_pdf.py --list  (to see available printers)")
        sys.exit(1)

    success = print_pdf(args.pdf_file, args.printer)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

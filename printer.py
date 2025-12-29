"""
Printer communication module for Zebra GK420d
Supports multiple connection methods: USB, Network, and File Export
"""

import socket
import platform
import subprocess
from typing import Optional


class ZebraPrinter:
    """Handle communication with Zebra GK420d printer"""

    def __init__(self, connection_type: str = 'file', **kwargs):
        """
        Initialize printer connection

        Args:
            connection_type: 'usb', 'network', or 'file'
            **kwargs: Additional connection parameters
                - ip: IP address for network connection
                - port: Port for network connection (default: 9100)
                - printer_name: System printer name for USB
        """
        self.connection_type = connection_type
        self.ip = kwargs.get('ip')
        self.port = kwargs.get('port', 9100)
        self.printer_name = kwargs.get('printer_name', 'Zebra_GK420d')

    def print_zpl(self, zpl_code: str, quantity: int = 1) -> dict:
        """
        Send ZPL code to printer

        Args:
            zpl_code: ZPL code string to print
            quantity: Number of labels to print

        Returns:
            dict with status and message
        """
        try:
            if self.connection_type == 'network':
                return self._print_network(zpl_code, quantity)
            elif self.connection_type == 'usb':
                return self._print_usb(zpl_code, quantity)
            elif self.connection_type == 'file':
                return self._export_file(zpl_code, quantity)
            else:
                return {'status': 'error', 'message': f'Unknown connection type: {self.connection_type}'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _print_network(self, zpl_code: str, quantity: int) -> dict:
        """Send ZPL to printer via network"""
        if not self.ip:
            return {'status': 'error', 'message': 'IP address not configured'}

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.ip, self.port))

            for _ in range(quantity):
                sock.send(zpl_code.encode('utf-8'))

            sock.close()
            return {
                'status': 'success',
                'message': f'{quantity} label(s) sent to printer at {self.ip}:{self.port}'
            }
        except socket.timeout:
            return {'status': 'error', 'message': 'Connection timeout - check printer IP and network'}
        except ConnectionRefusedError:
            return {'status': 'error', 'message': 'Connection refused - check printer is online and port 9100 is open'}
        except Exception as e:
            return {'status': 'error', 'message': f'Network error: {str(e)}'}

    def _print_usb(self, zpl_code: str, quantity: int) -> dict:
        """Send ZPL to printer via USB using system commands"""
        try:
            system = platform.system()

            if system == 'Darwin':  # macOS
                # Use lpr command to send to printer
                for _ in range(quantity):
                    process = subprocess.Popen(
                        ['lpr', '-P', self.printer_name, '-o', 'raw'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate(zpl_code.encode('utf-8'))

                    if process.returncode != 0:
                        return {'status': 'error', 'message': f'Print failed: {stderr.decode()}'}

                return {
                    'status': 'success',
                    'message': f'{quantity} label(s) sent to {self.printer_name}'
                }

            elif system == 'Windows':
                # Windows: write to printer port
                for _ in range(quantity):
                    with open(f'\\\\localhost\\{self.printer_name}', 'wb') as printer:
                        printer.write(zpl_code.encode('utf-8'))

                return {
                    'status': 'success',
                    'message': f'{quantity} label(s) sent to {self.printer_name}'
                }

            elif system == 'Linux':
                # Linux: use lp command
                for _ in range(quantity):
                    process = subprocess.Popen(
                        ['lp', '-d', self.printer_name, '-o', 'raw'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate(zpl_code.encode('utf-8'))

                    if process.returncode != 0:
                        return {'status': 'error', 'message': f'Print failed: {stderr.decode()}'}

                return {
                    'status': 'success',
                    'message': f'{quantity} label(s) sent to {self.printer_name}'
                }

            else:
                return {'status': 'error', 'message': f'Unsupported operating system: {system}'}

        except FileNotFoundError:
            return {'status': 'error', 'message': f'Printer "{self.printer_name}" not found'}
        except Exception as e:
            return {'status': 'error', 'message': f'USB print error: {str(e)}'}

    def _export_file(self, zpl_code: str, quantity: int) -> dict:
        """Export ZPL to file for manual printing or review"""
        import datetime

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'label_{timestamp}.zpl'

        try:
            # Write ZPL code repeated for quantity
            with open(filename, 'w', encoding='utf-8') as f:
                for i in range(quantity):
                    f.write(f'# Label {i+1}/{quantity}\n')
                    f.write(zpl_code)
                    f.write('\n\n')

            return {
                'status': 'success',
                'message': f'ZPL exported to {filename}',
                'filename': filename,
                'zpl_code': zpl_code
            }
        except Exception as e:
            return {'status': 'error', 'message': f'File export error: {str(e)}'}

    def test_connection(self) -> dict:
        """Test printer connection"""
        test_zpl = '^XA^FO50,50^ADN,36,20^FDTest^FS^XZ'

        if self.connection_type == 'network':
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.ip, self.port))
                sock.close()
                return {'status': 'success', 'message': f'Connected to {self.ip}:{self.port}'}
            except Exception as e:
                return {'status': 'error', 'message': f'Connection failed: {str(e)}'}

        elif self.connection_type == 'usb':
            return {'status': 'info', 'message': 'USB connection not tested - try printing a label'}

        elif self.connection_type == 'file':
            return {'status': 'success', 'message': 'File export mode - no connection needed'}

        else:
            return {'status': 'error', 'message': 'Unknown connection type'}


def create_printer(config: dict) -> ZebraPrinter:
    """
    Factory function to create printer instance from config

    Args:
        config: Dictionary with connection settings
            Example:
            {
                'type': 'network',
                'ip': '192.168.1.100',
                'port': 9100
            }
    """
    return ZebraPrinter(
        connection_type=config.get('type', 'file'),
        ip=config.get('ip'),
        port=config.get('port', 9100),
        printer_name=config.get('printer_name', 'Zebra_GK420d')
    )

#!/usr/bin/env python3
"""
view_vmware_licenses.py

List all VMware licenses (vCenter or standalone ESXi) using pyVmomi SDK.

Usage:
  python3 view_vmware_licenses.py

Requirements:
  pip install pyvmomi
"""

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import atexit
import argparse

def connect_vsphere(host, user, password, port=443, disable_ssl=True):
    """Connect to vCenter or ESXi and return service instance."""
    context = None
    if disable_ssl:
        context = ssl._create_unverified_context()
    try:
        si = SmartConnect(host=host, user=user, pwd=password, port=port, sslContext=context)
        atexit.register(Disconnect, si)
        return si
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return None

def list_licenses(si):
    """Retrieve license information."""
    try:
        license_manager = si.content.licenseManager
    except Exception:
        print("[-] Unable to access licenseManager.")
        return

    print("\n=== VMware License Information ===")
    try:
        licenses = license_manager.licenses
        for lic in licenses:
            print(f"License Key      : {lic.licenseKey}")
            print(f"  Name           : {lic.name}")
            print(f"  Edition        : {lic.editionKey}")
            print(f"  Total Capacity : {lic.total}")
            print(f"  Used Capacity  : {lic.used}")
            print(f"  Expiration     : {getattr(lic, 'expirationDate', 'N/A')}")
            print("-" * 45)
    except Exception as e:
        print(f"[-] Error fetching licenses: {e}")

def main():
    parser = argparse.ArgumentParser(description="View VMware Licenses (vCenter or ESXi)")
    parser.add_argument("--host", required=True, help="vCenter or ESXi hostname / IP")
    parser.add_argument("--user", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--port", type=int, default=443, help="Port number (default 443)")
    args = parser.parse_args()

    si = connect_vsphere(args.host, args.user, args.password, args.port)
    if not si:
        return

    about_info = si.content.about
    print(f"[+] Connected to: {about_info.fullName} ({about_info.apiType})")
    print(f"[i] Version: {about_info.version}, Build: {about_info.build}")

    list_licenses(si)

if __name__ == "__main__":
    main()

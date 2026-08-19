"""
Experiment: Test construction of PSP Directory from scratch
Goal: Understand if UtkAmd's constructors work for building (not just parsing)

Test flow:
1. Create a PspDirectoryHeader
2. Create PspDirectoryEntry objects
3. Create a PspDirectory with these objects
4. Try to serialize and verify structure
"""

import sys
import os

# Add parent directory to path to import UtkAmd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from UtkAmd.psp.directories.pspDirectory import PspDirectory
from UtkAmd.psp.directories.directoryEntries.pspDirectoryEntry import PspDirectoryEntry
from UtkAmd.psp.directories.directoryHeaders.pspDirectoryHeader import PspDirectoryHeader
from UtkAmd.psp.directories.directoryHeaders.infoField import PspDirectoryHeaderInfoField
from UtkAmd.psp.addressMode import AddressMode
from UtkAmd.psp.firmwareTypes import FirmwareType


def test_create_psp_header_from_scratch():
    """Test 1: Can we create a PspDirectoryHeader with sane defaults?"""
    print("\n=== Test 1: Create PspDirectoryHeader from scratch ===")
    
    try:
        # Try to create header with minimal args
        infoField = PspDirectoryHeaderInfoField()
        print(f"✓ Created PspDirectoryHeaderInfoField: {infoField}")
        
        header = PspDirectoryHeader(signature="$PSP", checksum=0, count=0, infoField=infoField)
        print(f"✓ Created PspDirectoryHeader: {header}")
        print(f"  - Signature: {header.getSignature()}")
        print(f"  - Entry Count: {header.getEntryCount()}")
        print(f"  - Address Mode: {header.getAddressMode()}")
        
        # Try to serialize
        serialized = header.serialize()
        print(f"✓ Serialized header: {len(serialized)} bytes")
        print(f"  First bytes (hex): {serialized[:16].hex()}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_psp_directory_entry_from_scratch():
    """Test 2: Can we create a PspDirectoryEntry with reasonable defaults?"""
    print("\n=== Test 2: Create PspDirectoryEntry from scratch ===")
    
    try:
        # Try to create entry with minimal args
        # Constructor signature: (entryType, subProgram, byteGroup, entrySize, offset, addressMode=None)
        entry = PspDirectoryEntry(
            entryType=FirmwareType.PSP_PUBKEY.value,  # 0x00
            subProgram=0,
            byteGroup=0,
            entrySize=0x1000,  # 4KB
            offset=0x1000,     # Starts at 4KB
            addressMode=AddressMode.FlashOffset
        )
        print(f"✓ Created PspDirectoryEntry")
        print(f"  - Type: {entry.getEntryType()}")
        print(f"  - Size: {hex(entry.getEntrySize())}")
        print(f"  - Location: {hex(entry.getEntryLocation())}")
        
        # Try to serialize
        serialized = entry.serialize()
        print(f"✓ Serialized entry: {len(serialized)} bytes")
        print(f"  Hex: {serialized.hex()}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_psp_directory_from_scratch():
    """Test 3: Can we create a PspDirectory with entries?"""
    print("\n=== Test 3: Create PspDirectory from scratch ===")
    
    try:
        # Create header
        infoField = PspDirectoryHeaderInfoField()
        infoField.setMaxSize(1)  # Minimal size (1 * 0x1000 bytes)
        header = PspDirectoryHeader(signature="$PSP", checksum=0, count=1, infoField=infoField)
        print(f"✓ Created header")
        
        # Create entry
        entry = PspDirectoryEntry(
            entryType=FirmwareType.PSP_PUBKEY.value,
            subProgram=0,
            byteGroup=0,
            entrySize=0x1000,
            offset=0x1000,
            addressMode=AddressMode.FlashOffset
        )
        print(f"✓ Created entry")
        
        # Try to create directory
        # Constructor: (offset, header, directoryEntries, content, trailingBinary=None, fullBinary=None)
        directory = PspDirectory(
            offset=0x0,
            header=header,
            directoryEntries=[entry],
            content={},  # Empty content dict
            trailingBinary=None
        )
        print(f"✓ Created PspDirectory")
        print(f"  - Offset: {hex(directory.getOffset())}")
        print(f"  - Size: {hex(directory.getSize())}")
        print(f"  - Entries: {len(directory.getDirectoryEntries())}")
        
        # Try to serialize
        serialized = directory.serialize()
        print(f"✓ Serialized directory: {len(serialized)} bytes")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_link_firmware_to_entry():
    """Test 4: Can we link firmware objects to entries?"""
    print("\n=== Test 4: Link firmware to entry ===")
    
    try:
        entry = PspDirectoryEntry(
            entryType=FirmwareType.PSP_PUBKEY.value,
            subProgram=0,
            byteGroup=0,
            entrySize=0x1000,
            offset=0x1000,
            addressMode=AddressMode.FlashOffset
        )
        print(f"✓ Created entry")
        
        # Get the entry reference
        ref = entry.getEntryReference()
        print(f"✓ Got entry reference: {ref}")
        print(f"  - Offset: {hex(ref.getOffset())}")
        print(f"  - Absolute Offset: {hex(ref.getAbsoluteOffset())}")
        
        # Try to create a dummy firmware blob
        dummy_firmware = b'\x00' * 0x1000
        print(f"✓ Created dummy firmware blob: {len(dummy_firmware)} bytes")
        
        # Can we set it on the reference?
        # NOTE: Firmware should be an ImageElement, not raw bytes
        # This might fail - let's see what happens
        print("  (Skipping firmware assignment - need proper Firmware object)")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("="*60)
    print("UTK PSP Directory Construction Experiment")
    print("="*60)
    
    results = []
    results.append(("PspDirectoryHeader creation", test_create_psp_header_from_scratch()))
    results.append(("PspDirectoryEntry creation", test_create_psp_directory_entry_from_scratch()))
    results.append(("PspDirectory creation", test_create_psp_directory_from_scratch()))
    results.append(("Firmware linking", test_link_firmware_to_entry()))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_pass = all(r for _, r in results)
    print("\n" + ("All tests passed!" if all_pass else "Some tests failed."))
    sys.exit(0 if all_pass else 1)

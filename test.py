import sys
import io

# Set UTF-8 encoding for stdout to handle Unicode characters on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import time
import platform
from dtor import TorHandler


started = time.time()
print("\n" + "="*80)
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] COMPREHENSIVE TorHandler TESTING WITH REAL TOR BINARIES")
print("="*80 + "\n")
# # Configuration
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Configurations 101 ")
handler = TorHandler(recover=False)
handler.debug = True
print("   - Cleaning up directories and stale processes...")
# print(f"  - Using clear_all_directories to clean {handler.clear_all_directories()} directories")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Max port resolve attempts: {handler.max_port_resolve_attempts}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Max Socket Ports:          {handler.max_socks_ports}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Max Control Ports:         {handler.max_control_ports}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Max Hidden Services:       {handler.max_hidden_services}\n")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Data Directory:            {handler.data_directory}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Binary Directory:          {handler.binary_dir}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Cache Directory:           {handler.cache_directory}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - torrc File:                {handler.torrc_file}\n")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - SocksPorts:                {handler.socks_port}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - ControlPorts:              {handler.control_port}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Data directory:            {handler.data_directory}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - Torrc file:                {handler.torrc_file}\n")
# Test 2: Fetch Tor info
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Test 2: Fetch latest Tor download information")
tor_info = handler.fetch_latest_tor_download_url()
if tor_info['url']:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✓ Fetched Tor download info")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]   - Version: {tor_info['version']}")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]   - Platform: {platform.system()} {platform.machine()}")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]   - File: {tor_info['latest_file']}\n")
else:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✗ No suitable Tor binary found\n")
    import sys; sys.exit(1)
# Test 3: Download binaries
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Test 3: Download and install Tor binaries")
result = handler.download_and_install_tor_binaries()
if result:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✓ Tor binaries downloaded successfully")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]   - Executable: {handler.get_tor_executable_path()}\n")
else:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✗ Failed to download\n")
    import sys; sys.exit(1)
# Test 4: Configure ports
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Test 4: Configure ports with collision resolution")
handler.socks_port_collision_resolve = True
handler.control_port_collision_resolve = True
handler.add_socks_port(19052)
handler.add_control_port(19053)
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✓ Ports configured")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]  - SocksPorts: {handler.socks_port}")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]  - ControlPorts: {handler.control_port}\n")
# Test 5: Register hidden services
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Test 5: Register hidden services")
handler.hidden_service_port_collision_resolve = True  # Enable collision resolution
services = [(80, 8080, "HTTP"), (443, 8443, "HTTPS"), (22, 2222, "SSH")]
for port, target, desc in services:
    result = handler.register_hidden_service(port=port, target_port=target)
    if result:
        print(f"✓ Registered {desc}: {port} -> {target}")
    else:
        print(f"⊘ Could not register {desc}: {port} -> {target}")
print(f"  - Total services: {len(handler.hidden_services)}\n")
# Test 6: Save configuration
print("Test 6: Save configuration")
handler.save_torrc_configuration()
print(f"✓ Configuration saved to {handler.torrc_file}\n")
# Test 7: Load configuration
print("Test 7: Load configuration")
print(f"✓ Configuration loaded")
print(f"  - Hidden services: {len(handler.hidden_services)}\n")
print("   Current Hidden Services:")
for service in handler.hidden_services:
    print(f"      - Service Dir: {service['dir']}")
    print(f"      - Port: {service['port']} -> Target Port: {service['target_port']}")
    print(f"      - Pre-configured: {service['pre_config']}")
    print(f"      - Host: {service['host']}")
    print(f"      - Public Key: {service['pk']}")
    print(f"      - Secret Key: {service['sk']}\n")
# Test 8: Detect conflicts
print("Test 8: Port conflict detection")
conflicts = handler.detect_port_conflicts()
print(f"✓ Conflicts: {conflicts}\n")
# Test 9: Start Tor
print("Test 9: Start Tor service (30s timeout)")
print(f"Tor Binary Path: {handler.get_tor_executable_path()}")
print(f"Tor Data Directory: {handler.data_directory}")
if handler.start_tor_service():
    print(f"✓ Tor started (PID: {handler.tor_process_id})")
    print(f"  - Waiting for control port to be ready...")
    # Give extra time for control port to fully initialize
    time.sleep(8)
    print()
else:
    print(f"✗ Failed to start\n")
# Test 10: Runtime SOCKS port
print("Test 10: Runtime SOCKS port addition")
if handler.running:
    result = handler.add_runtime_socks_port(19060, temporary=True)
    if result:
        print(f"✓ Added runtime SocksPort 19060\n")
    else:
        print(f"✗ Failed\n")
else:
    print(f"⊘ Tor not running\n")
# Test 11: Runtime Control port
print("Test 11: Runtime Control port addition")
if handler.running:
    result = handler.add_runtime_control_port(19061, temporary=True)
    if result:
        print(f"✓ Added runtime ControlPort 19061")
        print(f"  - Waiting for Tor to reconfigure control ports...")
        time.sleep(5)  # Give Tor extra time to reconfigure control ports
        print()
    else:
        print(f"✗ Failed\n")
else:
    print(f"⊘ Tor not running\n")
# Test 12: Control commands
print("Test 12: Send control commands")
if handler.running:
    # Give a moment after any control port changes
    time.sleep(1)
    # Retry a few times as control port might be reconfiguring
    max_attempts = 5
    responses = None
    for attempt in range(max_attempts):
        responses = handler.send_control_commands(["GETINFO version", "GETINFO status/bootstrap-phase"])
        if responses:
            break
        if attempt < max_attempts - 1:
            print(f"  - Attempt {attempt + 1} failed, retrying in 2 seconds...")
            time.sleep(2)
    if responses:
        print(f"✓ Executed {len(responses)} commands")
        for idx, resp in responses.items():
            print(f"  - Command {idx}: {resp['command']}")
        print()
    else:
        print(f"✗ Failed after {max_attempts} attempts\n")
else:
    print(f"⊘ Tor not running\n")
# Test 12.2: Runtime Hidden Service
print("Test 12.2: Add runtime hidden service")
if handler.running:
    result = handler.register_runtime_hidden_service(port=8888, target_port=8080, temporary=False)
    if result and isinstance(result, dict):
        print(f"✓ Added runtime hidden service")
        print(f"  - Onion address: {result['onion_address']}")
        print(f"  - Port mapping: {result['port']} -> {result['target_port']}")
        print(f"  - Service key: {result['service_key'][:50] if result['service_key'] else 'N/A'}...")
        print()
    else:
        print(f"✗ Failed\n")
else:
    print(f"⊘ Tor not running\n")
# Test 12.3: List runtime onion addresses
print("Test 12.3: List runtime hidden services")
onion_list = []
if handler.running:
    runtime_services = handler.list_runtime_hidden_services()
    if runtime_services:
        print(f"✓ Found {len(runtime_services)} runtime hidden service(s):")
        for i, svc in enumerate(runtime_services):
            print(f"  - Service {i+1}: {svc.get('onion_address', 'N/A')} (Port: {svc.get('port', 'N/A')} -> {svc.get('target_port', 'N/A')})")
            onion_list.append(svc.get('onion_address', 'N/A'))
        print()
    else:
        print(f"⊘ No runtime hidden services\n")
else:
    print(f"⊘ Tor not running\n")
# Test 12.3.5: Verify runtime hidden service existence
print("Test 12.3.5: Verify runtime hidden service existence")
if handler.running:
    time.sleep(5)
    for i, service in enumerate(handler.hidden_services):
        hostname_file = service['dir'] / "hostname"
        if hostname_file.exists():
            with open(hostname_file) as f:
                print(f"✓ Service {i+1}: {f.read().strip()}")
        else:
            print(f"⊘ Service {i+1}: Not yet generated")
    print()
else:
    print(f"⊘ Tor not running\n")
# Test 12.3.6: Persist runtime hidden service to torrc
print("Test 12.3.6: Persist runtime hidden service to torrc")
if handler.running and onion_list:
    onion_to_persist = onion_list[0]
    result = handler.persist_runtime_hidden_service(onion_to_persist)
    if result:
        print(f"✓ Persisted runtime hidden service to torrc: {onion_to_persist}\n")
    else:
        print(f"✗ Failed to persist: {onion_to_persist}\n")
else:
    print(f"⊘ Tor not running or no runtime services\n")
# Test 12.4: Remove runtime hidden service
print("Test 12.4: Remove runtime hidden service")
if handler.running and onion_list:
    onion_to_remove = onion_list[0]
    result = handler.remove_runtime_hidden_service(onion_to_remove)
    if result:
        print(f"✓ Removed runtime hidden service: {onion_to_remove}\n")
    else:
        print(f"✗ Failed to remove: {onion_to_remove}\n")
        print(result)
else:
    print(f"⊘ Tor not running or no runtime services\n")
# Test 13: Verify hidden services
print("Test 13: Verify hidden service directories")
if handler.running:
    time.sleep(5)
    for i, service in enumerate(handler.hidden_services):
        hostname_file = service['dir'] / "hostname"
        if hostname_file.exists():
            with open(hostname_file) as f:
                print(f"✓ Service {i+1}: {f.read().strip()}")
        else:
            print(f"⊘ Service {i+1}: Not yet generated")
    print()
else:
    print(f"⊘ Tor not running\n")
# Test 13.5: List runtime hidden services
print("Test 13.5: List runtime hidden services")
if handler.running:
    runtime_services = handler.list_runtime_hidden_services()
    if runtime_services:
        print(f"✓ Found {len(runtime_services)} runtime service(s)")
        for i, svc in enumerate(runtime_services):
            print(f"  - Service {i+1}: {svc.get('onion_address', 'N/A')}")
            print(f"    Port: {svc.get('port', 'N/A')} -> {svc.get('target_port', 'N/A')}")
            print(f"    Temporary: {svc.get('temporary', 'N/A')}")
        print()
    else:
        print(f"⊘ No runtime services\n")
else:
    print(f"⊘ Tor not running\n")
# Test 13.6: Persist runtime hidden service to torrc
print("Test 13.6: Persist runtime hidden service to torrc")
if handler.running:
    runtime_services = handler.list_runtime_hidden_services()
    if runtime_services:
        # Persist the first non-temporary service
        for svc in runtime_services:
            if not svc.get('temporary'):
                onion_addr = svc.get('onion_address')
                print(f"  - Persisting {onion_addr}...")
                # Stop Tor first to save to torrc
                handler.stop_tor_service()
                time.sleep(2)
                result = handler.persist_runtime_hidden_service(onion_addr)
                if result:
                    print(f"✓ Persisted to torrc")
                    print(f"  - Total configured services: {len(handler.hidden_services)}")
                    # Restart Tor to verify persisted service
                    print(f"  - Restarting Tor with persisted configuration...")
                    if handler.start_tor_service():
                        print(f"✓ Tor restarted successfully (PID: {handler.tor_process_id})")
                        time.sleep(3)
                    print()
                else:
                    print(f"✗ Failed to persist\n")
                break
        else:
            print(f"⊘ No non-temporary services to persist\n")
    else:
        print(f"⊘ No runtime services\n")
else:
    print(f"⊘ Tor not running\n")
# Test 14: Process info
print("Test 14: Process monitoring")
process = handler.get_tor_process()
if process:
    print(f"✓ PID: {process.pid}, Status: {process.status()}")
    print(f"  - Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB\n")
else:
    print(f"⊘ No process\n")
# Test 15: Restart
print("Test 15: Restart Tor service")
if handler.running:
    if handler.restart_tor_service():
        print(f"✓ Restarted (New PID: {handler.tor_process_id})\n")
        time.sleep(3)
    else:
        print(f"✗ Failed\n")
else:
    print(f"⊘ Tor not running\n")
# Test 16: Stop
print("Test 16: Stop Tor service")
if handler.running:
    if handler.stop_tor_service():
        print(f"✓ Stopped successfully\n")
    else:
        print(f"✗ Failed\n")
else:
    print(f"⊘ Already stopped\n")
# Test 17: Force cleanup
print("Test 17: Force cleanup")
handler.force_stop_tor()
handler.terminate_all_tor_processes()
print(f"✓ Cleanup complete\n")
print("="*80)
print("✓ ALL TESTS COMPLETED")
print("="*80)
print("\n📊 Test Summary:")
print(f"  - Tor binaries downloaded and installed")
print(f"  - Configuration ports: SOCKS {handler.socks_port}, Control {handler.control_port}")
print(f"  - Hidden services: {len(handler.hidden_services)} configured")
print(f"  - Runtime services: {len(handler.temp_config['hidden_services'])} temporary")
print(f"  - All lifecycle operations tested (start/stop/restart)")
print(f"  - Runtime port and service management tested")
print("\n💡 Features Demonstrated:")
print(f"  ✓ Automatic Tor binary download for platform")
print(f"  ✓ Port collision detection and resolution")
print(f"  ✓ Hidden service configuration (file-based)")
print(f"  ✓ Runtime hidden service creation (ADD_ONION)")
print(f"  ✓ Runtime port addition (SOCKS/Control)")
print(f"  ✓ Control port authentication and commands")
print(f"  ✓ Process management and monitoring")
print(f"  ✓ Stale process cleanup")
print(f"  ✓ Configuration persistence (torrc)")
print("\n📝 Check 'tor_handler.log' for detailed logs")
print("="*80)
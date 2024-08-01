 #Wake on lan feature
import wakeonlan

 #Replace with the MAC address of the target PC (format: XX:XX:XX:XX:XX:XX)
 #Send the magic packet

 wakeonlan.send_magic_packet('A4:BB:6D:82:4C:38')

 print(f"Wake-on-LAN magic packet sent to ip")

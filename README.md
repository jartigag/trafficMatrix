# trafficMatrix.py

returns a traffic matrix from a .pcap.

to use this script, install [tshark](https://www.wireshark.org/docs/man-pages/tshark.html) before with  
```
sudo apt install tshark
```
(if you haven't done it before).

after executing `python3 trafficMatrix.py your_capture_file.pcap.gz`, you'll get  
* <samp>ips.txt</samp> with all the IPv4 addresses of the .pcap
* <samp>matrix.txt</samp> with the resulting traffic matrix (no header row/column)

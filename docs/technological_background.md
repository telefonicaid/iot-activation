## Technological background

### Mobile IoT Technologies
Since the beginning of cellular communications, not only people have been connected using mobile phones, also machines have been connected to each other, 
what we call M2M, Machine-To-Machine communications. Currently, the term M2M has been replaced by IoT, 
to make clear the evolution that will have this type of technologies in the coming years, miniaturization of connected devices, 
massive increase in the number of connected equipment, increased coverage will be what will lead to the M2M a step further to the IoT. 

Typically the cheapest and simplest solution has been to use second generation 2G mobile technologies (GSM, GPRS, EDGE),
but when the throughput requirements were higher and the cost requirements were less demanding, 3G and 4G technologies were used too.


It is necessary to include cellular technologies in the use cases:
- Utilities: gas and water metering,
- Medical assisted living, remote monitoring
- Agriculture: Stationary tracking, environmental monitoring
- Industrial: machinery control, safety monitoring
- Consumer: wearables, pet tracking.
- Smart City: parking sensors, waste management

These use cases have specific requirements that force the emergence of new cellular technologies focused on the IoT:
- Wide area coverage: Covered by all mobile technologies.
- No access to the mains power: The devices will be battery powered in most cases.
- Low cost: The number of devices and applications will require a cost per device inside the current one.
- Strong propagation: Go one step further in coverage to enable IoT access to basements, rural environments, etc.

These four requirements are not met by current mobile technologies, 
which forced 3GPP to define two new standards based on the existing 4G infrastructure: NBIoT and LTE-M

Now launched commercially, the Mobile Internet of Things (Mobile IoT) is expanding rapidly with over 40 Commercial networks available globally, 
a combination of LTE-M and NB-IoT. Operating in licensed spectrum, low power wide area networks can provide low cost, yet secure, 
connectivity to battery-powered devices in both rural and urban locations. Following successful pilots involving a wide variety of use cases, 
Mobile IoT connectivity has now been deployed across Europe, North America and East Asia. 

### LPWAN: LTE-M vs NBIoT

![pick](pictures/miscellaneous/ltem_LPWA.png)

LTE-M extends LTE with features for improved support for Machine-Type Communications (MTC) and IoT.
The objective of LTE-M was to bring down the LTE device cost substantially to make LTE attractive for low end MTC applications that have so far been
adequately handled by GPRS. The cost reduction techniques were: reduced peak rate (1Mbps), single receive antenna, half duplex operation,
reduced bandwidth (1,4Mhz) and TX power (20dBm). 

NBIoT is designed for ultra-low-cost massive Machine-Type Communications, aiming to support a massive number of devices in a cell.
Low device complexity is one of the main design objectives, enabling module cost. Furthermore, it is designed to offer substantial coverage
improvements over GPRS as well as for enabling long battery lifetime. NBIoT has been designed to give maximal deployment flexibility.


|| LTE-M | NBIOT |
|:------ | ----- | ----- |
| BANDWIDTH | 1,4MHz | 200kHz |
| DL PEAK RATE | 300kbps HD | 50kbps |
|   | 1Mbps FD |  |
| UP PEAK RATE | 375kbps HD | 20kbps single tone |
|   | 1Mbps FD | 50 kbps multi tone |
| DUPLEX | HD (type B) or FD | HD (type B) or FD |
| LATENCY | 10-15ms | 1,4-10s |
| ANTENNAE | 1 | 1 |
| TRANSMIT POWER | 20dBm | 23dBm |
| MOBILITY  | Handover | Cell-Resellection |
| VOICE | Yes | No |


NBIoT is recommended when devices are massive and static. But when dealing with moving devices it is recommended to use a multi-technology 
NBIoT/LTE-M solution to avoid coverage issues and to guarantee the services.
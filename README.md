# PyGPSClient

PyGPSClient is a free, open source graphical GPS testing and diagnostic client application written entirely in Python and tkinter.

![fullmap](/images/fullmapquest.png)

The application runs on any platform which supports a Python3 interpreter (>=3.6) and tkinter (>=8.6) GUI framework, 
including Windows, MacOS, Linux and Raspberry Pi OS. It displays location and diagnostic data from any NMEA or UBX (u-blox &copy;) 
compatible GPS device over a standard serial (UART) or USB port.

Originally designed as a platform-agnostic evaluation, development and educational tool for the [u-blox NEO-6M series](https://www.u-blox.com/en/product/neo-6-series) GPS modules, and in particular the [Makerhawk Hobbyist GPS Board](https://www.amazon.co.uk/MakerHawk-Microcontroller-Compatible-Navigation-Positioning/dp/B0783H7BLW), it has evolved
into a more general purpose multi-platform NMEA / UBX GPS client.

## Features:

1. Supports both NMEA and UBX protocols. It uses the existing pynmea2 library for NMEA parsing and 
implements a **new pyubx2 library** for UBX parsing. 
1. Configurable GUI with selectable and resizeable widgets.
1. Serial console widget showing either raw or parsed data stream.
1. Skyview widget showing current satellite visibility and position (elevation / azimuth).
1. Graphview widget showing current satellite reception (signal-to-noise ratio).
1. Mapview widget with location marker, showing either a static Mercator world map, or an optional dynamic web-based map downloaded via a MapQuest API (requires an Internet connection and free 
[MapQuest API Key](https://developer.mapquest.com/plan_purchase/steps/business_edition/business_edition_free/register)).
1. **WORK IN PROGRESS** The ability to configure certain key parameters on u-blox GPS devices via the proprietary UBX protocol, including serial port protocols, dynamic navigation mode and standard/proprietary NMEA message filters.

![fullubx](/images/fullubx.png)
![banneronly](/images/banneronly.png)
![basicview](/images/basicview.png)
![ubxconfig](/images/ubxconfig.png)

Future versions may include additional features like GPX track recording, though the application is *not* intended to be used for real-time navigation or route planning.

This is a personal project and I have no affiliation whatsoever with u-blox &copy;, Makerhawk &copy; or MapQuest &copy;.

### Current Status

![Release](https://img.shields.io/github/v/release/semuconsulting/PyGPSClient?include_prereleases)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/PyGPSClient)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/PyGPSClient)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/PyGPSClient.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/PyGPSClient)

Pre-Alpha. Main application and widgets are fully functional. NMEA implementation is solid. UBX implementation is partial at present (incoming UBX data is streamed to the console widget but not yet to the other widgets) but in hand, along with improvements to exception handling and threading performance. The UBX config dialog is under development and additional configuration functionality will be added in due course.

Constructive feedback welcome.

## Installation

First, check the [dependencies](#dependencies) listed below.

To install and run, download and unzip this repository and run:

`python /path_to_folder/foldername` (or `python3...`, depending on your environment)

e.g. if you downloaded and unzipped to a folder named `PyGPSClient`, run: 

`python /path_to_folder/PyGPSClient`.

**NB:** to access the serial port on most linux platforms, you will need to be a member of the 
tty and dialout groups.


## <a name="dependencies">Dependencies</a>

**MapQuest API Key**

To use the optional dynamic web-based mapview facility, you need to request and install a 
[MapQuest API key](https://developer.mapquest.com/plan_purchase/steps/business_edition/business_edition_free/register).
The free edition of this API allows for up to 15,000 transactions/month (roughly 500/day) on a non-commercial basis.
For this reason, the map refresh rate is intentionally limited to 1/minute to avoid exceeding the free transaction
limit under normal use. **NB:** this application is *not* intended to be used for real time navigational purposes.

Once you have received the API key (a 32-character alphanumeric string), copy it to a file named `apikey` (lower case, 
no extension) and place this file in the application's root directory.

**Python Libraries**

See [requirements.txt](requirements.txt).

The application implements a **new python library pyubx2** for UBX protocol handling.

The following additional standard libraries are required, and can be installed using pip, e.g.:

`python -m pip install pyubx2 pyserial pynmea2 Pillow requests`

On Windows and MacOS, pip, tkinter and the necessary imaging libraries are generally packaged with Python. 
On some Linux distributions like Ubuntu 18+, they may need to be installed separately, e.g.:

`sudo apt-get install python3-pip python3-tk python3-pil python3-pil.imagetk`

## License

![License](https://img.shields.io/github/license/semuconsulting/PyGPSClient.svg)

BSD 3-Clause License ("BSD License 2.0", "Revised BSD License", "New BSD License", or "Modified BSD License")

Copyright (c) 2020, SEMU Consulting
All rights reserved.

Application icons from [iconmonstr](https://iconmonstr.com/) &copy;.

## Author Information

semuadmin@semuconsulting.com

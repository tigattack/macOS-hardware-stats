# Known SMC keys

Below is a list of SMC keys I've managed to discover from the source code of various projects and some tinkering.

Some work and some don't. Tested on a 2019 15" MacBook Pro.

They can be queried with `smc -k <key> -r`.

## Keys

* F0Ac: 'Fan 0 RPM'
* F0Mn: 'Fan 0 Min RPM'
* F0Mx: 'Fan 0 Max RPM'
* F0Sf: 'Fan 0 safe speed'
* F0Tg: 'Fan 0 target speed'
* F1Ac: 'Fan 1 RPM'
* F1Mn: 'Fan 1 Min RPM'
* F1Mx: 'Fan 1 Max RPM'
* F1Sf: 'Fan 1 safe speed'
* F1Tg: 'Fan 1 target speed'
* FS!: 'See if fans are in automatic or forced mode'
* TA0P: 'Ambient temperature'
* TA0p: 'Ambient temperature'
* TA1P: 'Ambient temperature'
* TA1p: 'Ambient temperature'
* TA0S: 'PCI Slot 1 Pos 1'
* TA1S: 'PCI Slot 1 Pos 2'
* TA2S: 'PCI Slot 2 Pos 1'
* TA3S: 'PCI Slot 2 Pos 2'
* Tb0P: 'BLC Proximity'
* TB0T: 'Battery TS_MAX'
* TB1T: 'Battery 1'
* TB2T: 'Battery 2'
* TB3T: 'Battery 3'
* TC0C: 'CPU 0 Core'
* TC0D: 'CPU 0 Die'
* TCXC: 'PECI CPU'
* TCXc: 'PECI CPU'
* TC0E: 'CPU 0 ??'
* TC0F: 'CPU 0 ??'
* TC0G: 'CPU 0 ??'
* TC0H: 'CPU 0 Heatsink'
* TC0J: 'CPU 0 ??'
* TC0P: 'CPU 0 Proximity'
* TC1C: 'Core 1'
* TC2C: 'Core 2'
* TC3C: 'Core 3'
* TC4C: 'Core 4'
* TC5C: 'Core 5'
* TC6C: 'Core 6'
* TC7C: 'Core 7'
* TC8C: 'Core 8'
* TCGC: 'PECI GPU'
* TCGc: 'PECI GPU'
* TCSC: 'PECI SA'
* TCSc: 'PECI SA'
* TCSA: 'PECI SA'
* TG0H: 'GPU 0 Heatsink'
* TG0P: 'GPU 0 Proximity'
* TG0D: 'GPU 0 Die'
* TG1D: 'GPU 1 Die'
* TG1H: 'GPU 1 Heatsink'
* TH0P: 'Harddisk 0 Proximity'
* Th1H: 'NB/CPU/GPU HeatPipe 1 Proximity'
* TL0P: 'LCD Proximity'
* TM0P: 'Memory Slot Proximity'
* TM0S: 'Memory Slot 1'
* Tm0p: 'Misc (clock chip) Proximity'
* TO0P: 'Optical Drive Proximity'
* Tp0P: 'PowerSupply Proximity'
* TPCD: 'Platform Controller Hub Die'
* TS0C: 'Expansion slots'
* Ts0P: 'Palm rest L'
* Ts0S: 'Memory Bank Proximity'
* Ts1p: 'Palm rest R'
* TW0P: 'AirPort Proximity'

* TA0P: 'AMBIENT_AIR_0'
* TA1P: 'AMBIENT_AIR_1'
* TC0F: 'CPU_0_DIE'
* TC0D: 'CPU_0_DIODE'
* TC0H: 'CPU_0_HEATSINK'
* TC0P: 'CPU_0_PROXIMITY'
* TB0T: 'ENCLOSURE_BASE_0'
* TB1T: 'ENCLOSURE_BASE_1'
* TB2T: 'ENCLOSURE_BASE_2'
* TB3T: 'ENCLOSURE_BASE_3'
* TG0D: 'GPU_0_DIODE'
* TG0H: 'GPU_0_HEATSINK'
* TG0P: 'GPU_0_PROXIMITY'
* TH0P: 'HDD_PROXIMITY'
* Th0H: 'HEATSINK_0'
* Th1H: 'HEATSINK_1'
* Th2H: 'HEATSINK_2'
* TL0P: 'LCD_PROXIMITY'
* TM0S: 'MEM_SLOT_0'
* TM0P: 'MEM_SLOTS_PROXIMITY'
* Tm0P: 'MISC_PROXIMITY'
* TN0H: 'NORTHBRIDGE'
* TN0D: 'NORTHBRIDGE_DIODE'
* TN0P: 'NORTHBRIDGE_PROXIMITY'
* TO0P: 'ODD_PROXIMITY'
* Ts0P: 'PALM_REST'
* Tp0P: 'PWR_SUPPLY_PROXIMITY'
* TI0P: 'THUNDERBOLT_0'
* TI1P: 'THUNDERBOLT_1'
* ALV0: 'Light sensor left'
* ALV1: 'Light sensor right'
* M0_X: 'Motion sensor X'
* M0_Y: 'Motion sensor Y'
* M0_Z: 'Motion sensor Z'

## Sources

[https://github.com/mmarcon/node-smc/blob/master/index.js](https://github.com/mmarcon/node-smc/blob/master/index.js)
[https://github.com/hholtmann/smcFanControl/tree/master/smc-command](https://github.com/hholtmann/smcFanControl/tree/master/smc-command)

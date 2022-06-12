Midi monitor based on [Samplerbox by hansehv](https://github.com/hansehv/SamplerBox)

Extended with an API to monitor note sequences and trigger actions based on them.
Devices will be implemented over time :)

### Coffee Machine ###
| Action          | Relay Channel | ESP 32 Pin | Raspi Button PIN |
|-----------------|---------------|------------|------------------|
| Power           | 1             | 18         | 17               |
| Espresso        | 2             | 19         | 27               |
| Double Espresso | 3             | 21         | 22               |
| Clean           | 4             | 22         | 5                |
| Double Coffee   | 5             | 23         | 6                |
| Coffee          | 6             | 25         | 13               |
| Steam           | 7             | 26         | 12               |
| Unused          | 8             | -          | -                |

### Other GPIO pins ###

Some pins are in use by Samplerbox, additionally, this project uses the following:

| Use                | GPIO Pin number |
|--------------------|-----------------|
| Lock relay channel | 20              |

License: [Creative Commons BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/)

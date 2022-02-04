
## Getting started:

1.  Rename the *creds_example.env* file to *creds.env*.

2.  Then, change the environment variables from EX_USER to USER, etc. . .
    Store your credentials in the creds.env folder.

3.  Open main.py

4.  Ensure that credentials are properly stored in USER, PASSWORD, and SECRET variables.

5.  Initialize the Site class as:

    from Mass_push import Site  

    device = Site(USER, PASSWORD, SECRET)

6.  You can now call the other functions in the class to provision devices.


### Push to multiple devices at once 

1.  Define the address of the device(s) in the format of:  x.x.x [1, 2, 3, 4] and pass the device list to the mass_push function. 

2.  Example: Site.Mass_push('192.168.1', [2, 3, 4], 'show run')
        This example would contact 192.168.1.2, 192.168.1.3, 192.168.1.4

### Debugging with basic CLI

1.  Call: `Site.enter_cli()` to enter a basic CLI mode.




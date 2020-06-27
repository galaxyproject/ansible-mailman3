Role Name
=========

Install Mailman version 3, including either/all of Core, Postorius, Hyperkitty.

Mailman 3 is not trivial to set up.

Requirements
------------

The role does not include configuration of the MTA (exim, postfix, etc) which must be done
to get email in and out of Mailman Core. Mailman 3 (normally) uses LMTP to send/receive
mail, and canned condfigurations are available in many places.


Role Variables
--------------

Refer to default/main.yml for the role variables, which are somewhat documented there.

Some suggestions:

 - Unless you are using a multi-server postfix setup, you don't need to consider map directories.

 - To start with, you may wish to set mailman3\_uwsgi\_static true, so the python webserver
   provides these files, and consider configuring nginx, etc, to do that later

 - The main configuration is done by merging the default config dictionary with a custom
   (playbook-provided) one -- and some default items can be set individually as well, so there
   are two ways to define some items. In your playbook, most config can be set in "mailman3\_config":
   or "mailman3\_django":, which will be merged to make "\_\_mailman3\_config\_merged". In
   config.yml some debug actions are commented out, and enabling them may be helpful to understand
   what you have set.

 - You definitely need to change "mailman3\_core\_api\_admin\_pass" and "mailman3\_archiver\_key"!


Dependencies
------------

This role works well with rivimey.exim to configure the Exim MTA.

Example Playbook
----------------


License
-------

BSD

Author Information
------------------

Created by Nate Coraor @natefoo
dditional work by Ruth Ivimey-Cook @rivimey

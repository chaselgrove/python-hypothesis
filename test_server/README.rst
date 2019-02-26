.. See file COPYING distributed with python-hypothesis for copyright and 
   license.

Test server
===========

This directory contains an Ansible playbook for setting up a test
Hypothesis server.  The code and instructions follow the `dev server
installation`_ and `dev client installation`_ pages on the Hypothesis
web site.

.. _dev server installation: https://h.readthedocs.io/en/latest/developing/install/
.. _dev client installation: https://h.readthedocs.io/projects/client/en/latest/developers/developing/

The Ansible playbook was tested on a Debian 9 (Stretch) EC2 instance
on AWS.  t2.micro and t2.small are not powerful enough to run the
server.

To run the server, ssh to the EC2 instance and forward port 5000
to localhost.  Then, as root:

::

    cd /root/h
    docker-compose up -d
    make dev

Then Hypothesis can be accessed at http://localhost:5000/.

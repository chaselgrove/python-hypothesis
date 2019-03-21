.. See file COPYING distributed with python-hypothesis for copyright and 
   license.

Test server -- Ansible
======================

This directory contains an Ansible playbook for setting up a test
Hypothesis server.  The code and instructions follow the `dev server
installation`_ and `dev client installation`_ pages on the Hypothesis
web site.

.. _dev server installation: https://h.readthedocs.io/en/latest/developing/install/
.. _dev client installation: https://h.readthedocs.io/projects/client/en/latest/developers/developing/

The Ansible playbook was tested on a Debian 9 (Stretch) EC2 instance
on AWS.  t2.micro and t2.small are not powerful enough to run the
server.

Server
------

To run the server, ssh to the EC2 instance and forward port 5000
to localhost.  Then, as root:

::

    cd /root/h
    docker-compose up -d
    make dev

Then Hypothesis can be accessed at http://localhost:5000/.

Client
------

This section describes how to serve the web client from the test
server.  Some details have been omitted; see the Hypothesis development
documentation pages linked above for details.

Create a user in the running Hypothesis server and make the user
an admin.  Log in as this user and register a new OAuth client by
going to http://localhost:5000/admin/oauthclients.  Choose a name,
use http://localhost:5000/app.html for the redirect URL, and note
the client ID.

Stop the server, set CLIENT_OAUTH_ID and CLIENT_URL, and restart the server:

::

    export CLIENT_OAUTH_ID=...
    export CLIENT_URL=http://localhost:3001/hypothesis
    make dev

In another terminal, start the client; as root:

::

    cd /root/client
    export SIDEBAR_APP_URL=http://localhost:5000/app.html
    make dev

Forward ports 3000 and 3001 from the test server and the embedded
client will be available.  Test at:

::

    http://localhost:5000/docs/help

Add the following to pages to embed the client:

::

    <script async src="http://localhost:5000/embed.js"></script>

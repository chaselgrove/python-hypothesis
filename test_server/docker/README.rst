.. See file COPYING distributed with python-hypothesis for copyright and 
   license.

Test server -- Docker
=====================

This directory contains resources for running a development Hypothesis
server in a Docker container.

The Dockerfile in this directory creates a container that will pull
the current server code from GitHub and run the development server.
We require PostgreSQL, Elasticsearch, and RabbitMQ to be running in
other containers.

Build the server container using:

::

    docker build .

and note the container ID.  Then replace IMAGE-ID in docker-compose.yml
and run:

::

    docker-compose up

Alternatively, run the services and the server container separately.
Clone the Hypothesis server code at https://github.com/hypothesis/h
and run ``docker-compose up`` in that directory.  Then start the
server container with:

::

    docker run -p 5000:5000 --network h_default <image id>

About 2GB free memory is required to run the server and its services.

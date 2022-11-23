# netguru-ddd-workshop
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

DDD workshop during integration meeting with Netguru's workmates.

## Final implementation

The example implementation you can find on the [final-implementation](https://github.com/szymon6927/netguru-ddd-workshop/tree/final-implementation) branch

## Table of contents

* [About](#about)
* [Domain description](#domain-description)
* [Stack](#stack)
* [Prerequisites](#prerequisites)
* [Setup](#setup)

## About

The main purpose of this workshop is to show the basics of DDD tactical patterns against example business requirements.
This is for **educational** purposes only and the code is not **production-ready**.

The project is built on top of the Hexagonal Architecture and shows the following building blocks:
- Value Object
- Repository
- Domain Events
- Aggregate
- Entity
- Application Service

It does not cover:
- Modules
- Domain services
- Integration events
- Policies

## Domain description

Event storming session - https://miro.com/app/board/uXjVO14wBhc=/?share_link_id=664794037385


## Stack

- Python 3.9
- MongoDB
- Docker Compose

## Prerequisites

Make sure you have installed all the following prerequisites on your development machine:

- [Poetry](https://python-poetry.org/)
- [GIT](https://git-scm.com/downloads)
- [Make](http://gnuwin32.sourceforge.net/packages/make.htm)
- [Python 3.9](https://www.python.org/downloads/)
- [Docker version >= 20.10.11](https://www.docker.com/get-started)
- [docker-compose version >= 1.29.2](https://docs.docker.com/compose/install/)

## Setup

1. Install dependencies:

```bash
$ poetry install
```

2. Setup pre-commit hooks before committing:

```bash
$ poetry run pre-commit install
```

3. Run MongoDB

```bash
$ docker-compose up -d
```

### Meta
If you have any questions/problems/thoughts drop me a line

Szymon Miks – miks.szymon@gmail.com

# Arnheim

### Idea

This is a basic implementation of the Arnheim Framework, that seeks to implement a working pipeline for the processing
and analysis of microscopic data. Arnheim uses Docker-Containers to ensure most of its workflow is as modular and scalable as
possible. Its architrecture consists of
 * Bergen (the Backend, a django-driven API-Backend)
 * Oslo (the Frontend, react-based orchestrator of the modules, separate GitHub)
 * Database (either sqlite or postgres database for object persistence)
 * JupJup (the Jupyter-Server for easy Access to the Models Provided)
 
Non-Working Modules are also included in this repository for future directions: Apache Kafka, Certbot, VSCode

Arnheim uses OAuth system to provide authoriazion and authentification; users are only able to
use the application once registered on the backend, and can login from a variety of different clients (checkout foreign for a 
working implementation using PyQT)

Real-Time Communication is based on an implementation of Django-Channels that is only available for signed-in users.

### Prerequisites

As Arnheim is based on Docker it needs a working Docker instance running on your Machine
(detailed instructions found on [Docker Get Started](https://docs.docker.com/get-started/))


### Installing

Once this repository is cloned, cd into the parent directory and adjust the docker-compose.yml
according to your needs ( a good place to start is adjusting the media directories according to your file structure)
once adjusted run (with admin privileges)

```
docker-compose up
```

This should cause the initial installation of all required libraries through docker, (please be patient)

### Running

From now on you can run the project through 
```
docker-compose up
```


## Populating the Database

As there is no initial Database provided you need to setup the Database with a Superuser before starting to do so check the django tutorial on [superuser creation](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site)
Beware that Django commands like

```
python3 manage.py createsuperuser
```

translate to

```
docker-compose run web python manage.py createsuperuser
```
in the Docker context


### Testing and Documentation

So far Arnheim does not provide unit-tests and is in desperate need of documentation,
please beware that you are using an Alpha-Version


### Roadmap

- Import and Export of Samples
- Implementation of standard image processing
- Machine Learning Pipeline (Kafka)

## Deployment

Contact the Developer before you plan to deploy this App, it is NOT ready for public release

## Built With

* [Docker](http://www.dropwizard.io/1.0.2/docs/) - Architecture
* [Django](https://maven.apache.org/) - Web Server in python
* [Django-Channels](https://rometools.github.io/rome/) - Used for real-time-communictation
* [python-bioimage](https://bio-it.embl.de/image-analysis-with-python/) - Used to read vendor microscopy format

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/jhnnsrs/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

There is not yet a working versioning profile in place, consider non-stable for every release 

## Authors

* **Johannes Roos ** - *Initial work* - [jhnnsrs](https://github.com/jhnnsrs)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is yet to be licensed, consider private

## Acknowledgments

* EVERY single open-source project this library used (the list is too extensive so far)

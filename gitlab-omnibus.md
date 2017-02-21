# Building gitlab from source with custom patches

Gitlab is written in ruby and uses the rails MVC framework. It requires Ruby 2.1.8 or newer, which is not available as a package for older ubuntu.

## Required tools

1. Ruby, etc.

    # apt-get install ruby-full

2. Ruby build gems

	# gem install rake -v '10.4.2'
	# gem install ohai -v '8.7.0'

## Building the project

Done with bundle and not with make!

    $ bundle install
## Trouble shooting
when it complained about permissions (and then stopped the container)
* "docker exec -it compare-gitlab update-permissions"

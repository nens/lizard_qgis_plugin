# LizardViewer
QGIS plug-in for viewing data from Lizard in QGIS.

## Features
* Log in with Lizard account
* Show organisations of user
* View the first 100 point assets as memory layer (of assets type bridges, manholes, outlets, overflows, wastewatertreatmentplants or weirs)
* Log out

## Requirements
* QGIS 2.14
* [lizard-connector](https://github.com/lizardsystem/lizard-connector) (included)

## Installation
The plug-in can be added using one of the following ways:
* Use the Lizard QGIS repository
  * via the QGIS menu bar go to Plugins > Manage And Install Plugins... > Settings
  * add `https://plugins.lizard.net/plugins.xml` and reload
  * install the plugin by selecting LizardViewer
* Copy or symlink the repo directory to your plugin directory
  * on *Linux*: `~/.qgis2/python/plugins`
  * on *Windows*: `C:\\Users\<username>\.qgis2\python\plugins\`
  * make sure the dir is called LizardViewer. 

## Release
Make sure you have `zest.releaser` with `qgispluginreleaser` installed. To make a release (also see: [1]):
* `$ cd /path/to/the/plugin`
* `$ fullrelease  # NOTE: if it asks you if you want to check out the tag press 'y'.`

Manually copy to server:
* `$ scp LizardViewer.0.1.zip <user.name>@packages-server.example.local:/srv/packages.lizardsystem.nl/var/plugins`

## Tests
There are currently 4 tests (in the test folder).
These tests can be run by using `make test` [2].

## Other interesting QGIS plug-ins:
* [3Di QGIS plug-in](https://github.com/nens/threedi-qgis-plugin)

## Notes
[1]: Under the hood it calls `make zip` (see `Makefile`, the old zip directive is overwritten).
[2]: Make test uses `nose`. Make sure you have `nose` installed (`pip install nose`). And make sure the plugin dir has the right package name, is `LizardViewer` or else the relative imports won't work correctly. Then run `nosetests` inside the plugin directory:
`$ nosetests --with-doctest`
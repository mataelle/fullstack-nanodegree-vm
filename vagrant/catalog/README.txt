## Item Catalog

Catalog with some categories. Logged in users can add items, edit their own items and delete their items.
Application uses

To see it working, you need to clone this repository and install virtual machine (for this you need VirtualBox and Vagrant installed):

```
vagrant up
vagrant ssh
```

Then go to the shared folder:

```
cd /vagrant/catalog
```

You don't have to create and fill in the database, because the one is already created and included in repo.
But you also can do it by yourself:

```
python models.py
python insert_items.py
```

Run the app with command:

```
python webserver.py
```

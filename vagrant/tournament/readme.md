## tournament results

Exercise that includes creation of tables and implementation of query-functions.

To see it working, you need to clone this repository and install virtual machine (for this you need VirtualBox and Vagrant installed):

```
vagrant up
vagrant ssh
```

Then go to the shared folder:

```
cd /vagrant/tournament
```

After this you need to create tournament database and connect to it. I did it manually, so...

```
psql
create database tournament;
\c tournament
```

Now you can run script that will create tables:

```
\i tournament.sql
```

To run python script with test, you need to exit from psql:

```
\q
```

Then you can launch test script with command:

```
python tournament_test.py
```

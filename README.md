# CommandLineLabeller
A program to easily labelled the sentiment of texts in a sqlite database via the command line.

In this module contains a class which reads an sqlite file, whose table named 'texts' has the index column 'id', and 'phrase' column containing the strings to be labelled by the user in the command line. It has a 'sentiment' column, for which unlabelled sentiments are given the sentinal value of -99.

From the command line, one can label phrases in three classes, 1, 0, -1, for positive, neutral, and negative sentiment respectively. It allows the user to also skip phrases, and quit the session at any time having their work saved.

One can then load up the program at a later time to resume the labelling.

The program also includes an automatic backup of the database for each labelling session.

"""
A program to easily labelled the sentiment of texts in a sqlite database via
the command line.

In this module contains a class which reads an sqlite file, whose table named
'texts' has the index column 'id', and 'phrase' column containing the strings
to be labelled by the user in the command line. It has a 'sentiment' column,
for which unlabelled sentiments are given the sentinal value of -99.

From the command line, one can label phrases in three classes, 1, 0, -1, for
positive, neutral, and negative sentiment respectively. It allows the user to
also skip phrases, and quit the session at any time having their work saved.

One can then load up the program at a later time to resume the labelling.

The program also includes an automatic backup of the database for each
labelling session.
"""
import sqlite3
import shutil
import sys
import time


class LabelSession(object):

    def __init__(self, db_name):
        self.db_name = db_name
        self.cxn = sqlite3.connect(self.db_name)

    def backup_db(self):
        epoch_int = int(time.time())
        name_parts = self.db_name.split('.')
        new_name = name_parts[0] + '_' + str(epoch_int) + '.' + name_parts[1]
        shutil.copy(self.db_name, new_name)

    def session(self):
        unlabelled_id_text_tuple_list = self.get_unlabelled_texts()
        for n in unlabelled_id_text_tuple_list[:5]:
            print n[0]
            print n[1][:20]
        self.process_unlabelled_texts(unlabelled_id_text_tuple_list)
        self.close_connection()

    def get_unlabelled_texts(self):
        # TODO: this returns the entirity, alter to take chunks of a certain
        # size.
        cursor = self.cxn.cursor()
        sql_cmd = '''SELECT id, phrase FROM texts WHERE sentiment = -99
                     ORDER BY id'''
        unlabelled_id_text_tuple_list = cursor.execute(sql_cmd).fetchall()
        return unlabelled_id_text_tuple_list

    def process_unlabelled_texts(self, unlabelled_texts):
        for (id, unlabelled_text) in unlabelled_texts:
            user_sentiment = self.get_user_label(unlabelled_text)
            self.enter_user_label((id, user_sentiment))

    def get_user_label(self, unlabelled_text):
        correct_input = False
        while not correct_input:
            self.display_label_instructions()
            print unlabelled_text
            print '\n' + '-'*20
            user_input = \
                raw_input('\nWhat sentiment do you give the text?: ').strip()
            correct_input = self.check_sentiment_input(user_input)

        return user_input

    def enter_user_label(self, id_label_tuple):
        label_id, label_sentiment = id_label_tuple[:]
        if label_sentiment in ['1', '-1', '0']:
            label_sentiment = int(label_sentiment)
            cursor = self.cxn.cursor()
            cursor.execute('''UPDATE texts SET sentiment=? WHERE id=?''',
                           (label_sentiment, label_id))
            self.cxn.commit()
        elif label_sentiment == 'q':
            self.close_connection()
            sys.exit()
        elif label_sentiment == 's':
            # skip this text
            pass
        else:
            raise ValueError('Not sure user input for sentiment is correct')

    def display_label_instructions(self):
        print '\nRate the following text as either: ' +\
            '1 (for positive sentiment), -1 (for negative sentiment), ' +\
            'or 0 (for neutral sentiment). To skip a tweet type s.' +\
            ' To quit, exit terminal (all previous work hass been saved).'
        print '-'*20

    def check_sentiment_input(self, user_input):
        if user_input == '1':
            correct_input = True
        elif user_input == '-1':
            correct_input = True
        elif user_input == '0':
            correct_input = True
        elif user_input == 's':
            correct_input = True
        elif user_input == 'q':
            correct_input = True
        else:
            print '\nYou input: ' + user_input
            print 'Please input either pos, neg, or neu.\n'
            correct_input = False
        return correct_input

    def close_connection(self):
        self.cxn.close()


def main(argv):
    db_name = argv[1]
    label_session = LabelSession(db_name)
    label_session.backup_db()
    label_session.session()

if __name__ == "__main__":
    main(sys.argv)

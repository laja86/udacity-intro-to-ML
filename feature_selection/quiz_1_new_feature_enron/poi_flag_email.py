# # !/usr/bin/python

###
### in poiFlagEmail() below, write code that returns a boolean
### indicating if a given email is from a POI
###

import sys
# Note that "reader.py" and "poi_emails.py" imported by the grader are not
# available for editing, and are called when a Test Run or Submit is made.
import reader  # includes parseAddresses function
import poi_emails

def getToFromStrings(f):
    '''
    The imported reader.py file contains functions that we've created to help
    parse e-mails from the corpus. .getAddresses() reads in the opening lines
    of an e-mail to find the To: From: and CC: strings, while the
    .parseAddresses() line takes each string and extracts the e-mail addresses
    as a list.
    '''
    f.seek(0)
    to_string, from_string, cc_string   = reader.getAddresses(f)

    # I assume this returns a list based on to_emails processing below
    to_emails   = reader.parseAddresses( to_string )
    from_emails = reader.parseAddresses( from_string )
    cc_emails   = reader.parseAddresses( cc_string )

    return to_emails, from_emails, cc_emails


### POI flag an email, returns tuple of 3 bools
def poiFlagEmail(f):
    """ given an email file f,
        return a trio of booleans for whether that email is
        to, from, or cc'ing a poi """

    to_emails, from_emails, cc_emails = getToFromStrings(f)

    ### poi_emails.poiEmails() returns a list of all POIs' email addresses.
    poi_email_list = poi_emails.poiEmails()

    to_poi = False
    from_poi = False
    cc_poi   = False

    ### to_poi and cc_poi are related functions, which flag whether
    ### the email under inspection is addressed to a POI, or if a POI is in cc
    ### you don't have to change this code at all

    ### there can be many "to" emails, but only one "from", so the
    ### "to" processing needs to be a little more complicated
    #       uses counter for iteration, duplicates process for cc_emails
    #           does not seem very pythonic, but maybe clearest method
    if to_emails:
        ctr = 0  # counter for iterating through, perhaps not pythonic
        while not to_poi and ctr < len(to_emails):
            if to_emails[ctr] in poi_email_list:
                to_poi = True
            ctr += 1
    if cc_emails:
        ctr = 0
        while not to_poi and ctr < len(cc_emails):
            if cc_emails[ctr] in poi_email_list:
                cc_poi = True
            ctr += 1


    #################################
    ######## your code below ########
    ### set from_poi to True if #####
    ### the email is from a POI #####
    #################################
    # initial difficulty getting correct output because I was not
    #   I had from_email in... instead of from_emails[0] in...
    #   (needs item index for list, even though only one item in list)
    assert len(from_emails) == 1
    from_poi = True if from_emails[0] in poi_email_list else False

    # assert from_emails == True
    # if from_emails:
    #   if from_emails[0] in poi_email_list:
    #       from_poi = True





    #################################
    return to_poi, from_poi, cc_poi

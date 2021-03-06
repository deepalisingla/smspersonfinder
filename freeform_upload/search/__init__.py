import urllib2
from models import *
from util import *

SubDomain = "rhok"
AuthToken = "soNQ67BhLRP0tIvP"
host = "https://googlepersonfinder.appspot.com"

def name_search(name, persons):
    found_persons = []
    name = name.lower()

    for person in persons:
        full_name = person.full_name
        first_name = person.first_name
        last_name = person.last_name

        if full_name and full_name.lower().find(name):
            found_persons.append(person)
            continue
        elif first_name and first_name.lower().find(name):
            found_persons.append(person)
            continue
        elif last_name and last_name.lower().find(name):
            found_persons.append(person)
            continue

    return found_persons

def format_info(person) :
   result=""
   if person.full_name:
       result += person.full_name + " "
   else:
      if person.first_name:
         result += person.first_name + " "
      if person.last_name:
         result += person.last_name + " "
   if person.sex:
      result += person.sex + " "
   if person.date_of_birth:
      result += person.date_of_birth + " "
   elif person.age:
      result += person.age + " "

   found_status = 0
   found_location = 0
   found_contact = 0
   found_text = 0

   note_text = ""

   while len(person.notes):
      note = person.notes.pop()
      if found_status == 0 and note.status:
         result += note.status + " "
         found_status = 1
         #Collect Note text from the last known status
         if note.text:
            note_text = note.text
            found_text = 1
      if found_location == 0 and note.last_known_location:
         result += note.last_known_location + " "
         found_location = 1
      if found_contact == 0 and note.phone_of_found_person:
         result += note.phone_of_found_person + " "
         found_contact = 1
         break

   if found_status == 0:
      result += "Status - Unknown"
   elif found_text:
      result += "Notes: " + note_text
   #print result
   return result

def print_person_info(person):
    print "person_record_id..%s" % person.person_record_id
    print "entry_date........%s" % person.entry_date
    print "expiry_date.......%s" % person.expiry_date
    print "author_name.......%s" % person.author_name
    print "author_email......%s" % person.author_email
    print "author_phone......%s" % person.author_phone
    print "source_name.......%s" % person.source_name
    print "source_date.......%s" % person.source_date
    print "source_url........%s" % person.source_url
    print "full_name.........%s" % person.full_name
    print "first_name........%s" % person.first_name
    print "last_name.........%s" % person.last_name
    print "sex...............%s" % person.sex
    print "date_of_birth.....%s" % person.date_of_birth
    print "age...............%s" % person.age
    print "home_city.........%s" % person.home_city
    print "home_state........%s" % person.home_state
    print "home_neighborhood.%s" % person.home_neighborhood
    print "home_street.......%s" % person.home_street
    print "home_postal_code..%s" % person.home_postal_code
    print "photo_url.........%s" % person.photo_url
    print "other.............%s" % person.other
    print "home_country......%s" % person.home_country

def print_note_info(note):
    print "note_record_id..............%s" % note.note_record_id
    print "person_record_id............%s" % note.person_record_id
    print "linked_person_record_id.....%s" % note.linked_person_record_id
    print "entry_date..................%s" % note.entry_date
    print "author_name.................%s" % note.author_name
    print "author_email................%s" % note.author_email
    print "author_phone................%s" % note.author_phone
    print "source_date.................%s" % note.source_date
    print "found.......................%s" % note.found
    print "email_of_found_person.......%s" % note.email_of_found_person
    print "phone_of_found_person.......%s" % note.phone_of_found_person
    print "last_known_location.........%s" % note.last_known_location
    print "text........................%s" % note.text
    print "status......................%s" % note.status

def handle(message):
    query_uri = "/api/search?key=" + AuthToken + "&subdomain=" + SubDomain + "&q=" + message
    data = urllib2.urlopen("%s%s" % (host, query_uri)).read()
    dom1 = dom.parseString(data)
    (persons, notes) = from_xml(dom1)
    found_persons = name_search(message, persons)
    persons_str = ""
    count = 0
    if found_persons:
        for person in found_persons:
           #add a new line after each person entry in the result
            if count == 0:
               persons_str += "\n"
            persons_str += format_info(person)
            count += 1

    return persons_str

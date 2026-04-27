HOW TO RUN
1. Make sure PostgreSQL is open and database phonebook exists.
2. Password in config.py is 12345678.
3. Run:
   python phonebook.py

IMPORTANT ORDER
1. Choose 1 first: Create clean schema + load functions/procedures
2. Choose 3: Import from CSV
3. Then test other menu options.

WHAT IS IMPLEMENTED
- contacts table with email, birthday, group_id, date_added
- groups table
- phones table for multiple phones per contact
- CSV import with email, birthday, group, phone type
- JSON export
- JSON import with duplicate handling: skip / overwrite
- filter by group
- search by email
- sort by name, birthday, date added
- paginated navigation with get_contacts_page function
- procedure add_phone
- procedure move_to_group
- function search_contacts searches name, surname, email, and all phones

GIT COMMIT EXAMPLES
init extended phonebook schema
add groups and multiple phones
add search filters sorting and pagination
add json import export
add phonebook stored procedures

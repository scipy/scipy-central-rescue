import psycopg2
import os, re
import sphinx_generator

#Fixes any faulty syntax in documentation descriptions displaying images
def add_images(description):
    image_directory = '/Data/media/images/'
    replaced_image_tags = re.sub(":image:`", "\n.. image:: "+image_directory, description)
    removed_quotations = re.sub(".png`", ".png", replaced_image_tags)
    removed_quotations = re.sub(".jpg`", ".jpg", removed_quotations)
    return removed_quotations


conn = psycopg2.connect("dbname=scipy_central user=postgres")
cur = conn.cursor()
cur.execute("SELECT a.entry_id, a.title, a.slug, a.created_by_id, a.description, a.date_created, b.fileset_id INTO temp FROM submission_revision a INNER JOIN submission_submission b on a.entry_id = b.id WHERE b.sub_type = 'snippet' AND (a.slug LIKE ' ' OR a.title LIKE ' ' OR a.slug LIKE '-' OR a.title LIKE '-' OR a.id < 100);")

cur.execute("SELECT * FROM temp;")
temp = cur.fetchall()

submissions = {}
#Creates a dictionary storing info for each submission
for submission in temp:
    sub_info = {}
    sub_id, sub_title, sub_slug, sub_author_id, sub_desc, sub_date, sub_fileset_id = submission
    sub_info["id"] = sub_id
    sub_info["title"] = sub_title
    sub_info["slug"] = sub_slug
    sub_info["author_id"] = sub_author_id
    sub_info["description"] = add_images(sub_desc)
    sub_info["date"] = sub_date
    submissions[sub_id] = sub_info

cur.execute("SELECT a.entry_id, a.title, a.date_created, b.repo_path INTO repos FROM temp a INNER JOIN filestorage_fileset b on a.fileset_id = b.id;")
cur.execute("SELECT entry_id, repo_path FROM repos;")
repos = cur.fetchall()

#Finds repo_path of each code snippet, and adds the file name into the submission info dictionary
for entry_id, repo_path in repos:
     submissions[entry_id]["repo_path"] = repo_path
     files = os.listdir('./SPC Static Data/code/' + repo_path)
     python_files = []
     for file_name in files:
         if file_name[-3:] == ".py":
             python_files.append(file_name)
     if len(python_files) == 0:
         print "ERROR: no python files in directory", repo_path
     elif len(python_files) > 1:
         submissions[entry_id]["snippet_file"] = python_files[0]
     else:
         submissions[entry_id]["snippet_file"] = python_files[0]

#Joins temp table and person_profile table on user_id's to get author usernames
cur.execute("SELECT t.entry_id, p.slug FROM temp t INNER JOIN person_userprofile p on p.user_id = t.created_by_id")
authors = cur.fetchall()

for entry_id, author_user in authors:
    submission = submissions[entry_id]
    submission["author"] = author_user

cur.execute("DROP TABLE temp")

#Creates a file directory for all created rst files
if not os.path.exists("rst-files"):
    os.makedirs("rst-files")

with open("rst-file-names.rst", 'w') as file_names:
    for submission_id, submission in submissions.iteritems():
        sphinx_generator.create_rst_file(submission)
        #Puts all rst files in a folder
        file_name = str(submission["id"])+'-'+submission["slug"]+'.rst'
        new_folder_dest = './rst-files/' + file_name
        os.rename('./'+file_name, new_folder_dest)
        #Writes all rst file names to a text file for toctree
        new_file_name = 'rst-files/' + file_name
        file_names.write(new_file_name + "\n")

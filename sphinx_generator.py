'''Given a dictionary containing information about a file, sphinx_generator
generates an RST file to be used by Sphinx'''

def create_rst_file(file_info):
    title = file_info["title"]
    entry_id = file_info["id"]
    slug = file_info["slug"]
    author = file_info["author"]
    date = file_info["date"]
    description = file_info["description"]
    snippet_file = file_info["snippet_file"]
    repo_path = file_info["repo_path"]
    if "image" in file_info.keys():
         image = file_info["image"]

    with open(str(entry_id)+'-'+slug+".rst", 'w') as rst_file:
        #Writes title of file
        rst_file.write(title + "\n")
        for letter in title:
            rst_file.write("=")
        rst_file.write('\n\n')

        #Writes author and date
        rst_file.write("**Author:** " + str(author) + "\n\n**Submitted on:** " + str(date) + "\n\n")

        #Adds description
        rst_file.write(description + "\n\n")

        #Adds code snippet
        if snippet_file[0:1] != '/' and repo_path[-1:] != '/':
            snippet_file_path = '/Data/code/' + repo_path + '/'+ snippet_file
        else:
            snippet_file_path = '/Data/code/' + repo_path + snippet_file
        print snippet_file_path
        rst_file.write(".. literalinclude:: " + snippet_file_path + "\n\t:language: python\n\n")

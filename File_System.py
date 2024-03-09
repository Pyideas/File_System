#CLASSE PER OPERAZIONI DI FILE SYSTEM:
class File_System():
    #Attributo Di Classe:
    forbidden_chars = '/\:*?"<>|'

    #Elencazione Del Contenuto Di Una Cartella:
    def listdir(folder: str)-> tuple[bool,str]:
        #Caso parametro nullo:
        if folder == '': folder = os.getcwd()
        #Caso cartella inesistente:
        if not os.path.isdir(folder):
            return (False,f'The folder "{folder}" doesn\'t exist')
        #Caso cartella protetta:
        try: dir_list = os.listdir(folder)
        except: return (False,f'"{folder}" is system-protected folder')
        #Caso cartella vuota:
        if dir_list == []:
            return (False,f'The folder "{folder}" is empty')
        #Elencazione del contenuto della cartella:
        resources = ''
        for res in dir_list:
            if os.path.isdir(os.path.join(folder,res)): type = 'fold'
            elif os.path.splitext(res)[1] == '.lnk': type = 'link'
            elif os.path.isfile(os.path.join(folder,res)): type = 'file'
            else: type = '????'
            resources += f'[{type}]  {res}\n' #[tipo]   *nome risorsa*
        return (True, resources.strip())

    #Creazione Di Un File:
    def create_file(file: str)-> tuple[bool,str]:
        basename = os.path.basename(file)
        #Caso nome file nullo:
        if basename == '':
            return (False,f'ERROR: Missing file name in "{file}"')
        #Caso caratteri proibiti:
        if any([ char in basename for char in File_System.forbidden_chars ]):
            return (False,f'ERROR: The file name "{file}" can\'t have these characters: {File_System.forbidden_chars}')
        #Caso mancata estensione:
        if not '.' in basename:
            return (False,f'ERROR: Missing extension in "{file}"')
        #Caso file già esistente:
        if os.path.exists(file):
            return (False,f'The file "{file}" already exists')
        #File increabile:
        try: open(file,'x').close()
        except: return (False,f'Unable to create "{file}"')
        #File creato:
        return (True,f'"{file}" created')

    #Rimozione Di Un File:
    def remove_file(file: str)-> tuple[bool,str]:
        #Caso file inesistente:
        if not os.path.exists(file):
            return (False,f'The file "{file}" doesn\'t exist')
        #Caso file irrimovibile:
        try: os.remove(file)
        except: return (False,f'Unable to remove "{file}"')
        #Rimozione del file avvenuta:
        return (True,f'"{file}" removed')

    #Creazione Di Una Cartella:
    def create_folder(folder: str)-> tuple[bool,str]:
        #Caso parametro nullo:
        if folder == '':
            return (False,'ERROR: Missing name')
        #Caso caratteri proibiti:
        if any([ char in folder for char in File_System.forbidden_chars[1:] ]):
            return (False,f'ERROR: The folder name "{folder}" can\'t have these characters: {File_System.forbidden_chars[1:]}')
        #Caso cartella già esistente:
        if os.path.exists(folder):
            return (False,f'The folder "{folder}" already exists')
        #Caso cartella increabile:
        try: os.makedirs(folder)
        except: return (False,f'Unable to create "{folder}"')
        #Cartella creata:
        return (True,f'"{folder}" created')

    #Rimozione Di Una Cartella:
    def remove_folder(folder: str)-> tuple[bool,str]:
        #Caso cartella inesistente:
        if not os.path.isdir(folder):
            return (False,f'The folder "{folder}" doesn\'t exist')
        #Caso cartella irremovibile:
        try: os.removedirs(folder)
        except: return (False,f'Unable to remove "{folder}"')
        #Rimozione della cartella avvenuta:
        return (True,f'"{folder}" removed')

    #ATTENZIONE: CODICE MOLTO PERICOLOSO!!!
    def delete_tree(folder: str)-> tuple[bool,str]:
        #Caso cartella inesistente:
        if not os.path.exists(folder):
            return (False,f'The folder "{folder}" doesn\'t exist')
        #Rimozione dell'albero di cartelle:
        not_eliminated = ''
        for path, _, files in os.walk(folder, False):
            for file in files:
                file_path = os.path.join(path,file)
                try: os.remove(file_path)
                except: not_eliminated += f'{file_path}\n'
            try: os.rmdir(path) #Rimozione del percorso svuotato.
            except: not_eliminated += f'{path}\n'
        #Caso eliminazione parziale:
        if not_eliminated != '':
            return (False,f'Error deleting:\n{not_eliminated.strip()}')
        #Caso eliminazione totale:
        return (True,f'"{folder}" deleted')

    #Rinominazione Di File E Cartelle:
    def rename(resource: str, new_name: str)-> tuple[bool,str]:
        #Caso risorsa inesistente:
        if not os.path.exists(resource):
            return (False,f'The resource "{resource}" doesn\'t exist')
        #Caso nuovo nome mancante:
        if new_name == '':
            return (False,f'ERROR: Missing new name for "{resource}"')
        #Caso caratteri proibiti:
        if any([ char in new_name for char in File_System.forbidden_chars ]):
            return (False,f'ERROR: The resource new name "{new_name}" can\'t have these characters: {File_System.forbidden_chars}')
        #Risolvo problema di sintassi imprecisa:
        if resource[-1] in '/\\': resource = resource[:-1]
        #Ricavo l'estensione in caso di file se non specificata:
        ext = os.path.splitext(resource)[1] if os.path.isfile(resource) and not '.' in new_name else ''
        #Caso risorsa inrinominabile:
        try: os.renames(resource, os.path.join(os.path.dirname(resource),new_name+ext))
        except: return (False,f'Unable to rename "{resource}"')
        #Risorsa rinominata:
        return (True,f'"{resource}" renamed in: {new_name}')

    #Spostamento Di File E Cartelle:
    def move(resource: str, destination: str)-> tuple[bool,str]:
        from shutil import move
        destination_path = os.path.join(destination,os.path.basename(resource))
        #Caso risorsa inesistente:
        if not os.path.exists(resource):
            return (False,f'The resource "{resource}" doesn\'t exist')
        #Caso destinazione inesistente:
        if not os.path.isdir(destination) and destination != '':
            return (False,f'The destination "{destination}" doesn\'t exist')
        #Caso risorsa già esistente nella destinazione:
        if os.path.exists(destination_path):
            return (False,f'The resource "{resource}" altready exists in "{destination}"')
        #Caso risorsa immovibile:
        try: move(resource, destination_path)
        except: return (False,f'Unable to move "{resource}" to "{destination}"')
        #Risorsa spostata:
        if destination in '.': destination = 'current folder'
        return (True,f'"{resource}" moved to: {destination}')

     def copy(resource: str, destination: str)-> tuple[bool,str]:
        from shutil import copytree, copyfile
        destination_path = os.path.join(destination,os.path.basename(resource))
        #Caso risorsa inesistente:
        if not os.path.exists(resource):
            return (False,f'The resource "{resource}" doesn\'t exist')
        #Caso destinazione inesistente:
        if not os.path.isdir(destination) and destination != '':
            return (False,f'The destination "{destination}" doesn\'t exist')
        #Caso risorsa già esistente nella destinazione:
        if os.path.exists(destination_path):
            return (False,f'The resource "{resource}" already exists in "{destination}"')
        #Caso risorsa incopiabile:
        try:
            if os.path.isdir(resource):
                copytree(resource, destination_path)
            else: copyfile(resource, destination_path)
        except: return (False,f'Unable to copy "{resource}" to "{destination}"')
        #Risorsa copiata:
        if destination in '.': destination = 'current folder'
        return (True,f'"{resource}" copied to: {destination}')


"""Current tool directory names for the retained construction metadata keys."""
DIRECTORY_NAMES={
 'bootasm':'bootasm','asm86':'asm0','asma0':'asm1','asm86a':'asm86',
 'ir86':'ir86','rill':'rill0','rb':'rillboot','rc':'rill',
 'toolchain':'toolchain','link86':'link86','edit86':'edit86',
}
def directory_name(collection):return DIRECTORY_NAMES.get(collection,collection)
def collection_key(directory):
 return next((key for key,name in DIRECTORY_NAMES.items() if name==directory),directory)

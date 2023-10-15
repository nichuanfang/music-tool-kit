from git_changelog.cli import get_release_notes
from actions_toolkit import core

res: str  = get_release_notes()
compare= res.split('\n\n')[1].split('[Compare with latest]')[1].split('(')[1].rsplit(')', 1)[0]
core.set_output('compare', compare)
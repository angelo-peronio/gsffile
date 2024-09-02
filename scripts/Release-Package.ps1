# Tag a release and push to remotes/origin.
# A GitHub action will then build, test, release on PyPi.

# Known bug:
# will fail if encounters a git tag different form a version tag "v<major>.<minor>.<patch>".

Param (
    [Parameter(Mandatory, HelpMessage = "Please provide a version, in the form <major>.<minor>.<patch>.")]
    [Version]$Version
)

$ErrorActionPreference = "Stop"

$CurrentBranch = git branch --show-current
if ($CurrentBranch -ne "master") {
    throw "Release invoked, but not on master branch.`n" `
        + "You probably want to merge your work into master. Quitting."
}

# https://stackoverflow.com/a/50737015
# https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git/17192101#comment23385634_3258271
$UpToDate = git rev-list HEAD..origin/master --count
if (-Not $UpToDate) {
    throw "Local repository is not up-to-date. Run git pull. Quitting."
}

# https://stackoverflow.com/a/5737794
$Dirty = git status --porcelain
if ($Dirty) {
    throw "Release invoked, but the working copy is dirty.`n" `
        + "You probably want to commit your work. Quitting."
}

$Patch = $Version.Revision
if ($Patch -ne -1) {
    throw "Supplied version $Version is not in the form <major>.<minor>.<patch>. Quitting."
}

# https://stackoverflow.com/a/7261049
git fetch --tags
$PreviousVersionTag = git describe --tags --abbrev=0
$PreviousVersion = [Version]$PreviousVersionTag.Substring(1)

if ($PreviousVersion -ge $Version) {
    throw "Existing version $PreviousVersion is greter or equal than supplied version $Version."
}

$VersionTag = "v$Version"
git tag --annotate --message "Version $Version" $VersionTag
git push --follow-tags

import requests
import semver

from packages.models import VersionedPackage

NPM_REGISTRY_URL = "https://registry.npmjs.org"  # idea: move to settings

# idea: add docstrings to functions
# review: add exception handling / logging (e.g. indicate if version is invalid, etc.)
def get_package(name: str, range: str) -> VersionedPackage: # review: rename range (reserved keyword - use what semver uses if you want `range_`)
    url = f"{NPM_REGISTRY_URL}/{name}"

    # review: you could wrap this in a separate class to make the interactions with the API simpler and easier to test
    npm_package = requests.get(url).json()
    # review: you shouldn't need to cast to list here
    versions = list(npm_package["versions"].keys())
    version = semver.min_satisfying(versions, range)
    version_record = npm_package["versions"][version]

    package = VersionedPackage(
        name=version_record["name"],
        version=version_record["version"],
        description=version_record["description"],
    )
    dependencies = version_record.get("dependencies", {})

    # review: You should introduce a cache to prevent extra calls to NPM for dependencies already in memory
    package.dependencies = [
        get_package(name=dep_name, range=dep_range) for dep_name, dep_range in dependencies.items()
    ]

    return package


# review: did you forget to use this above? This looks like it is mid-refactor, would be good to use it or delete it
def request_package(name: str, range: str) -> tuple[VersionedPackage, dict]:
    url = f"{NPM_REGISTRY_URL}/{name}"

    npm_package = requests.get(url).json()

    versions = list(npm_package["versions"].keys())
    version = semver.min_satisfying(versions, range)
    version_record = npm_package["versions"][version]

    return VersionedPackage(
        name=version_record["name"],
        version=version_record["version"],
        description=version_record["description"],
    ), version_record.get("dependencies", {})

import requests
import semver

from packages.models import VersionedPackage

NPM_REGISTRY_URL = "https://registry.npmjs.org"  # idea: move to settings

versioned_package_cache = {}

# idea: add docstrings to functions
# review: add exception handling / logging (e.g. indicate if version is invalid, etc.)
def get_package(name: str,
                range: str,
                seen_dependencies: set = None) -> VersionedPackage:  # review: rename range (reserved keyword - use what semver uses if you want `range_`)

    if name in versioned_package_cache:
        return versioned_package_cache[name]

    if seen_dependencies is None:
        seen_dependencies = set()

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

    seen_dependencies.add(name)
    for dep_name, dep_range in dependencies.items():
        dependency = get_package(name=dep_name, range=dep_range, seen_dependencies=seen_dependencies) \
            if dep_name not in seen_dependencies \
            else VersionedPackage(
            name=dep_name,
            version=dep_range,
            description="dependency loop",
        )
        package.dependencies.append(dependency)

    versioned_package_cache[name] = package

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

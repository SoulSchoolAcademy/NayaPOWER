import json
import os
import platform
import sys

FIXTURE = os.environ["TEST13_EXPECTED_FIXTURE"]
EXPECTED_BRANCH = os.environ["TEST13_EXPECTED_BRANCH"]

with open(FIXTURE, encoding="utf-8") as f:
    fixture = json.load(f)

assert os.environ.get("GITHUB_ACTIONS") == "true", "Not running inside GitHub Actions"
assert os.environ.get("GITHUB_REF_NAME") == EXPECTED_BRANCH, "Wrong branch"
assert os.environ.get("GITHUB_REF_NAME") != "main", "main mutation boundary violated"
assert fixture["expected_runner"] == "ubuntu-latest", "Fixture runner contract mismatch"
assert fixture["expected_permissions"]["contents"] == "read", "Fixture permission contract mismatch"
assert fixture["main_mutation_allowed"] is False, "Fixture permits main mutation"
assert fixture["deployment_allowed"] is False, "Fixture permits deployment"
assert fixture["secrets_required"] is False, "Fixture requires secrets"
assert sys.platform.startswith("linux"), f"Expected Linux runner, got {sys.platform}"
assert platform.system() == "Linux", f"Expected Linux runner, got {platform.system()}"

print("T13_RUNNER=RUNNING")
print(f"T13_REPOSITORY={os.environ.get('GITHUB_REPOSITORY', '<unset>')}")
print(f"T13_REF={os.environ.get('GITHUB_REF_NAME', '<unset>')}")
print(f"T13_PLATFORM={platform.system()}")
print("T13_FIXTURE=PUBLIC")
print("T13_SECRETS_REQUIRED=FALSE")
print("T13_DEPLOYMENT=DISABLED")
print("T13_MAIN_MUTATION=FORBIDDEN")
print("T13_VERIFIER=PASS")

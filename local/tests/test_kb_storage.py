import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "skill"))
import kb_storage


class FakeContext:
    def __init__(self, secrets=None):
        self._secrets = dict(secrets or {})

    def get_secret(self, name):
        return self._secrets.get(name)


class TestKbStorage(unittest.TestCase):
    def test_resolve_config_defaults_and_github_fallbacks(self):
        ctx = FakeContext(
            {
                "GITHUB_OWNER": "acme",
                "GITHUB_REPO": "docs",
                "GITHUB_BRANCH": "develop",
                "GITHUB_TOKEN": "legacy-token",
            }
        )
        cfg = kb_storage._resolve_config(ctx)
        self.assertEqual(cfg["provider"], "github")
        self.assertEqual(cfg["owner"], "acme")
        self.assertEqual(cfg["repo"], "docs")
        self.assertEqual(cfg["project"], "acme/docs")
        self.assertEqual(cfg["branch"], "develop")
        self.assertEqual(cfg["token"], "legacy-token")

    def test_github_raw_url(self):
        cfg = {
            "owner": "owner1",
            "repo": "repo1",
            "branch": "main",
        }
        got = kb_storage._github_raw_url(cfg, "kb/subdir/file.md")
        self.assertEqual(
            got,
            "https://raw.githubusercontent.com/owner1/repo1/main/kb/subdir/file.md",
        )

    def test_gitlab_raw_url_encodes_project_and_path(self):
        ctx = FakeContext(
            {
                "KB_GIT_PROVIDER": "gitlab",
                "KB_REPO": "group/project",
            }
        )
        cfg = kb_storage._resolve_config(ctx)
        got = kb_storage._gitlab_raw_url(cfg, "kb/sub dir/file.md")
        self.assertEqual(
            got,
            "https://gitlab.com/api/v4/projects/group%2Fproject/repository/files/"
            "kb%2Fsub%20dir%2Ffile.md/raw?ref=main",
        )

    def test_kb_repo_overrides_github_owner_repo(self):
        ctx = FakeContext(
            {
                "KB_REPO": "new-owner/new-repo",
                "GITHUB_OWNER": "old-owner",
                "GITHUB_REPO": "old-repo",
            }
        )
        cfg = kb_storage._resolve_config(ctx)
        self.assertEqual(cfg["provider"], "github")
        self.assertEqual(cfg["owner"], "new-owner")
        self.assertEqual(cfg["repo"], "new-repo")
        self.assertEqual(cfg["project"], "new-owner/new-repo")

    def test_header_helpers_with_and_without_tokens(self):
        gh = kb_storage._github_headers("gh-token")
        self.assertEqual(gh.get("Authorization"), "Bearer gh-token")
        self.assertEqual(gh.get("Accept"), "application/vnd.github+json")

        gh_no = kb_storage._github_headers("")
        self.assertNotIn("Authorization", gh_no)
        self.assertEqual(gh_no.get("Accept"), "application/vnd.github+json")

        gh_write = kb_storage._github_write_headers("gh-token")
        self.assertEqual(gh_write.get("X-GitHub-Api-Version"), "2022-11-28")

        gl = kb_storage._gitlab_headers("gl-token")
        self.assertEqual(gl.get("PRIVATE-TOKEN"), "gl-token")
        self.assertEqual(gl.get("Accept"), "application/json")

        gl_no = kb_storage._gitlab_headers("")
        self.assertNotIn("PRIVATE-TOKEN", gl_no)
        self.assertEqual(gl_no.get("Accept"), "application/json")


if __name__ == "__main__":
    unittest.main()


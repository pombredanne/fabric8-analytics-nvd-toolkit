"""Tests for ecos module."""

import os
import unittest

from toolkit.preprocessing.handlers import GitHandler
from toolkit.preprocessing.ecos import Package, Maven


TEST_MAVEN_REPO_URL = "https://github.com/inversoft/prime-jwt/"
TEST_TRAVERSAL_PATH = "src/main/java/org/primeframework/jwt/"


class TestMaven(unittest.TestCase):
    """Tests for maven ecosystem."""

    def test_find_pom_files(self):
        """Test MavenRepository `find_pom_files` method."""
        with GitHandler.clone(TEST_MAVEN_REPO_URL) as git:
            repo_dir = git.repository

            pom_files = Maven.find_pom_files(repo_dir)

            self.assertIsNotNone(pom_files)
            self.assertTrue(any(pom_files))
            self.assertTrue(all([f.endswith('.xml') for f in pom_files]))

            # try it with reverse search
            child_path = os.path.join(repo_dir, TEST_TRAVERSAL_PATH)
            pom_files = Maven.find_pom_files(child_path, topdown=False)
            print(pom_files)

            self.assertIsNotNone(pom_files)
            self.assertTrue(any(pom_files))
            self.assertTrue(all([f.endswith('.xml') for f in pom_files]))

    def test_get_package_from_spec(self):
        """Test MavenRepository `get_package_from_spec` method."""
        with GitHandler.clone(TEST_MAVEN_REPO_URL) as git:
            repo_dir = git.repository

            pom_files = Maven.find_pom_files(repo_dir)
            assert any(pom_files)

            with open(pom_files[0], 'r') as pom_spec:
                package = Maven.get_package_from_spec(pom_spec)

                self.assertIsNotNone(package)
                self.assertTrue(isinstance(package, Package))

    def test_find_packages(self):
        """Test MavenRepository `find_packages` method."""
        with GitHandler.clone(TEST_MAVEN_REPO_URL) as git:
            repo_dir = git.repository

            packages = Maven.find_packages(repo_dir)

            self.assertIsNotNone(packages)
            self.assertTrue(any(packages))
            self.assertTrue(all([isinstance(f, Package) for f in packages]))
